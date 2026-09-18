import tensorflow as tf
from tensorflow.keras import layers


# ============================================================
# Data Augmentation Pipeline
# ============================================================

data_augmentation = tf.keras.Sequential(
    [
        # Random horizontal flip
        layers.RandomFlip(
            mode="horizontal"
        ),

        # Random rotation
        layers.RandomRotation(
            factor=0.08,
            fill_mode="reflect"
        ),

        # Random zoom
        layers.RandomZoom(
            height_factor=(-0.10, 0.10),
            width_factor=(-0.10, 0.10),
            fill_mode="reflect"
        ),

        # Random brightness adjustment
        layers.RandomBrightness(
            factor=0.15,
            value_range=(-1.0, 1.0)
        ),
    ],
    name="data_augmentation"
)


def augment_images(images, labels):
    """
    Apply random augmentation to a batch of training images.

    Images are expected to already be normalized
    to the range [-1, 1].
    """

    images = data_augmentation(
        images,
        training=True
    )

    return images, labels


def apply_augmentation(dataset):
    """
    Apply augmentation only to the training dataset.
    """

    dataset = dataset.map(
        augment_images,
        num_parallel_calls=tf.data.AUTOTUNE
    )

    dataset = dataset.prefetch(
        buffer_size=tf.data.AUTOTUNE
    )

    return dataset


# ============================================================
# Test
# ============================================================

if __name__ == "__main__":

    print("=" * 60)
    print("DATA AUGMENTATION MODULE")
    print("=" * 60)

    print("\nAugmentation techniques:")

    print("✓ Horizontal Flip")
    print("✓ Random Rotation")
    print("✓ Random Zoom")
    print("✓ Random Brightness")

    print("\nData augmentation module ready.")