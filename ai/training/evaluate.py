from pathlib import Path
import json

import numpy as np
import tensorflow as tf

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report
)

from preprocessing import create_datasets


# ============================================================
# Configuration
# ============================================================

MODEL_PATH = Path(
    "ai/models/waste_classifier_best.keras"
)

CLASS_NAMES_PATH = Path(
    "ai/models/class_names.json"
)

REPORT_DIR = Path(
    "docs/report"
)

REPORT_PATH = REPORT_DIR / "evaluation_report.txt"


# ============================================================
# Load Class Names
# ============================================================

def load_class_names():

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
# Load Model
# ============================================================

def load_model():

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
# Get Predictions
# ============================================================

def get_predictions(
    model,
    test_dataset
):

    true_labels = []
    predicted_labels = []

    print("\nRunning predictions on test dataset...")

    for images, labels in test_dataset:

        predictions = model.predict(
            images,
            verbose=0
        )

        predicted_classes = np.argmax(
            predictions,
            axis=1
        )

        true_labels.extend(
            labels.numpy()
        )

        predicted_labels.extend(
            predicted_classes
        )

    return (
        np.array(true_labels),
        np.array(predicted_labels)
    )


# ============================================================
# Calculate Metrics
# ============================================================

def calculate_metrics(
    true_labels,
    predicted_labels,
    class_names
):

    accuracy = accuracy_score(
        true_labels,
        predicted_labels
    )

    precision = precision_score(
        true_labels,
        predicted_labels,
        average="weighted",
        zero_division=0
    )

    recall = recall_score(
        true_labels,
        predicted_labels,
        average="weighted",
        zero_division=0
    )

    f1 = f1_score(
        true_labels,
        predicted_labels,
        average="weighted",
        zero_division=0
    )

    report = classification_report(
        true_labels,
        predicted_labels,
        target_names=class_names,
        digits=4,
        zero_division=0
    )

    return {
        "accuracy": accuracy,
        "precision": precision,
        "recall": recall,
        "f1": f1,
        "report": report
    }


# ============================================================
# Display Results
# ============================================================

def display_results(metrics):

    print("\n" + "=" * 70)
    print("MODEL EVALUATION RESULTS")
    print("=" * 70)

    print(
        f"\nAccuracy  : "
        f"{metrics['accuracy'] * 100:.2f}%"
    )

    print(
        f"Precision : "
        f"{metrics['precision'] * 100:.2f}%"
    )

    print(
        f"Recall    : "
        f"{metrics['recall'] * 100:.2f}%"
    )

    print(
        f"F1 Score  : "
        f"{metrics['f1'] * 100:.2f}%"
    )

    print("\n" + "=" * 70)
    print("PER-CLASS CLASSIFICATION REPORT")
    print("=" * 70)

    print(
        metrics["report"]
    )


# ============================================================
# Save Report
# ============================================================

def save_report(metrics):

    REPORT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(
        REPORT_PATH,
        "w",
        encoding="utf-8"
    ) as file:

        file.write(
            "AI-Based Waste Segregation\n"
        )

        file.write(
            "Model Evaluation Report\n"
        )

        file.write(
            "=" * 70 + "\n\n"
        )

        file.write(
            f"Accuracy  : "
            f"{metrics['accuracy'] * 100:.2f}%\n"
        )

        file.write(
            f"Precision : "
            f"{metrics['precision'] * 100:.2f}%\n"
        )

        file.write(
            f"Recall    : "
            f"{metrics['recall'] * 100:.2f}%\n"
        )

        file.write(
            f"F1 Score  : "
            f"{metrics['f1'] * 100:.2f}%\n\n"
        )

        file.write(
            "Per-Class Classification Report\n"
        )

        file.write(
            "=" * 70 + "\n"
        )

        file.write(
            metrics["report"]
        )

    print(
        f"\nEvaluation report saved to:\n"
        f"{REPORT_PATH}"
    )


# ============================================================
# Main
# ============================================================

def main():

    print("\n" + "=" * 70)
    print("WASTE CLASSIFIER MODEL EVALUATION")
    print("=" * 70)

    # --------------------------------------------------------
    # Load class names
    # --------------------------------------------------------

    class_names = load_class_names()

    print(
        f"\nClasses:\n"
        f"{class_names}"
    )

    # --------------------------------------------------------
    # Load datasets
    # --------------------------------------------------------

    (
        train_dataset,
        validation_dataset,
        test_dataset,
        dataset_class_names
    ) = create_datasets()

    # Safety check
    if class_names != dataset_class_names:

        raise ValueError(
            "Class order mismatch between "
            "class_names.json and test dataset."
        )

    # --------------------------------------------------------
    # Load trained model
    # --------------------------------------------------------

    model = load_model()

    # --------------------------------------------------------
    # Get predictions
    # --------------------------------------------------------

    (
        true_labels,
        predicted_labels
    ) = get_predictions(
        model,
        test_dataset
    )

    # --------------------------------------------------------
    # Calculate metrics
    # --------------------------------------------------------

    metrics = calculate_metrics(
        true_labels,
        predicted_labels,
        class_names
    )

    # --------------------------------------------------------
    # Display results
    # --------------------------------------------------------

    display_results(
        metrics
    )

    # --------------------------------------------------------
    # Save report
    # --------------------------------------------------------

    save_report(
        metrics
    )

    print("\n" + "=" * 70)
    print("MODEL EVALUATION COMPLETED")
    print("=" * 70)


if __name__ == "__main__":
    main()