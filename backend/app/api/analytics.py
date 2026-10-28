from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from backend.app.database.session import get_db
from backend.app.schemas.analytics import AnalyticsSummary
from backend.app.services.analytics_service import (
    get_analytics_summary,
)


router = APIRouter(
    prefix="/api",
    tags=["Analytics"],
)


@router.get(
    "/analytics/summary",
    response_model=AnalyticsSummary,
)
def read_analytics_summary(
    days: int = Query(
        default=7,
        ge=1,
        le=90,
        description="How many recent days to include in scans_per_day.",
    ),
    db: Session = Depends(get_db),
):
    """
    Return dashboard statistics: totals, category counts,
    scans per day, average confidence, and feedback summary.
    """

    return get_analytics_summary(
        db,
        days=days,
    )
