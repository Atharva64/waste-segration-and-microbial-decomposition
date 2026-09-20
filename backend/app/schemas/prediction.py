from pydantic import BaseModel, Field


class PredictionResponse(BaseModel):
    prediction_id: int

    filename: str

    predicted_class: str

    confidence: float = Field(
        ge=0.0,
        le=1.0,
    )

    probabilities: dict[str, float]

    model_name: str
