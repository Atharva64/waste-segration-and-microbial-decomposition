from pathlib import Path
from collections import defaultdict
import csv
import hashlib
import random
import shutil


# ============================================================
# Configuration
# ============================================================

RAW_DIR = Path("data/raw")
PROCESSED_DIR = Path("data/processed")
REPORT_PATH = Path("data/sample/class_distribution.csv")

TRAIN_RATIO = 0.70
VAL_RATIO = 0.15
TEST_RATIO = 0.15

RANDOM_SEED = 42

SUPPORTED_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".webp",
    ".bmp",
}

# Kaggle class name -> Project class name
CLASS_MAP = {
    "organic waste": "biodegradable",
    "plastic waste": "plastic",
    "paper waste": "paper",
    "glass waste": "glass",
    "metal waste": "metal",
    "e-waste": "e-waste",
}


# ============================================================
# Utility Functions
# ============================================================

def normalize_name(name: str) -> str:
    """
    Normalize folder names for reliable matching.
    """
    return " ".join(
        name.lower()
        .replace("_", " ")
        .replace("-", " ")
        .split()
    )


def discover_class_folders():
    """
    Search recursively inside data/raw and find folders matching
    the required dataset classes.
    """

    discovered = defaultdict(list)

    for folder in RAW_DIR.rglob("*"):

        if not folder.is_dir():
            continue

        normalized = normalize_name(folder.name)

        for source_class, project_class in CLASS_MAP.items():

            if normalized == normalize_name(source_class):
                discovered[project_class].append(folder)

    return discovered


def collect_images(class_folders):
    """
    Collect unique image files recursively from discovered
    class folders.
    """

    images = set()

    for folder in class_folders:

        for file_path in folder.rglob("*"):

            if (
                file_path.is_file()
                and file_path.suffix.lower() in SUPPORTED_EXTENSIONS
            ):
                images.add(file_path.resolve())

    return sorted(images)


def split_images(images):
    """
    Split one class into train / validation / test.
    """

    images = list(images)

    random.Random(RANDOM_SEED).shuffle(images)

    total = len(images)

    train_count = int(total * TRAIN_RATIO)
    val_count = int(total * VAL_RATIO)

    train_images = images[:train_count]

    validation_images = images[
        train_count:
        train_count + val_count
    ]

    test_images = images[
        train_count + val_count:
    ]

    return train_images, validation_images, test_images


def generate_destination_name(source_path: Path):
    """
    Generate a unique destination filename to avoid collisions.
    """

    path_hash = hashlib.sha1(
        str(source_path).encode("utf-8")
    ).hexdigest()[:10]

    return f"{path_hash}_{source_path.name}"


def copy_images(images, destination):
    """
    Copy images into the processed dataset.
    """

    destination.mkdir(
        parents=True,
        exist_ok=True
    )

    for source in images:

        destination_name = generate_destination_name(source)

        destination_path = destination / destination_name

        shutil.copy2(
            source,
            destination_path
        )


def clear_processed_dataset():
    """
    Remove previous processed dataset before recreating it.
    """

    if PROCESSED_DIR.exists():

        print(
            f"Removing previous processed dataset: "
            f"{PROCESSED_DIR}"
        )

        shutil.rmtree(PROCESSED_DIR)

    PROCESSED_DIR.mkdir(
        parents=True,
        exist_ok=True
    )


# ============================================================
# Reporting
# ============================================================

def print_distribution(report):

    print("\n")
    print("=" * 75)
    print("DATASET DISTRIBUTION")
    print("=" * 75)

    print(
        f"{'Class':<18}"
        f"{'Total':>10}"
        f"{'Train':>10}"
        f"{'Validation':>14}"
        f"{'Test':>10}"
    )

    print("-" * 75)

    for row in report:

        print(
            f"{row['class']:<18}"
            f"{row['total']:>10}"
            f"{row['train']:>10}"
            f"{row['validation']:>14}"
            f"{row['test']:>10}"
        )

    print("-" * 75)

    total_all = sum(
        row["total"]
        for row in report
    )

    print(
        f"{'TOTAL':<18}"
        f"{total_all:>10}"
    )


