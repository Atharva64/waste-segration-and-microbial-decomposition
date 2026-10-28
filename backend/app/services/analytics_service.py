import datetime as dt

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from backend.app.models import Feedback, Prediction, WasteCategory


def get_analytics_summary(
    db: Session,
    *,
    days: int = 7,
) -> dict:
    """
    Aggregate prediction history for the analytics dashboard.

    Counts are computed in SQL, so they stay correct even when there
    are more predictions than the history endpoint's 100-row limit.
    """

    total_predictions = (
        db.scalar(select(func.count(Prediction.id))) or 0
    )

    average_confidence = db.scalar(
        select(func.avg(Prediction.confidence))
    )

    # --------------------------------------------------------
    # Predictions per waste category (zero-count categories kept)
    # --------------------------------------------------------

    category_rows = db.execute(
        select(
            WasteCategory.slug,
            WasteCategory.name,
            func.count(Prediction.id),
        )
        .outerjoin(
            Prediction,
            Prediction.predicted_category_id == WasteCategory.id,
        )
        .group_by(
            WasteCategory.id,
            WasteCategory.slug,
            WasteCategory.name,
        )
        .order_by(WasteCategory.id)
    ).all()

    by_category = [
        {"slug": slug, "name": name, "count": int(count)}
        for slug, name, count in category_rows
    ]

    top_category = None

    if total_predictions > 0 and by_category:
        top_category = max(
            by_category,
            key=lambda item: item["count"],
        )["slug"]

    # --------------------------------------------------------
    # Predictions per day for the last N days (zero days filled)
    # --------------------------------------------------------

    # Use the database's own "today" so day boundaries match
    # func.date(created_at), which is evaluated in the DB session.
    today = db.scalar(select(func.current_date()))
    start_date = today - dt.timedelta(days=days - 1)

    day_column = func.date(Prediction.created_at)

    daily_rows = db.execute(
        select(day_column, func.count(Prediction.id))
        .where(day_column >= start_date)
        .group_by(day_column)
        .order_by(day_column)
    ).all()

    counts_by_day = {
        row_date: int(count)
        for row_date, count in daily_rows
    }

    scans_per_day = [
        {
            "date": start_date + dt.timedelta(days=offset),
            "count": counts_by_day.get(
                start_date + dt.timedelta(days=offset),
                0,
            ),
        }
        for offset in range(days)
    ]

    # --------------------------------------------------------
    # User feedback on prediction correctness
    # --------------------------------------------------------

    feedback_total = (
        db.scalar(select(func.count(Feedback.id))) or 0
    )

    feedback_correct = (
        db.scalar(
            select(func.count(Feedback.id)).where(
                Feedback.was_prediction_correct.is_(True)
            )
        )
        or 0
    )

    feedback_incorrect = (
        db.scalar(
            select(func.count(Feedback.id)).where(
                Feedback.was_prediction_correct.is_(False)
            )
        )
        or 0
    )

    return {
        "days": days,
        "total_predictions": int(total_predictions),
        "average_confidence": (
            float(average_confidence)
            if average_confidence is not None
            else None
        ),
        "top_category": top_category,
        "by_category": by_category,
        "scans_per_day": scans_per_day,
        "feedback_total": int(feedback_total),
        "feedback_correct": int(feedback_correct),
        "feedback_incorrect": int(feedback_incorrect),
    }
