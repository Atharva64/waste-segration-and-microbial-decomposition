from pathlib import Path
import tensorflow as tf
from tensorflow.keras import layers, Model

from preprocessing import create_datasets


# ============================================================
# Configuration
# ============================================================

IMAGE_SIZE = (224, 224)
INPUT_SHAPE = (224, 224, 3)

LEARNING_RATE = 0.001
DROPOUT_RATE = 0.2

EPOCHS = 15

MODEL_DIR = Path("ai/models")
LOG_DIR = Path("docs/report")

BEST_MODEL_PATH = MODEL_DIR / "waste_classifier_best.keras"
FINAL_MODEL_PATH = MODEL_DIR / "waste_classifier_final.keras"
HISTORY_PATH = LOG_DIR / "training_history.csv"


# ============================================================
# Build MobileNetV3Small Transfer Learning Model
# ============================================================

def create_callbacks(): 
    """
    Create callbacks for checkpointing and early stopping.
    """

    MODEL_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    LOG_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    callbacks = [
        tf.keras.callbacks.ModelCheckpoint(
            filepath=BEST_MODEL_PATH,
            monitor="val_accuracy",
            save_best_only=True,
            mode="max",
            verbose=1
        ),

        tf.keras.callbacks.EarlyStopping(
            monitor="val_loss",
            patience=4,
            restore_best_weights=True,
            verbose=1
        ),

        tf.keras.callbacks.ReduceLROnPlateau(
            monitor="val_loss",
            factor=0.5,
            patience=2,
            min_lr=1e-6,
            verbose=1
        ),

        tf.keras.callbacks.CSVLogger(
            HISTORY_PATH
        )
    ]

    return callbacks

def train_model(
    model,
    train_dataset,
    validation_dataset
):
    """
    Train the classification head while MobileNetV3Small
    remains frozen.
    """

    print("\n" + "=" * 70)
    print("STARTING MODEL TRAINING")
    print("=" * 70)

    callbacks = create_callbacks()

    history = model.fit(
        train_dataset,
        validation_data=validation_dataset,
        epochs=EPOCHS,
        callbacks=callbacks
    )

    return history

def build_model(num_classes):
    """
    Build a MobileNetV3Small transfer-learning model.

    The ImageNet-trained base model is frozen.
    A new classification head is added for the project's
    six waste categories.
    """

    print("\n" + "=" * 70)
    print("BUILDING MOBILENETV3SMALL MODEL")
    print("=" * 70)

    # --------------------------------------------------------
    # Pre-trained base model
    # --------------------------------------------------------

    base_model = tf.keras.applications.MobileNetV3Small(
        input_shape=INPUT_SHAPE,

        # Remove original ImageNet classifier
        include_top=False,

        # Use ImageNet-trained weights
        weights="imagenet",

        # Images are already normalized to [-1, 1]
        # by preprocessing.py
        include_preprocessing=False
    )

    # Freeze all MobileNetV3 layers
    base_model.trainable = False

    # --------------------------------------------------------
    # Input Layer
    # --------------------------------------------------------

    inputs = layers.Input(
        shape=INPUT_SHAPE,
        name="input_image"
    )

    # --------------------------------------------------------
    # MobileNetV3 Feature Extraction
    # --------------------------------------------------------

    x = base_model(
        inputs,
        training=False
    )

    # --------------------------------------------------------
    # Classification Head
    # --------------------------------------------------------

    x = layers.GlobalAveragePooling2D(
        name="global_average_pooling"
    )(x)

    x = layers.Dropout(
        DROPOUT_RATE,
        name="dropout"
    )(x)

    outputs = layers.Dense(
        num_classes,
        activation="softmax",
        name="waste_classification"
    )(x)

    # --------------------------------------------------------
    # Final Model
    # --------------------------------------------------------

    model = Model(
        inputs=inputs,
        outputs=outputs,
        name="waste_classifier_mobilenetv3small"
    )

    return model, base_model


# ============================================================
# Compile Model
# ============================================================

