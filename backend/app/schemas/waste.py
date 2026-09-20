from pydantic import BaseModel, ConfigDict, Field


# ============================================================
# Waste Category Schemas
# ============================================================

class WasteItemSummary(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    slug: str
    description: str | None = None
    knowledge_subtype_slug: str | None = None


class WasteCategorySummary(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    slug: str
    description: str | None = None
    is_biodegradable: bool


class WasteCategoryDetail(WasteCategorySummary):
    waste_items: list[WasteItemSummary] = Field(default_factory=list)


# ============================================================
# Decomposition Schemas
# ============================================================

class DecompositionSubtype(BaseModel):
    id: int
    name: str
    slug: str
    description: str | None = None


class DecompositionMicroorganism(BaseModel):
    id: int
    scientific_name: str
    common_name: str | None = None
    microbial_type: str
    taxonomic_group: str | None = None
    role_description: str | None = None
    role_in_profile: str | None = None


class DecompositionSource(BaseModel):
    source_ref: str
    title: str
    authors: str | None = None
    publication: str | None = None
    publication_year: int | None = None
    doi: str | None = None
    url: str
    source_type: str
    evidence_note: str | None = None


class DecompositionProfileResponse(BaseModel):
    profile_id: int
    treatment_method: str
    compost_stage: str | None = None

    temperature_min_c: float | None = None
    temperature_max_c: float | None = None

    moisture_min_percent: float | None = None
    moisture_max_percent: float | None = None

    ph_min: float | None = None
    ph_max: float | None = None

    cn_ratio_min: float | None = None
    cn_ratio_max: float | None = None

    expected_days_min: int | None = None
    expected_days_max: int | None = None

    evidence_scope: str
    recommendation_text: str | None = None
    notes: str | None = None

    microorganisms: list[DecompositionMicroorganism] = Field(default_factory=list)
    sources: list[DecompositionSource] = Field(default_factory=list)


class DecompositionLookupResponse(BaseModel):
    waste: str
    decomposition_available: bool
    subtype_required: bool = False
    selected_subtype: str | None = None
    message: str | None = None
    available_subtypes: list[DecompositionSubtype] = Field(default_factory=list)
    profiles: list[DecompositionProfileResponse] = Field(default_factory=list)
