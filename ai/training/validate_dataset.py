from pathlib import Path
from PIL import Image, UnidentifiedImageError
import argparse


SUPPORTED_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".webp",
    ".bmp"
}


def validate_image(image_path: Path):
    """
    Check whether an image can be opened and decoded correctly.

    Returns:
        (True, None)  -> valid image
        (False, msg)  -> invalid/corrupted image
    """

    try:
        # First check image structure
        with Image.open(image_path) as img:
            img.verify()

        # Re-open and actually decode the image
        with Image.open(image_path) as img:
            img.load()

            if img.width <= 0 or img.height <= 0:
                return False, "Invalid image dimensions"

        return True, None

    except (
        UnidentifiedImageError,
        OSError,
        ValueError,
        SyntaxError
    ) as error:
        return False, str(error)


def scan_dataset(dataset_path: Path, delete_invalid=False):

    if not dataset_path.exists():
        print(f"\nERROR: Dataset folder not found: {dataset_path}")
        return

    print("\n==========================================")
    print(" Waste Dataset Validation")
    print("==========================================")
    print(f"Dataset: {dataset_path.resolve()}")
    print()

    total_images = 0
    valid_images = 0
    invalid_images = []

    for file_path in dataset_path.rglob("*"):

        if not file_path.is_file():
            continue

        # Ignore files such as .gitkeep and metadata
        if file_path.suffix.lower() not in SUPPORTED_EXTENSIONS:
            continue

        total_images += 1

        valid, error = validate_image(file_path)

        if valid:
            valid_images += 1

        else:
            invalid_images.append((file_path, error))

            print(f"[INVALID] {file_path}")
            print(f"          Reason: {error}")

            if delete_invalid:
                try:
                    file_path.unlink()
                    print("          Deleted.")
                except OSError as delete_error:
                    print(
                        f"          Could not delete: {delete_error}"
                    )

    print("\n==========================================")
    print(" Validation Summary")
    print("==========================================")

    print(f"Total images checked : {total_images}")
    print(f"Valid images         : {valid_images}")
    print(f"Invalid images       : {len(invalid_images)}")

    if total_images > 0:
        percentage = (valid_images / total_images) * 100

        print(
            f"Valid percentage      : {percentage:.2f}%"
        )

    if invalid_images:

        print("\nInvalid image list:")

        for path, reason in invalid_images:
            print(f"- {path}")
            print(f"  {reason}")

    else:
        print("\nNo corrupted images detected.")

    print("\nValidation completed.")


def main():

    parser = argparse.ArgumentParser(
        description="Validate images in the waste dataset."
    )

    parser.add_argument(
        "--dataset",
        default="data/raw",
        help="Path to dataset directory (default: data/raw)"
    )

    parser.add_argument(
        "--delete-invalid",
        action="store_true",
        help="Delete corrupted images after detection"
    )

    args = parser.parse_args()

    dataset_path = Path(args.dataset)

    scan_dataset(
        dataset_path,
        delete_invalid=args.delete_invalid
    )


if __name__ == "__main__":
    main()