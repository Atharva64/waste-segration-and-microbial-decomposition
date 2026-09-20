from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


class PredictionHistoryItem(BaseModel):
    id: int
    filename: str | None = None
    predicted_class: str
    confidence: float = Field(ge=0.0, le=1.0)
    probabilities: dict[str, float] | None = None
    model_name: str
    model_version: str | None = None
    created_at: datetime


class FeedbackCreate(BaseModel):
    prediction_id: int = Field(gt=0)
    recommendation_id: int | None = Field(default=None, gt=0)
    corrected_category_id: int | None = Field(default=None, gt=0)
    rating: int | None = Field(default=None, ge=1, le=5)
    was_prediction_correct: bool | None = None
    comments: str | None = Field(default=None, max_length=2000)

    @field_validator("comments")
    @classmethod
    def clean_comments(cls, value: str | None):
        if value is None:
            return None
        value = value.strip()
        return value or None

    @model_validator(mode="after")
    def validate_correction(self):
        if (
            self.was_prediction_correct is True
            and self.corrected_category_id is not None
        ):
            raise ValueError(
                "corrected_category_id must not be provided "
                "when was_prediction_correct is true."
            )
        return self


class FeedbackResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    prediction_id: int
    recommendation_id: int | None = None
    corrected_category_id: int | None = None
    rating: int | None = None
    was_prediction_correct: bool | None = None
    comments: str | None = None
    created_at: datetime
