from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Query,
    status,
)
from sqlalchemy.orm import Session

from backend.app.database.session import get_db
from backend.app.schemas.history import (
    FeedbackCreate,
    FeedbackResponse,
    PredictionHistoryItem,
)
from backend.app.services.history_service import (
    create_feedback,
    get_prediction_history,
)


router = APIRouter(
    prefix="/api",
    tags=["History & Feedback"],
)


# ============================================================
# GET /api/predictions
# ============================================================

@router.get(
    "/predictions",
    response_model=list[PredictionHistoryItem],
)
def read_prediction_history(
    limit: int = Query(
        default=50,
        ge=1,
        le=100,
    ),
    db: Session = Depends(get_db),
):
    """
    Return prediction history, newest first.

    Authentication is not implemented yet, so this prototype
    endpoint returns all stored predictions.
    """

    return get_prediction_history(
        db,
        limit=limit,
    )


# ============================================================
# POST /api/feedback
# ============================================================

@router.post(
    "/feedback",
    response_model=FeedbackResponse,
    status_code=status.HTTP_201_CREATED,
)
def submit_feedback(
    payload: FeedbackCreate,
    db: Session = Depends(get_db),
):
    """
    Store feedback for an existing prediction.
    """

    try:
        feedback = create_feedback(
            db,
            payload,
        )

    except LookupError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc

    return feedback
