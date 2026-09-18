from pathlib import Path
from augmentation import apply_augmentation
import tensorflow as tf


# ============================================================
# Configuration
# ============================================================

IMAGE_SIZE = (224, 224)
BATCH_SIZE = 32
RANDOM_SEED = 42

PROCESSED_DIR = Path("data/processed")

TRAIN_DIR = PROCESSED_DIR / "train"
VALIDATION_DIR = PROCESSED_DIR / "validation"
TEST_DIR = PROCESSED_DIR / "test"


# ============================================================
# Image Preprocessing
# ============================================================

def normalize_images(images, labels):
    """
    Convert image pixels from [0, 255] to [-1, 1].

    This normalization is suitable for our planned
    MobileNetV3Small configuration with internal
    preprocessing disabled.
    """

    images = tf.cast(images, tf.float32)

    images = (images / 127.5) - 1.0

    return images, labels


# ============================================================
# Dataset Loader
# ============================================================

def load_dataset(
    directory,
    shuffle=False
):
    """
    Load an image dataset from a directory.

    Expected structure:

    directory/
        biodegradable/
        plastic/
        paper/
        glass/
        metal/
        e-waste/
    """

    directory = Path(directory)

    if not directory.exists():
        raise FileNotFoundError(
            f"Dataset directory not found: "
            f"{directory.resolve()}"
        )

    dataset = tf.keras.utils.image_dataset_from_directory(
        directory,
        labels="inferred",
        label_mode="int",

        # Force all images to RGB
        color_mode="rgb",

        # Resize automatically
        image_size=IMAGE_SIZE,

        batch_size=BATCH_SIZE,

        shuffle=shuffle,

        seed=RANDOM_SEED
        if shuffle
        else None
    )

    return dataset


# ============================================================
# Optimize TensorFlow Pipeline
# ============================================================

def optimize_dataset(
    dataset,
    training=False
):
    """
    Apply normalization and performance optimizations.
    """

    dataset = dataset.map(
        normalize_images,
        num_parallel_calls=tf.data.AUTOTUNE
    )

    if training:

        # Shuffle batches during training
        dataset = dataset.shuffle(
            buffer_size=1000,
            seed=RANDOM_SEED
        )

    dataset = dataset.prefetch(
        buffer_size=tf.data.AUTOTUNE
    )

    return dataset


# ============================================================
# Load All Dataset Splits
# ============================================================

def create_datasets():
    """
    Create train, validation, and test TensorFlow datasets.
    """

    print("\n" + "=" * 60)
    print("LOADING TRAINING DATASET")
    print("=" * 60)

    train_dataset = load_dataset(
        TRAIN_DIR,
        shuffle=True
    )

    class_names = train_dataset.class_names

    print(
        f"\nClasses detected: {class_names}"
    )

    print("\n" + "=" * 60)
    print("LOADING VALIDATION DATASET")
    print("=" * 60)

    validation_dataset = load_dataset(
        VALIDATION_DIR,
        shuffle=False
    )

    print("\n" + "=" * 60)
    print("LOADING TEST DATASET")
    print("=" * 60)

    test_dataset = load_dataset(
        TEST_DIR,
        shuffle=False
    )

    # Apply normalization
    train_dataset = optimize_dataset(
        train_dataset,
        training=True
    ) 
    train_dataset = apply_augmentation(train_dataset)

    validation_dataset = optimize_dataset(
        validation_dataset)

    test_dataset = optimize_dataset(
        test_dataset)
    

    return (
        train_dataset,
        validation_dataset,
        test_dataset,
        class_names
    )


# ============================================================
# Pipeline Test
# ============================================================

def test_pipeline():

    (
        train_dataset,
        validation_dataset,
        test_dataset,
        class_names
    ) = create_datasets()

    print("\n" + "=" * 60)
    print("PREPROCESSING PIPELINE TEST")
    print("=" * 60)

    print(
        f"\nNumber of classes: "
        f"{len(class_names)}"
    )

    print(
        f"Classes: "
        f"{class_names}"
    )

    # Inspect one batch
    for images, labels in train_dataset.take(1):

        print(
            f"\nImage batch shape: "
            f"{images.shape}"
        )

        print(
            f"Label batch shape: "
            f"{labels.shape}"
        )

        print(
            f"Image data type: "
            f"{images.dtype}"
        )

        print(
            f"Minimum pixel value: "
            f"{tf.reduce_min(images).numpy():.3f}"
        )

        print(
            f"Maximum pixel value: "
            f"{tf.reduce_max(images).numpy():.3f}"
        )

        print(
            f"Example labels: "
            f"{labels[:10].numpy()}"
        )

    print("\n" + "=" * 60)
    print("PREPROCESSING PIPELINE READY")
    print("=" * 60)

    print(
        "\nExpected:"
        "\nImage size    : 224 x 224"
        "\nChannels      : 3 (RGB)"
        "\nPixel range   : -1.0 to 1.0"
        "\nBatch size    : 32"
    )


if __name__ == "__main__":
    test_pipeline()