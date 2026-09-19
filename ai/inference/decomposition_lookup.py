import os
from typing import Optional

import psycopg
from psycopg.rows import dict_row


DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": os.getenv("DB_PORT", "5432"),
    "dbname": os.getenv("DB_NAME", "waste_management"),
    "user": os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASSWORD"),
}

BIODEGRADABLE_CATEGORY = "biodegradable"

SUPPORTED_SUBTYPES = {
    "food_kitchen",
    "fruit_vegetable",
    "yard_green",
    "plant_crop_residues",
}


def get_connection():
    if not DB_CONFIG["password"]:
        raise RuntimeError(
            "DB_PASSWORD is not set. Set it in PowerShell before running."
        )

    return psycopg.connect(
        **DB_CONFIG,
        row_factory=dict_row
    )


def normalize_category(category: str) -> str:
    return category.strip().lower().replace(" ", "_")


def get_available_subtypes():
    query = """
        SELECT
            id,
            name,
            slug,
            description
        FROM waste_subtypes
        ORDER BY name;
    """

    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(query)
            return cursor.fetchall()


def get_profiles_for_subtype(subtype: str):
    normalized_subtype = normalize_category(subtype)

    if normalized_subtype not in SUPPORTED_SUBTYPES:
        raise ValueError(
            f"Unsupported biodegradable subtype: {subtype}"
        )

    query = """
        SELECT
            dp.id AS profile_id,
            ws.name AS waste_subtype,
            ws.slug AS waste_subtype_slug,
            dp.treatment_method,
            dp.compost_stage,
            dp.temperature_min_c,
            dp.temperature_max_c,
            dp.moisture_min_percent,
            dp.moisture_max_percent,
            dp.ph_min,
            dp.ph_max,
            dp.cn_ratio_min,
            dp.cn_ratio_max,
            dp.expected_days_min,
            dp.expected_days_max,
            dp.evidence_scope,
            dp.recommendation_text,
            dp.notes
        FROM decomposition_profiles dp
        JOIN waste_subtypes ws
            ON ws.id = dp.waste_subtype_id
        WHERE ws.slug = %s
        ORDER BY dp.treatment_method;
    """

    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(query, (normalized_subtype,))
            return cursor.fetchall()


def get_microorganisms_for_profile(profile_id: int):
    query = """
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
        WHERE dpm.profile_id = %s
        ORDER BY m.scientific_name;
    """

    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(query, (profile_id,))
            return cursor.fetchall()


def get_sources_for_profile(profile_id: int):
    query = """
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
        WHERE dps.profile_id = %s
        ORDER BY s.source_ref;
    """

    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(query, (profile_id,))
            return cursor.fetchall()


def attach_evidence(profiles):
    detailed_profiles = []

    for profile in profiles:
        profile = dict(profile)
        profile_id = profile["profile_id"]

        profile["microorganisms"] = get_microorganisms_for_profile(
            profile_id
        )
        profile["sources"] = get_sources_for_profile(
            profile_id
        )

        detailed_profiles.append(profile)

    return detailed_profiles


def lookup_decomposition(
    predicted_category: str,
    subtype: Optional[str] = None
):
    category = normalize_category(predicted_category)

    if category != BIODEGRADABLE_CATEGORY:
        return {
            "predicted_category": predicted_category,
            "decomposition_available": False,
            "reason": (
                "Microbial decomposition recommendations are "
                "currently available only for biodegradable waste."
            ),
            "profiles": []
        }

    if subtype is None:
        return {
            "predicted_category": predicted_category,
            "decomposition_available": True,
            "subtype_required": True,
            "message": (
                "Biodegradable waste was detected, but the current "
                "classifier does not identify the biodegradable subtype."
            ),
            "available_subtypes": get_available_subtypes(),
            "profiles": []
        }

    profiles = get_profiles_for_subtype(subtype)

    return {
        "predicted_category": predicted_category,
        "decomposition_available": bool(profiles),
        "subtype_required": False,
        "selected_subtype": normalize_category(subtype),
        "profiles": attach_evidence(profiles)
    }


def display_lookup_result(result):
    print("\n" + "=" * 70)
    print("DECOMPOSITION KNOWLEDGE LOOKUP")
    print("=" * 70)

    print(
        f"Predicted category: {result['predicted_category']}"
    )

    if not result["decomposition_available"]:
        print(f"\n{result['reason']}")
        return

    if result.get("subtype_required"):
        print(f"\n{result['message']}")
        print("\nAvailable biodegradable sub-types:")

        for subtype in result["available_subtypes"]:
            print(
                f"- {subtype['slug']}: {subtype['name']}"
            )
        return

    print(
        f"Selected subtype: {result['selected_subtype']}"
    )

    profiles = result["profiles"]

    if not profiles:
        print("\nNo decomposition profiles were found.")
        return

    for index, profile in enumerate(profiles, start=1):
        print("\n" + "-" * 70)
        print(
            f"Profile {index}: {profile['treatment_method']}"
        )
        print(
            f"Evidence scope: {profile['evidence_scope']}"
        )
        print(
            f"Compost stage: {profile['compost_stage']}"
        )

        if profile["recommendation_text"]:
            print(
                "Recommendation/context: "
                f"{profile['recommendation_text']}"
            )

        if profile["microorganisms"]:
            print("\nLiterature-linked microbial groups:")

            for organism in profile["microorganisms"]:
                print(
                    f"  - {organism['scientific_name']} "
                    f"({organism['microbial_type']})"
                )

        if profile["sources"]:
            print("\nSources:")

            for source in profile["sources"]:
                doi_text = (
                    f" DOI: {source['doi']}"
                    if source["doi"]
                    else ""
                )
                print(
                    f"  - [{source['source_ref']}] "
                    f"{source['title']}.{doi_text}"
                )


if __name__ == "__main__":
    result = lookup_decomposition(
        "biodegradable",
        subtype="fruit_vegetable"
    )
    display_lookup_result(result)
