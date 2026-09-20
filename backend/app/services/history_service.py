from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.app.models import (
    Feedback,
    Prediction,
    Recommendation,
    WasteCategory,
)
from backend.app.schemas.history import (
    FeedbackCreate,
)


# ============================================================
# Prediction Persistence
# ============================================================

def save_prediction(
    db: Session,
    *,
    filename: str | None,
    prediction_result: dict,
) -> Prediction:
    """
    Save one AI prediction to PostgreSQL.
    """

    predicted_class = (
        prediction_result["predicted_class"]
        .strip()
        .lower()
    )

    category = db.scalar(
        select(WasteCategory).where(
            WasteCategory.slug == predicted_class
        )
    )

    if category is None:
        raise RuntimeError(
            "Predicted category is not present in "
            "waste_categories. Seed the application "
            "waste categories before using /api/predict."
        )

    prediction = Prediction(
        image_path=filename,
        predicted_category_id=category.id,
        predicted_item_id=None,
        confidence=Decimal(
            str(
                prediction_result[
                    "confidence"
                ]
            )
        ),
        class_probabilities=prediction_result[
            "probabilities"
        ],
        model_name=prediction_result[
            "model_name"
        ],
        model_version=None,
    )

    try:
        db.add(prediction)
        db.commit()
        db.refresh(prediction)

    except Exception:
        db.rollback()
        raise

    return prediction


# ============================================================
# Prediction History
# ============================================================

def get_prediction_history(
    db: Session,
    *,
    limit: int = 50,
):
    """
    Return newest predictions first.
    """

    statement = (
        select(
            Prediction,
            WasteCategory.slug.label(
                "predicted_class"
            ),
        )
        .join(
            WasteCategory,
            WasteCategory.id
            == Prediction.predicted_category_id,
        )
        .order_by(
            Prediction.created_at.desc()
        )
        .limit(limit)
    )

    rows = db.execute(
        statement
    ).all()

    history = []

    for prediction, predicted_class in rows:
        history.append(
            {
                "id": prediction.id,
                "filename": prediction.image_path,
                "predicted_class": predicted_class,
                "confidence": float(
                    prediction.confidence
                ),
                "probabilities": (
                    prediction.class_probabilities
                ),
                "model_name": prediction.model_name,
                "model_version": (
                    prediction.model_version
                ),
                "created_at": (
                    prediction.created_at
                ),
            }
        )

    return history


# ============================================================
# Feedback Persistence
# ============================================================

def create_feedback(
    db: Session,
    payload: FeedbackCreate,
) -> Feedback:
    """
    Validate and save user feedback.
    """

    prediction = db.get(
        Prediction,
        payload.prediction_id,
    )

    if prediction is None:
        raise LookupError(
            "Prediction not found."
        )

    if (
        payload.was_prediction_correct is True
        and payload.corrected_category_id
        is not None
    ):
        raise ValueError(
            "corrected_category_id should not be "
            "provided when was_prediction_correct "
            "is true."
        )

    if payload.recommendation_id is not None:
        recommendation = db.get(
            Recommendation,
            payload.recommendation_id,
        )

        if recommendation is None:
            raise LookupError(
                "Recommendation not found."
            )

        if (
            recommendation.prediction_id
            != payload.prediction_id
        ):
            raise ValueError(
                "The recommendation does not belong "
                "to the specified prediction."
            )

    if payload.corrected_category_id is not None:
        category = db.get(
            WasteCategory,
            payload.corrected_category_id,
        )

        if category is None:
            raise LookupError(
                "Corrected waste category not found."
            )

    feedback = Feedback(
        user_id=None,
        prediction_id=payload.prediction_id,
        recommendation_id=(
            payload.recommendation_id
        ),
        corrected_category_id=(
            payload.corrected_category_id
        ),
        rating=payload.rating,
        was_prediction_correct=(
            payload.was_prediction_correct
        ),
        comments=payload.comments,
    )

    try:
        db.add(feedback)
        db.commit()
        db.refresh(feedback)

    except Exception:
        db.rollback()
        raise

    return feedback
