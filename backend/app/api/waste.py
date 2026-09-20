from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)
from sqlalchemy.orm import Session

from backend.app.database.session import get_db
from backend.app.schemas.waste import (
    DecompositionLookupResponse,
    WasteCategoryDetail,
    WasteCategorySummary,
)
from backend.app.services.waste_service import (
    get_available_subtypes,
    get_category_by_slug,
    get_decomposition_profiles,
    get_subtype,
    get_waste_categories,
    get_waste_category,
    normalize_waste,
)


router = APIRouter(
    prefix="/api",
    tags=["Waste"],
)


# ============================================================
# GET /api/waste/categories
# ============================================================

@router.get(
    "/waste/categories",
    response_model=list[WasteCategorySummary],
)
def read_waste_categories(
    db: Session = Depends(get_db),
):
    """
    Return all application waste categories.
    """

    return get_waste_categories(
        db
    )


# ============================================================
# GET /api/waste/{id}
# ============================================================

@router.get(
    "/waste/{category_id}",
    response_model=WasteCategoryDetail,
)
def read_waste_category(
    category_id: int,
    db: Session = Depends(get_db),
):
    """
    Return one waste category and its known waste items.
    """

    category = get_waste_category(
        db,
        category_id,
    )

    if category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Waste category not found.",
        )

    return category


# ============================================================
# GET /api/decomposition/{waste}
# ============================================================

@router.get(
    "/decomposition/{waste}",
    response_model=DecompositionLookupResponse,
)
def read_decomposition(
    waste: str,
    db: Session = Depends(get_db),
):
    """
    Return literature-backed decomposition information.

    Supported Phase-3 subtype slugs:
        food_kitchen
        fruit_vegetable
        yard_green
        plant_crop_residues

    For the broad classifier class `biodegradable`, the API
    returns the available sub-types instead of guessing one.
    """

    normalized = normalize_waste(
        waste
    )

    if normalized == "biodegradable":
        subtypes = get_available_subtypes(
            db
        )

        return {
            "waste": waste,
            "decomposition_available": True,
            "subtype_required": True,
            "selected_subtype": None,
            "message": (
                "A biodegradable subtype is required "
                "for a specific decomposition profile."
            ),
            "available_subtypes": subtypes,
            "profiles": [],
        }

    subtype = get_subtype(
        db,
        normalized,
    )

    if subtype is not None:
        profiles = get_decomposition_profiles(
            db,
            subtype["id"],
        )

        return {
            "waste": waste,
            "decomposition_available": bool(
                profiles
            ),
            "subtype_required": False,
            "selected_subtype": subtype[
                "slug"
            ],
            "message": (
                None
                if profiles
                else "No decomposition profiles are stored for this subtype."
            ),
            "available_subtypes": [],
            "profiles": profiles,
        }

    # If it is an application category such as plastic,
    # paper, glass, metal, or e-waste, return a valid response
    # explaining that the microbial knowledge base does not
    # currently cover it.
    category = get_category_by_slug(
        db,
        normalized,
    )

    if category is not None:
        return {
            "waste": waste,
            "decomposition_available": False,
            "subtype_required": False,
            "selected_subtype": None,
            "message": (
                "Microbial decomposition profiles are "
                "currently available only for the "
                "biodegradable knowledge-base subtypes."
            ),
            "available_subtypes": [],
            "profiles": [],
        }

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=(
            "Unknown waste category or "
            "biodegradable subtype."
        ),
    )
