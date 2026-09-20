from fastapi import (
    APIRouter,
    Depends,
    File,
    HTTPException,
    UploadFile,
    status,
)
from sqlalchemy.orm import Session

from backend.app.database.session import get_db
from backend.app.schemas.prediction import (
    PredictionResponse,
)
from backend.app.services.history_service import (
    save_prediction,
)
from backend.app.services.prediction_service import (
    predict_image_bytes,
)


router = APIRouter(
    prefix="/api",
    tags=["Prediction"],
)


ALLOWED_CONTENT_TYPES = {
    "image/jpeg",
    "image/png",
    "image/webp",
    "image/bmp",
}

MAX_FILE_SIZE = 10 * 1024 * 1024


@router.post(
    "/predict",
    response_model=PredictionResponse,
    status_code=status.HTTP_200_OK,
)
async def predict_waste(
    image: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    """
    Upload one waste image, run the trained model,
    save the result, and return prediction JSON.
    """

    if image.content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail=(
                "Unsupported image type. "
                "Use JPEG, PNG, WEBP, or BMP."
            ),
        )

    image_bytes = await image.read()

    if not image_bytes:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Uploaded image is empty.",
        )

    if len(image_bytes) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail="Image must be 10 MB or smaller.",
        )

    try:
        result = predict_image_bytes(
            image_bytes
        )

        prediction = save_prediction(
            db,
            filename=(
                image.filename
                or "uploaded-image"
            ),
            prediction_result=result,
        )

    except FileNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(exc),
        ) from exc

    except RuntimeError as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(exc),
        ) from exc

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc

    return PredictionResponse(
        prediction_id=prediction.id,
        filename=(
            image.filename
            or "uploaded-image"
        ),
        **result,
    )
