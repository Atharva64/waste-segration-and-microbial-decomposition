from pathlib import Path
import argparse
import json

import numpy as np
import tensorflow as tf


# ============================================================
# Configuration
# ============================================================

IMAGE_SIZE = (224, 224)

MODEL_PATH = Path(
    "ai/models/waste_classifier_best.keras"
)

CLASS_NAMES_PATH = Path(
    "ai/models/class_names.json"
)


# ============================================================
# Load Class Names
# ============================================================

def load_class_names():
    """
    Load class names generated during training.
    """

    if not CLASS_NAMES_PATH.exists():
        raise FileNotFoundError(
            f"Class names file not found:\n"
            f"{CLASS_NAMES_PATH.resolve()}"
        )

    with open(
        CLASS_NAMES_PATH,
        "r",
        encoding="utf-8"
    ) as file:
        class_names = json.load(file)

    return class_names


# ============================================================
# Load Trained Model
# ============================================================

def load_trained_model():
    """
    Load the best trained waste classification model.
    """

    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            f"Model not found:\n"
            f"{MODEL_PATH.resolve()}"
        )

    print(
        f"\nLoading model:\n"
        f"{MODEL_PATH}"
    )

    model = tf.keras.models.load_model(
        MODEL_PATH
    )

    print("Model loaded successfully.")

    return model


# ============================================================
# Image Preprocessing
# ============================================================

def preprocess_image(image_path):
    """
    Prepare one image using the same preprocessing
    configuration used during training.
    """

    image_path = Path(image_path)

    if not image_path.exists():
        raise FileNotFoundError(
            f"Image not found:\n"
            f"{image_path.resolve()}"
        )

    # Load image as RGB and resize to 224x224
    image = tf.keras.utils.load_img(
        image_path,
        target_size=IMAGE_SIZE,
        color_mode="rgb"
    )

    # Convert image to array
    image_array = tf.keras.utils.img_to_array(
        image
    )

    # Convert to float32
    image_array = tf.cast(
        image_array,
        tf.float32
    )

    # Normalize:
    # [0, 255] -> [-1, 1]
    image_array = (
        image_array / 127.5
    ) - 1.0

    # Add batch dimension
    # (224, 224, 3)
    # becomes
    # (1, 224, 224, 3)
    image_array = tf.expand_dims(
        image_array,
        axis=0
    )

    return image_array


# ============================================================
# Prediction
# ============================================================

def predict_image(
    model,
    image_path,
    class_names
):
    """
    Predict the waste class for one image.
    """

    image = preprocess_image(
        image_path
    )

    predictions = model.predict(
        image,
        verbose=0
    )

    probabilities = predictions[0]

    predicted_index = int(
        np.argmax(probabilities)
    )

    predicted_class = class_names[
        predicted_index
    ]

    confidence = float(
        probabilities[
            predicted_index
        ]
    )

    return (
        predicted_class,
        confidence,
        probabilities
    )


# ============================================================
# Display Result
# ============================================================

def display_prediction(
    image_path,
    predicted_class,
    confidence,
    probabilities,
    class_names
):

    print("\n" + "=" * 60)
    print("WASTE CLASSIFICATION RESULT")
    print("=" * 60)

    print(
        f"\nImage:\n{image_path}"
    )

    print(
        f"\nPredicted class : "
        f"{predicted_class}"
    )

    print(
        f"Confidence      : "
        f"{confidence * 100:.2f}%"
    )

    print("\nClass probabilities:")

    for class_name, probability in zip(
        class_names,
        probabilities
    ):
        print(
            f"{class_name:<15} "
            f"{probability * 100:>7.2f}%"
        )

    print("=" * 60)


# ============================================================
# Main
# ============================================================

def main():

    parser = argparse.ArgumentParser(
        description=(
            "Predict the waste category "
            "of a single image."
        )
    )

    parser.add_argument(
        "image",
        help="Path to the waste image"
    )

    args = parser.parse_args()

    class_names = load_class_names()

    model = load_trained_model()

    (
        predicted_class,
        confidence,
        probabilities
    ) = predict_image(
        model,
        args.image,
        class_names
    )

    display_prediction(
        args.image,
        predicted_class,
        confidence,
        probabilities,
        class_names
    )


if __name__ == "__main__":
    main()