from pathlib import Path
import json
import time

import numpy as np
import tensorflow as tf

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score
)

from preprocessing import create_datasets


# ============================================================
# Configuration
# ============================================================

MOBILENET_PATH = Path(
    "ai/models/waste_classifier_best.keras"
)

EFFICIENTNET_PATH = Path(
    "ai/models/efficientnetv2b0_best.keras"
)

CLASS_NAMES_PATH = Path(
    "ai/models/class_names.json"
)

REPORT_PATH = Path(
    "docs/report/model_comparison.md"
)


# ============================================================
# Evaluate One Model
# ============================================================

def evaluate_model(
    name,
    model_path,
    test_dataset
):

    print(
        f"\nEvaluating {name}..."
    )

    model = tf.keras.models.load_model(
        model_path
    )

    true_labels = []
    predicted_labels = []

    start_time = time.perf_counter()

    for images, labels in test_dataset:

        predictions = model.predict(
            images,
            verbose=0
        )

        predicted = np.argmax(
            predictions,
            axis=1
        )

        true_labels.extend(
            labels.numpy()
        )

        predicted_labels.extend(
            predicted
        )

    elapsed = time.perf_counter() - start_time

    true_labels = np.array(
        true_labels
    )

    predicted_labels = np.array(
        predicted_labels
    )

    image_count = len(
        true_labels
    )

    inference_ms = (
        elapsed / image_count
    ) * 1000

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

    model_size_mb = (
        model_path.stat().st_size
        / (1024 * 1024)
    )

    return {
        "name": name,
        "accuracy": accuracy,
        "precision": precision,
        "recall": recall,
        "f1": f1,
        "inference_ms": inference_ms,
        "size_mb": model_size_mb
    }


# ============================================================
# Generate Markdown Report
# ============================================================

def save_report(
    mobilenet,
    efficientnet
):

    REPORT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    report = f"""# Model Comparison

## MobileNetV3Small vs EfficientNetV2B0

Both models were evaluated using the same test dataset and preprocessing
pipeline.

| Metric | MobileNetV3Small | EfficientNetV2B0 |
|---|---:|---:|
| Accuracy | {mobilenet["accuracy"] * 100:.2f}% | {efficientnet["accuracy"] * 100:.2f}% |
| Precision | {mobilenet["precision"] * 100:.2f}% | {efficientnet["precision"] * 100:.2f}% |
| Recall | {mobilenet["recall"] * 100:.2f}% | {efficientnet["recall"] * 100:.2f}% |
| F1 Score | {mobilenet["f1"] * 100:.2f}% | {efficientnet["f1"] * 100:.2f}% |
| Approx. inference time / image | {mobilenet["inference_ms"]:.2f} ms | {efficientnet["inference_ms"]:.2f} ms |
| Saved model size | {mobilenet["size_mb"]:.2f} MB | {efficientnet["size_mb"]:.2f} MB |

## Experimental Conditions

Both models used:

- The same six waste classes
- The same train/validation/test dataset split
- 224 × 224 RGB images
- The same normalization pipeline
- The same training augmentation
- ImageNet pretrained weights
- Frozen feature-extraction base
- Adam optimizer
- Sparse categorical cross-entropy loss
- Early stopping
- Learning-rate reduction
- Best validation checkpoint for final evaluation

## Interpretation

The two architectures should be compared using multiple factors rather than
accuracy alone.

Important considerations include:

- Test accuracy
- Precision
- Recall
- F1-score
- Inference speed
- Saved model size
- Future deployment requirements

MobileNetV3Small is designed as a lightweight architecture, while
EfficientNetV2B0 provides a different accuracy/efficiency trade-off.

The measured results above should be used when deciding which architecture
is more appropriate for later deployment in this project.
"""

    REPORT_PATH.write_text(
        report,
        encoding="utf-8"
    )

    print(
        f"\nComparison report saved to:\n"
        f"{REPORT_PATH}"
    )


# ============================================================
# Main
# ============================================================

def main():

    if not MOBILENET_PATH.exists():
        raise FileNotFoundError(
            MOBILENET_PATH
        )

    if not EFFICIENTNET_PATH.exists():
        raise FileNotFoundError(
            EFFICIENTNET_PATH
        )

    with open(
        CLASS_NAMES_PATH,
        "r",
        encoding="utf-8"
    ) as file:
        saved_classes = json.load(file)

    (
        train_dataset,
        validation_dataset,
        test_dataset,
        dataset_classes
    ) = create_datasets()

    if saved_classes != dataset_classes:

        raise ValueError(
            "Dataset class order does not match "
            "class_names.json."
        )

    mobilenet = evaluate_model(
        "MobileNetV3Small",
        MOBILENET_PATH,
        test_dataset
    )

    efficientnet = evaluate_model(
        "EfficientNetV2B0",
        EFFICIENTNET_PATH,
        test_dataset
    )

    print("\n" + "=" * 70)
    print("MODEL COMPARISON")
    print("=" * 70)

    print(
        f"\nMobileNetV3Small accuracy: "
        f"{mobilenet['accuracy'] * 100:.2f}%"
    )

    print(
        f"EfficientNetV2B0 accuracy: "
        f"{efficientnet['accuracy'] * 100:.2f}%"
    )

    save_report(
        mobilenet,
        efficientnet
    )


if __name__ == "__main__":
    main()