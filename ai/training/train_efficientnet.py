import json
from pathlib import Path

import tensorflow as tf
from tensorflow.keras import layers, Model

from preprocessing import create_datasets


# ============================================================
# Configuration
# ============================================================

INPUT_SHAPE = (224, 224, 3)

LEARNING_RATE = 0.001
DROPOUT_RATE = 0.2
EPOCHS = 15

MODEL_DIR = Path("ai/models")
LOG_DIR = Path("docs/report")

BEST_MODEL_PATH = (
    MODEL_DIR / "efficientnetv2b0_best.keras"
)

FINAL_MODEL_PATH = (
    MODEL_DIR / "efficientnetv2b0_final.keras"
)

HISTORY_PATH = (
    LOG_DIR / "efficientnet_training_history.csv"
)

CLASS_NAMES_PATH = (
    MODEL_DIR / "class_names.json"
)


# ============================================================
# Callbacks
# ============================================================

def create_callbacks():

    MODEL_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    LOG_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    return [
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


# ============================================================
# Build EfficientNetV2B0
# ============================================================

def build_model(num_classes):

    print("\n" + "=" * 70)
    print("BUILDING EFFICIENTNETV2B0 MODEL")
    print("=" * 70)

    base_model = tf.keras.applications.EfficientNetV2B0(
        input_shape=INPUT_SHAPE,
        include_top=False,
        weights="imagenet",

        # Our preprocessing.py already converts
        # [0,255] -> [-1,1]
        include_preprocessing=False
    )

    base_model.trainable = False

    inputs = layers.Input(
        shape=INPUT_SHAPE,
        name="input_image"
    )

    x = base_model(
        inputs,
        training=False
    )

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

    model = Model(
        inputs=inputs,
        outputs=outputs,
        name="waste_classifier_efficientnetv2b0"
    )

    return model, base_model


# ============================================================
# Compile
# ============================================================

def compile_model(model):

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
# Train
# ============================================================

def train_model(
    model,
    train_dataset,
    validation_dataset
):

    print("\n" + "=" * 70)
    print("STARTING EFFICIENTNETV2B0 TRAINING")
    print("=" * 70)

    history = model.fit(
        train_dataset,
        validation_data=validation_dataset,
        epochs=EPOCHS,
        callbacks=create_callbacks()
    )

    return history


# ============================================================
# Main
# ============================================================

def main():

    print("\n" + "=" * 70)
    print("EFFICIENTNETV2B0 WASTE CLASSIFIER")
    print("=" * 70)

    (
        train_dataset,
        validation_dataset,
        test_dataset,
        class_names
    ) = create_datasets()

    # Save class names if required
    MODEL_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(
        CLASS_NAMES_PATH,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            class_names,
            file,
            indent=4
        )

    model, base_model = build_model(
        len(class_names)
    )

    model = compile_model(
        model
    )

    print(
        f"\nBase model trainable: "
        f"{base_model.trainable}"
    )

    print(
        f"Number of classes: "
        f"{len(class_names)}"
    )

    print("\nClass mapping:")

    for index, class_name in enumerate(
        class_names
    ):
        print(
            f"{index} -> {class_name}"
        )

    model.summary()

    # Train
    train_model(
        model,
        train_dataset,
        validation_dataset
    )

    # Save final model
    model.save(
        FINAL_MODEL_PATH
    )

    print("\n" + "=" * 70)
    print("TRAINING COMPLETED")
    print("=" * 70)

    print(
        f"\nBest model:\n"
        f"{BEST_MODEL_PATH}"
    )

    print(
        f"\nFinal model:\n"
        f"{FINAL_MODEL_PATH}"
    )

    print(
        f"\nTraining history:\n"
        f"{HISTORY_PATH}"
    )


if __name__ == "__main__":
    main()
    