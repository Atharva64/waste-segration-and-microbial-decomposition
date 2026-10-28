import datetime as dt

from pydantic import BaseModel, Field


class CategoryCount(BaseModel):
    slug: str
    name: str
    count: int = Field(ge=0)


class DailyCount(BaseModel):
    date: dt.date
    count: int = Field(ge=0)


class AnalyticsSummary(BaseModel):
    days: int
    total_predictions: int = Field(ge=0)
    average_confidence: float | None = Field(default=None, ge=0.0, le=1.0)
    top_category: str | None = None
    by_category: list[CategoryCount] = Field(default_factory=list)
    scans_per_day: list[DailyCount] = Field(default_factory=list)
    feedback_total: int = Field(ge=0)
    feedback_correct: int = Field(ge=0)
    feedback_incorrect: int = Field(ge=0)
