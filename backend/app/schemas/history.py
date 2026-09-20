from datetime import datetime

from pydantic import BaseModel, Field


# ============================================================
# Prediction History
# ============================================================

class PredictionHistoryItem(BaseModel):
    id: int
    filename: str | None = None
    predicted_class: str
    confidence: float = Field(
        ge=0.0,
        le=1.0,
    )
    probabilities: dict[str, float] | None = None
    model_name: str
    model_version: str | None = None
    created_at: datetime


# ============================================================
# Feedback
# ============================================================

class FeedbackCreate(BaseModel):
    prediction_id: int = Field(
        gt=0,
    )

    recommendation_id: int | None = Field(
        default=None,
        gt=0,
    )

    corrected_category_id: int | None = Field(
        default=None,
        gt=0,
    )

    rating: int | None = Field(
        default=None,
        ge=1,
        le=5,
    )

    was_prediction_correct: bool | None = None

    comments: str | None = Field(
        default=None,
        max_length=2000,
    )


class FeedbackResponse(BaseModel):
    id: int
    prediction_id: int
    recommendation_id: int | None = None
    corrected_category_id: int | None = None
    rating: int | None = None
    was_prediction_correct: bool | None = None
    comments: str | None = None
    created_at: datetime
