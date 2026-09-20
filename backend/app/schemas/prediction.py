from pydantic import BaseModel, Field


class PredictionResponse(BaseModel):
    filename: str

    predicted_class: str

    confidence: float = Field(
        ge=0.0,
        le=1.0,
    )

    probabilities: dict[str, float]

    model_name: str
