-- Day 15 PostgreSQL knowledge-base schema

CREATE TABLE IF NOT EXISTS waste_subtypes (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    slug VARCHAR(100) NOT NULL UNIQUE,
    description TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS sources (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    source_ref VARCHAR(20) NOT NULL UNIQUE,
    title TEXT NOT NULL,
    authors TEXT,
    publication TEXT,
    publication_year SMALLINT,
    doi VARCHAR(255),
    url TEXT NOT NULL,
    source_type VARCHAR(50) NOT NULL,
    notes TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT chk_source_type CHECK (
        source_type IN (
            'peer_reviewed_article',
            'review_article',
            'government_guidance',
            'government_technical_document',
            'other_credible_source'
        )
    )
);

CREATE TABLE IF NOT EXISTS microorganisms (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    scientific_name VARCHAR(255) NOT NULL,
    common_name VARCHAR(255),
    microbial_type VARCHAR(50) NOT NULL,
    taxonomic_group VARCHAR(255),
    role_description TEXT,
    notes TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uq_microorganism_name_type UNIQUE (scientific_name, microbial_type),
    CONSTRAINT chk_microbial_type CHECK (
        microbial_type IN (
            'bacterium',
            'fungus',
            'actinomycete',
            'archaea',
            'microbial_group',
            'mixed_community',
            'other'
        )
    )
);

CREATE TABLE IF NOT EXISTS decomposition_profiles (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    waste_subtype_id BIGINT NOT NULL
        REFERENCES waste_subtypes(id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,
    treatment_method VARCHAR(100) NOT NULL DEFAULT 'aerobic composting',
    compost_stage VARCHAR(50),
    temperature_min_c NUMERIC(5,2),
    temperature_max_c NUMERIC(5,2),
    moisture_min_percent NUMERIC(5,2),
    moisture_max_percent NUMERIC(5,2),
    ph_min NUMERIC(4,2),
    ph_max NUMERIC(4,2),
    cn_ratio_min NUMERIC(6,2),
    cn_ratio_max NUMERIC(6,2),
    expected_days_min INTEGER,
    expected_days_max INTEGER,
    evidence_scope VARCHAR(50) NOT NULL DEFAULT 'study_reported',
    recommendation_text TEXT,
    notes TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT chk_compost_stage CHECK (
        compost_stage IS NULL OR compost_stage IN (
            'mesophilic',
            'thermophilic',
            'cooling',
            'maturation',
            'multiple_stages',
            'not_specified'
        )
    ),
    CONSTRAINT chk_evidence_scope CHECK (
        evidence_scope IN (
            'study_reported',
            'government_guidance',
            'multi_source_synthesis'
        )
    ),
    CONSTRAINT chk_temperature_range CHECK (
        temperature_min_c IS NULL OR temperature_max_c IS NULL
        OR temperature_min_c <= temperature_max_c
    ),
    CONSTRAINT chk_moisture_range CHECK (
        moisture_min_percent IS NULL OR moisture_max_percent IS NULL
        OR (
            moisture_min_percent BETWEEN 0 AND 100
            AND moisture_max_percent BETWEEN 0 AND 100
            AND moisture_min_percent <= moisture_max_percent
        )
    ),
    CONSTRAINT chk_ph_range CHECK (
        ph_min IS NULL OR ph_max IS NULL
        OR (
            ph_min BETWEEN 0 AND 14
            AND ph_max BETWEEN 0 AND 14
            AND ph_min <= ph_max
        )
    ),
    CONSTRAINT chk_cn_ratio_range CHECK (
        cn_ratio_min IS NULL OR cn_ratio_max IS NULL
        OR (
            cn_ratio_min > 0
            AND cn_ratio_max > 0
            AND cn_ratio_min <= cn_ratio_max
        )
    ),
    CONSTRAINT chk_expected_days CHECK (
        expected_days_min IS NULL OR expected_days_max IS NULL
        OR (
            expected_days_min >= 0
            AND expected_days_max >= 0
            AND expected_days_min <= expected_days_max
        )
    )
);

CREATE TABLE IF NOT EXISTS decomposition_profile_microorganisms (
    profile_id BIGINT NOT NULL
        REFERENCES decomposition_profiles(id)
        ON DELETE CASCADE,
    microorganism_id BIGINT NOT NULL
        REFERENCES microorganisms(id)
        ON DELETE CASCADE,
    role_in_profile TEXT,
    PRIMARY KEY (profile_id, microorganism_id)
);

CREATE TABLE IF NOT EXISTS decomposition_profile_sources (
    profile_id BIGINT NOT NULL
        REFERENCES decomposition_profiles(id)
        ON DELETE CASCADE,
    source_id BIGINT NOT NULL
        REFERENCES sources(id)
        ON DELETE CASCADE,
    evidence_note TEXT,
    PRIMARY KEY (profile_id, source_id)
);

CREATE TABLE IF NOT EXISTS microorganism_sources (
    microorganism_id BIGINT NOT NULL
        REFERENCES microorganisms(id)
        ON DELETE CASCADE,
    source_id BIGINT NOT NULL
        REFERENCES sources(id)
        ON DELETE CASCADE,
    evidence_note TEXT,
    PRIMARY KEY (microorganism_id, source_id)
);

CREATE INDEX IF NOT EXISTS idx_profiles_waste_subtype
    ON decomposition_profiles(waste_subtype_id);

CREATE INDEX IF NOT EXISTS idx_profiles_compost_stage
    ON decomposition_profiles(compost_stage);

CREATE INDEX IF NOT EXISTS idx_microorganisms_type
    ON microorganisms(microbial_type);

CREATE INDEX IF NOT EXISTS idx_sources_type
    ON sources(source_type);

INSERT INTO waste_subtypes (name, slug, description)
VALUES
    ('Food / Kitchen Waste', 'food_kitchen',
     'Biodegradable household and food-service organic waste.'),
    ('Fruit and Vegetable Waste', 'fruit_vegetable',
     'Fruit peels, vegetable scraps, and similar plant-based kitchen waste.'),
    ('Yard / Green Waste', 'yard_green',
     'Leaves, grass clippings, small plant trimmings, and other green waste.'),
    ('Plant and Crop Residues', 'plant_crop_residues',
     'Agricultural and lignocellulosic plant residues such as straw and hulls.')
ON CONFLICT (slug) DO NOTHING;