def check_class_balance(report):

    counts = [
        row["total"]
        for row in report
        if row["total"] > 0
    ]

    if not counts:
        return

    largest = max(counts)
    smallest = min(counts)

    imbalance_ratio = largest / smallest

    print("\n")
    print("=" * 75)
    print("CLASS BALANCE CHECK")
    print("=" * 75)

    print(
        f"Largest class : {largest} images"
    )

    print(
        f"Smallest class: {smallest} images"
    )

    print(
        f"Imbalance ratio: {imbalance_ratio:.2f}:1"
    )

    if imbalance_ratio <= 1.5:

        print(
            "Status: Dataset is reasonably balanced."
        )

    elif imbalance_ratio <= 2.0:

        print(
            "Status: Moderate imbalance detected."
        )

        print(
            "Consider augmentation or class weights "
            "during training."
        )

    else:

        print(
            "Status: Significant class imbalance detected."
        )

        print(
            "Consider class weights, augmentation, "
            "or additional images for smaller classes."
        )


def save_report(report):

    REPORT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with REPORT_PATH.open(
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=[
                "class",
                "total",
                "train",
                "validation",
                "test",
            ],
        )

        writer.writeheader()

        writer.writerows(report)

    print(
        f"\nClass distribution report saved to:\n"
        f"{REPORT_PATH}"
    )


# ============================================================
# Main Dataset Preparation
# ============================================================

def main():

    print("=" * 75)
    print("WASTE DATASET PREPARATION")
    print("=" * 75)

    if not RAW_DIR.exists():

        print(
            f"\nERROR: Raw dataset folder does not exist:\n"
            f"{RAW_DIR.resolve()}"
        )

        return

    print(
        f"\nRaw dataset:\n"
        f"{RAW_DIR.resolve()}"
    )

    # --------------------------------------------------------
    # Discover class folders
    # --------------------------------------------------------

    discovered = discover_class_folders()

    print("\n")
    print("=" * 75)
    print("CLASS FOLDER DISCOVERY")
    print("=" * 75)

    missing_classes = []

    for project_class in CLASS_MAP.values():

        folders = discovered.get(
            project_class,
            []
        )

        print(
            f"\n{project_class}:"
        )

        if folders:

            for folder in folders:
                print(
                    f"  ✓ {folder}"
                )

        else:

            print(
                "  ✗ No matching folder found"
            )

            missing_classes.append(
                project_class
            )

    if missing_classes:

        print("\n")
        print("=" * 75)
        print("ERROR")
        print("=" * 75)

        print(
            "The following required classes "
            "were not found:"
        )

        for class_name in missing_classes:
            print(
                f"- {class_name}"
            )

        print(
            "\nCheck the actual folder names "
            "inside data/raw."
        )

        return

    # --------------------------------------------------------
    # Clean previous processed dataset
    # --------------------------------------------------------

    clear_processed_dataset()

    report = []

    # --------------------------------------------------------
    # Process each class independently
    # --------------------------------------------------------

    for project_class in CLASS_MAP.values():

        folders = discovered[
            project_class
        ]

        images = collect_images(
            folders
        )

        print(
            f"\nProcessing {project_class}: "
            f"{len(images)} images"
        )

        if not images:

            print(
                f"WARNING: No images found "
                f"for {project_class}"
            )

            continue

        (
            train_images,
            validation_images,
            test_images,
        ) = split_images(images)

        # Copy training images
        copy_images(
            train_images,
            PROCESSED_DIR
            / "train"
            / project_class
        )

        # Copy validation images
        copy_images(
            validation_images,
            PROCESSED_DIR
            / "validation"
            / project_class
        )

        # Copy test images
        copy_images(
            test_images,
            PROCESSED_DIR
            / "test"
            / project_class
        )

        report.append({
            "class": project_class,
            "total": len(images),
            "train": len(train_images),
            "validation": len(validation_images),
            "test": len(test_images),
        })

    # --------------------------------------------------------
    # Results
    # --------------------------------------------------------

    print_distribution(report)

    check_class_balance(report)

    save_report(report)

    print("\n")
    print("=" * 75)
    print("DATASET PREPARATION COMPLETED")
    print("=" * 75)

    print(
        f"\nProcessed dataset created at:\n"
        f"{PROCESSED_DIR.resolve()}"
    )


if __name__ == "__main__":
    main()