def compile_model(model):
    """
    Compile the model for multi-class classification.
    """

    model.compile(
        optimizer=tf.keras.optimizers.Adam(
            learning_rate=LEARNING_RATE
        ),

        loss=tf.keras.losses.SparseCategoricalCrossentropy(),

        metrics=[
            "accuracy"
        ]
    )

    return model


# ============================================================
# Display Model Information
# ============================================================

def display_model_info(
    model,
    base_model,
    class_names
):
    """
    Display model configuration and class information.
    """

    print("\n" + "=" * 70)
    print("MODEL INFORMATION")
    print("=" * 70)

    print(
        f"\nNumber of classes: "
        f"{len(class_names)}"
    )

    print("\nClass mapping:")

    for index, class_name in enumerate(class_names):

        print(
            f"{index} -> {class_name}"
        )

    print(
        f"\nBase model trainable: "
        f"{base_model.trainable}"
    )

    print(
        f"Input shape: "
        f"{INPUT_SHAPE}"
    )

    print(
        f"Learning rate: "
        f"{LEARNING_RATE}"
    )

    print(
        f"Dropout rate: "
        f"{DROPOUT_RATE}"
    )

    print("\nModel Summary:\n")

    model.summary()


# ============================================================
# Test Forward Pass
# ============================================================

def test_model(
    model,
    train_dataset
):
    """
    Pass one batch through the model to verify that
    input and output dimensions are correct.
    """

    print("\n" + "=" * 70)
    print("MODEL FORWARD-PASS TEST")
    print("=" * 70)

    for images, labels in train_dataset.take(1):

        predictions = model(
            images,
            training=False
        )

        print(
            f"\nInput batch shape: "
            f"{images.shape}"
        )

        print(
            f"Label batch shape: "
            f"{labels.shape}"
        )

        print(
            f"Prediction shape: "
            f"{predictions.shape}"
        )

        print(
            "\nExample prediction probabilities:"
        )

        print(
            predictions[0].numpy()
        )

        print(
            "\nProbability sum:"
        )

        print(
            float(
                tf.reduce_sum(
                    predictions[0]
                ).numpy()
            )
        )


# ============================================================
# Main
# ============================================================

def main():

    print("\n" + "=" * 70)
    print("AI-BASED WASTE SEGREGATION CLASSIFICATION SYSTEM")
    print("=" * 70)

    # --------------------------------------------------------
    # 1. Load datasets
    # --------------------------------------------------------

    (
        train_dataset,
        validation_dataset,
        test_dataset,
        class_names
    ) = create_datasets()

    # --------------------------------------------------------
    # 2. Build MobileNetV3Small model
    # --------------------------------------------------------

    model, base_model = build_model(
        num_classes=len(class_names)
    )

    # --------------------------------------------------------
    # 3. Compile model
    # --------------------------------------------------------

    model = compile_model(
        model
    )

    # --------------------------------------------------------
    # 4. Display model information
    # --------------------------------------------------------

    display_model_info(
        model,
        base_model,
        class_names
    )

    # --------------------------------------------------------
    # 5. Test forward pass
    # --------------------------------------------------------

    test_model(
        model,
        train_dataset
    )

    # --------------------------------------------------------
    # 6. Train model
    # --------------------------------------------------------

    history = train_model(
        model,
        train_dataset,
        validation_dataset
    )

    # --------------------------------------------------------
    # 7. Create model folder
    # --------------------------------------------------------

    MODEL_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    # --------------------------------------------------------
    # 8. Save final trained model
    # --------------------------------------------------------

    model.save(
        FINAL_MODEL_PATH
    )

    # --------------------------------------------------------
    # 9. Print saved file locations
    # --------------------------------------------------------

    print("\n" + "=" * 70)
    print("TRAINING COMPLETED")
    print("=" * 70)

    print(
        f"\nFinal model saved to:\n"
        f"{FINAL_MODEL_PATH}"
    )

    print(
        f"\nBest checkpoint saved to:\n"
        f"{BEST_MODEL_PATH}"
    )

    print(
        f"\nTraining history saved to:\n"
        f"{HISTORY_PATH}"
    )

    print("\nModel training successfully completed.")


if __name__ == "__main__":
    main()