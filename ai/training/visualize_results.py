from pathlib import Path
import csv
import json

import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt

from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay

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

HISTORY_PATH = Path(
    "docs/report/training_history.csv"
)

SCREENSHOT_DIR = Path(
    "docs/screenshots"
)

CONFUSION_MATRIX_PATH = (
    SCREENSHOT_DIR / "confusion_matrix.png"
)

ACCURACY_PLOT_PATH = (
    SCREENSHOT_DIR / "training_accuracy.png"
)

LOSS_PLOT_PATH = (
    SCREENSHOT_DIR / "training_loss.png"
)


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
            f"Model file not found:\n"
            f"{MODEL_PATH.resolve()}"
        )

    print(
        f"\nLoading model:\n"
        f"{MODEL_PATH}"
    )

    model = tf.keras.models.load_model(
        MODEL_PATH
    )

    print(
        "Model loaded successfully."
    )

    return model


# ============================================================
# Read Training History
# ============================================================

def load_training_history():

    if not HISTORY_PATH.exists():

        raise FileNotFoundError(
            f"Training history not found:\n"
            f"{HISTORY_PATH.resolve()}"
        )

    epochs = []
    accuracy = []
    val_accuracy = []
    loss = []
    val_loss = []

    with open(
        HISTORY_PATH,
        "r",
        encoding="utf-8"
    ) as file:

        reader = csv.DictReader(file)

        for row in reader:

            epochs.append(
                int(row["epoch"]) + 1
            )

            accuracy.append(
                float(row["accuracy"])
            )

            val_accuracy.append(
                float(row["val_accuracy"])
            )

            loss.append(
                float(row["loss"])
            )

            val_loss.append(
                float(row["val_loss"])
            )

    return (
        epochs,
        accuracy,
        val_accuracy,
        loss,
        val_loss
    )


# ============================================================
# Training Accuracy Plot
# ============================================================

def plot_accuracy(
    epochs,
    accuracy,
    val_accuracy
):

    print(
        "\nCreating training accuracy graph..."
    )

    plt.figure(
        figsize=(10, 6)
    )

    plt.plot(
        epochs,
        accuracy,
        marker="o",
        label="Training Accuracy"
    )

    plt.plot(
        epochs,
        val_accuracy,
        marker="o",
        label="Validation Accuracy"
    )

    plt.title(
        "Training vs Validation Accuracy"
    )

    plt.xlabel(
        "Epoch"
    )

    plt.ylabel(
        "Accuracy"
    )

    plt.grid(
        alpha=0.3
    )

    plt.legend()

    plt.tight_layout()

    plt.savefig(
        ACCURACY_PLOT_PATH,
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()

    print(
        f"Saved:\n{ACCURACY_PLOT_PATH}"
    )


# ============================================================
# Training Loss Plot
# ============================================================

def plot_loss(
    epochs,
    loss,
    val_loss
):

    print(
        "\nCreating training loss graph..."
    )

    plt.figure(
        figsize=(10, 6)
    )

    plt.plot(
        epochs,
        loss,
        marker="o",
        label="Training Loss"
    )

    plt.plot(
        epochs,
        val_loss,
        marker="o",
        label="Validation Loss"
    )

    plt.title(
        "Training vs Validation Loss"
    )

    plt.xlabel(
        "Epoch"
    )

    plt.ylabel(
        "Loss"
    )

    plt.grid(
        alpha=0.3
    )

    plt.legend()

    plt.tight_layout()

    plt.savefig(
        LOSS_PLOT_PATH,
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()

    print(
        f"Saved:\n{LOSS_PLOT_PATH}"
    )


# ============================================================
# Test Predictions
# ============================================================

def get_test_predictions(
    model,
    test_dataset
):

    true_labels = []
    predicted_labels = []

    print(
        "\nGenerating predictions "
        "for confusion matrix..."
    )

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
# Confusion Matrix
# ============================================================

def plot_confusion_matrix(
    true_labels,
    predicted_labels,
    class_names
):

    print(
        "\nCreating confusion matrix..."
    )

    matrix = confusion_matrix(
        true_labels,
        predicted_labels,
        labels=range(
            len(class_names)
        )
    )

    figure, axis = plt.subplots(
        figsize=(10, 8)
    )

    display = ConfusionMatrixDisplay(
        confusion_matrix=matrix,
        display_labels=class_names
    )

    display.plot(
        ax=axis,
        values_format="d",
        xticks_rotation=45
    )

    axis.set_title(
        "Waste Classification Confusion Matrix"
    )

    figure.tight_layout()

    figure.savefig(
        CONFUSION_MATRIX_PATH,
        dpi=300,
        bbox_inches="tight"
    )

    plt.close(
        figure
    )

    print(
        f"Saved:\n{CONFUSION_MATRIX_PATH}"
    )


# ============================================================
# Main
# ============================================================

def main():

    print(
        "\n" + "=" * 70
    )

    print(
        "WASTE CLASSIFIER VISUALIZATION"
    )

    print(
        "=" * 70
    )

    # --------------------------------------------------------
    # Create screenshot directory
    # --------------------------------------------------------

    SCREENSHOT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    # --------------------------------------------------------
    # Load class names
    # --------------------------------------------------------

    class_names = load_class_names()

    print(
        f"\nClasses:\n"
        f"{class_names}"
    )

    # --------------------------------------------------------
    # Training history
    # --------------------------------------------------------

    (
        epochs,
        accuracy,
        val_accuracy,
        loss,
        val_loss
    ) = load_training_history()

    # --------------------------------------------------------
    # Accuracy graph
    # --------------------------------------------------------

    plot_accuracy(
        epochs,
        accuracy,
        val_accuracy
    )

    # --------------------------------------------------------
    # Loss graph
    # --------------------------------------------------------

    plot_loss(
        epochs,
        loss,
        val_loss
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

    # --------------------------------------------------------
    # Verify class order
    # --------------------------------------------------------

    if class_names != dataset_class_names:

        raise ValueError(
            "Class order mismatch between "
            "class_names.json and dataset."
        )

    # --------------------------------------------------------
    # Load trained model
    # --------------------------------------------------------

    model = load_model()

    # --------------------------------------------------------
    # Test predictions
    # --------------------------------------------------------

    (
        true_labels,
        predicted_labels
    ) = get_test_predictions(
        model,
        test_dataset
    )

    # --------------------------------------------------------
    # Confusion matrix
    # --------------------------------------------------------

    plot_confusion_matrix(
        true_labels,
        predicted_labels,
        class_names
    )

    print(
        "\n" + "=" * 70
    )

    print(
        "VISUALIZATION COMPLETED"
    )

    print(
        "=" * 70
    )

    print(
        "\nGenerated files:"
    )

    print(
        f"1. {ACCURACY_PLOT_PATH}"
    )

    print(
        f"2. {LOSS_PLOT_PATH}"
    )

    print(
        f"3. {CONFUSION_MATRIX_PATH}"
    )


if __name__ == "__main__":
    main()