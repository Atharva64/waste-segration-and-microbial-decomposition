from functools import lru_cache
from io import BytesIO
from pathlib import Path
import json

import numpy as np
import tensorflow as tf
from PIL import Image, UnidentifiedImageError


# ============================================================
# Paths / Configuration
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[3]

MODEL_PATH = (
    PROJECT_ROOT
    / "ai"
    / "models"
    / "waste_classifier_best.keras"
)

CLASS_NAMES_PATH = (
    PROJECT_ROOT
    / "ai"
    / "models"
    / "class_names.json"
)

IMAGE_SIZE = (224, 224)


# ============================================================
# Load Class Names
# ============================================================

@lru_cache(maxsize=1)
def load_class_names() -> tuple[str, ...]:
    if not CLASS_NAMES_PATH.exists():
        raise FileNotFoundError(
            f"Class names file not found: {CLASS_NAMES_PATH}"
        )

    with open(
        CLASS_NAMES_PATH,
        "r",
        encoding="utf-8",
    ) as file:
        class_names = json.load(file)

    if not isinstance(class_names, list) or not class_names:
        raise ValueError(
            "class_names.json must contain a non-empty JSON list."
        )

    return tuple(class_names)


# ============================================================
# Load Trained Model
# ============================================================

@lru_cache(maxsize=1)
def load_model():
    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            f"Model file not found: {MODEL_PATH}"
        )

    model = tf.keras.models.load_model(
        MODEL_PATH,
        compile=False,
    )

    class_names = load_class_names()

    if model.output_shape[-1] != len(class_names):
        raise ValueError(
            "Model output size does not match class_names.json."
        )

    return model


# ============================================================
# Image Preprocessing
# ============================================================

def preprocess_image(image_bytes: bytes) -> tf.Tensor:
    """
    Decode an uploaded image and apply the same preprocessing
    used during training:
        RGB -> 224x224 -> float32 -> [-1, 1]
    """

    try:
        with Image.open(BytesIO(image_bytes)) as image:
            image = image.convert("RGB")
            image = image.resize(
                IMAGE_SIZE,
                resample=Image.Resampling.BILINEAR,
            )
            image_array = np.asarray(
                image,
                dtype=np.float32,
            )

    except UnidentifiedImageError as exc:
        raise ValueError(
            "Uploaded file is not a valid image."
        ) from exc

    except OSError as exc:
        raise ValueError(
            "Could not decode the uploaded image."
        ) from exc

    image_array = (
        image_array / 127.5
    ) - 1.0

    image_tensor = tf.convert_to_tensor(
        image_array,
        dtype=tf.float32,
    )

    image_tensor = tf.expand_dims(
        image_tensor,
        axis=0,
    )

    return image_tensor


# ============================================================
# Prediction
# ============================================================

def predict_image_bytes(image_bytes: bytes) -> dict:
    model = load_model()
    class_names = load_class_names()

    image_tensor = preprocess_image(
        image_bytes
    )

    predictions = model.predict(
        image_tensor,
        verbose=0,
    )[0]

    predicted_index = int(
        np.argmax(predictions)
    )

    predicted_class = class_names[
        predicted_index
    ]

    confidence = float(
        predictions[predicted_index]
    )

    probabilities = {
        class_name: float(probability)
        for class_name, probability in zip(
            class_names,
            predictions,
        )
    }

    return {
        "predicted_class": predicted_class,
        "confidence": confidence,
        "probabilities": probabilities,
        "model_name": "MobileNetV3Small",
    }
