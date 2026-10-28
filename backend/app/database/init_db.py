"""
Create the application tables and seed the six waste categories.

Run from the project root, AFTER the knowledge-base SQL files:

    psql -U postgres -d waste_management -f database/schema.sql
    psql -U postgres -d waste_management -f database/seed.sql
    python -m backend.app.database.init_db

It is safe to run more than once: existing tables are left untouched
and existing categories are not duplicated.
"""

from sqlalchemy import inspect, select

from backend.app.database.base import Base
from backend.app.database.session import SessionLocal, engine
from backend.app.models import WasteCategory


# Must match ai/models/class_names.json (the classifier's output labels).
WASTE_CATEGORIES = (
    {
        "name": "Biodegradable",
        "slug": "biodegradable",
        "is_biodegradable": True,
        "description": (
            "Organic waste such as food scraps, fruit and vegetable "
            "waste, and yard waste that can be composted."
        ),
    },
    {
        "name": "Plastic",
        "slug": "plastic",
        "is_biodegradable": False,
        "description": "Bottles, containers, wrappers, and packaging.",
    },
    {
        "name": "Paper",
        "slug": "paper",
        "is_biodegradable": True,
        "description": "Newspaper, cardboard, and office paper.",
    },
    {
        "name": "Glass",
        "slug": "glass",
        "is_biodegradable": False,
        "description": "Glass bottles, jars, and containers.",
    },
    {
        "name": "Metal",
        "slug": "metal",
        "is_biodegradable": False,
        "description": "Cans, metal containers, and scrap metal.",
    },
    {
        "name": "E-Waste",
        "slug": "e-waste",
        "is_biodegradable": False,
        "description": (
            "Circuit boards, cables, and other electronic parts."
        ),
    },
)

# Created by database/schema.sql, not by the ORM.
REQUIRED_KNOWLEDGE_BASE_TABLES = (
    "waste_subtypes",
    "decomposition_profiles",
)


def main() -> None:
    inspector = inspect(engine)

    missing = [
        table
        for table in REQUIRED_KNOWLEDGE_BASE_TABLES
        if not inspector.has_table(table)
    ]

    if missing:
        raise SystemExit(
            "Knowledge-base tables are missing: "
            + ", ".join(missing)
            + ".\nRun database/schema.sql and database/seed.sql "
            "first, then run this command again."
        )

    Base.metadata.create_all(engine)
    print("Application tables are ready.")

    added = 0

    with SessionLocal() as session:
        for category in WASTE_CATEGORIES:
            exists = session.scalar(
                select(WasteCategory.id).where(
                    WasteCategory.slug == category["slug"]
                )
            )

            if exists is None:
                session.add(WasteCategory(**category))
                added += 1

        session.commit()

    print(
        f"Waste categories: {added} added, "
        f"{len(WASTE_CATEGORIES) - added} already present."
    )


if __name__ == "__main__":
    main()
