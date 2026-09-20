from decimal import Decimal

from sqlalchemy import select, text
from sqlalchemy.orm import Session, selectinload

from backend.app.models import WasteCategory


# ============================================================
# Helpers
# ============================================================

def normalize_waste(value: str) -> str:
    return (
        value.strip()
        .lower()
        .replace("-", "_")
        .replace(" ", "_")
        .replace("/", "_")
    )


def _number(value):
    if isinstance(value, Decimal):
        return float(value)

    return value


# ============================================================
# Waste Category Queries
# ============================================================

def get_waste_categories(
    db: Session,
):
    statement = (
        select(WasteCategory)
        .order_by(WasteCategory.id)
    )

    return list(
        db.scalars(statement).all()
    )


def get_waste_category(
    db: Session,
    category_id: int,
):
    statement = (
        select(WasteCategory)
        .options(
            selectinload(
                WasteCategory.waste_items
            )
        )
        .where(
            WasteCategory.id == category_id
        )
    )

    return db.scalar(statement)


# ============================================================
# Phase-3 Knowledge Base Queries
# ============================================================

def get_available_subtypes(
    db: Session,
):
    result = db.execute(
        text(
            """
            SELECT
                id,
                name,
                slug,
                description
            FROM waste_subtypes
            ORDER BY name;
            """
        )
    )

    return [
        dict(row)
        for row in result.mappings().all()
    ]


def get_subtype(
    db: Session,
    waste: str,
):
    normalized = normalize_waste(
        waste
    )

    result = db.execute(
        text(
            """
            SELECT
                id,
                name,
                slug,
                description
            FROM waste_subtypes
            WHERE slug = :slug
            LIMIT 1;
            """
        ),
        {
            "slug": normalized,
        },
    )

    row = result.mappings().first()

    if row is None:
        return None

    return dict(row)


def get_profile_microorganisms(
    db: Session,
    profile_id: int,
):
    result = db.execute(
        text(
            """
            SELECT
                m.id,
                m.scientific_name,
                m.common_name,
                m.microbial_type,
                m.taxonomic_group,
                m.role_description,
                dpm.role_in_profile
            FROM decomposition_profile_microorganisms dpm
            JOIN microorganisms m
                ON m.id = dpm.microorganism_id
            WHERE dpm.profile_id = :profile_id
            ORDER BY m.scientific_name;
            """
        ),
        {
            "profile_id": profile_id,
        },
    )

    return [
        dict(row)
        for row in result.mappings().all()
    ]


def get_profile_sources(
    db: Session,
    profile_id: int,
):
    result = db.execute(
        text(
            """
            SELECT
                s.source_ref,
                s.title,
                s.authors,
                s.publication,
                s.publication_year,
                s.doi,
                s.url,
                s.source_type,
                dps.evidence_note
            FROM decomposition_profile_sources dps
            JOIN sources s
                ON s.id = dps.source_id
            WHERE dps.profile_id = :profile_id
            ORDER BY s.source_ref;
            """
        ),
        {
            "profile_id": profile_id,
        },
    )

    return [
        dict(row)
        for row in result.mappings().all()
    ]


def get_decomposition_profiles(
    db: Session,
    subtype_id: int,
):
    result = db.execute(
        text(
            """
            SELECT
                id AS profile_id,
                treatment_method,
                compost_stage,
                temperature_min_c,
                temperature_max_c,
                moisture_min_percent,
                moisture_max_percent,
                ph_min,
                ph_max,
                cn_ratio_min,
                cn_ratio_max,
                expected_days_min,
                expected_days_max,
                evidence_scope,
                recommendation_text,
                notes
            FROM decomposition_profiles
            WHERE waste_subtype_id = :subtype_id
            ORDER BY
                CASE evidence_scope
                    WHEN 'government_guidance' THEN 1
                    WHEN 'multi_source_synthesis' THEN 2
                    WHEN 'study_reported' THEN 3
                    ELSE 4
                END,
                treatment_method;
            """
        ),
        {
            "subtype_id": subtype_id,
        },
    )

    profiles = []

    for row in result.mappings().all():
        profile = {
            key: _number(value)
            for key, value in dict(row).items()
        }

        profile_id = profile[
            "profile_id"
        ]

        profile[
            "microorganisms"
        ] = get_profile_microorganisms(
            db,
            profile_id,
        )

        profile[
            "sources"
        ] = get_profile_sources(
            db,
            profile_id,
        )

        profiles.append(
            profile
        )

    return profiles


def get_category_by_slug(
    db: Session,
    slug: str,
):
    normalized = normalize_waste(
        slug
    )

    statement = (
        select(WasteCategory)
        .where(
            WasteCategory.slug == normalized
        )
    )

    return db.scalar(statement)
