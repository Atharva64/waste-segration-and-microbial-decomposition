-- ============================================================
-- AI-Based Waste Segregation and Microbial Decomposition
-- Day 16: Literature-backed seed data
-- Database: PostgreSQL
--
-- Scientific-integrity rules used here:
-- 1. Every scientific record is linked to a real source.
-- 2. NULL means the cited source was not used to assert that value.
-- 3. Study observations are not presented as universal recommendations.
-- 4. Reported microbial association/presence is not treated as proof
--    that an organism alone causes decomposition.
-- 5. General numeric guidance is stored only where supported by the
--    cited EPA/USDA sources.
-- ============================================================

BEGIN;


-- ============================================================
-- 1. Sources
-- ============================================================

INSERT INTO sources (
    source_ref,
    title,
    authors,
    publication,
    publication_year,
    doi,
    url,
    source_type,
    notes
)
VALUES
(
    'G1',
    'Approaches to Composting',
    'United States Environmental Protection Agency',
    'U.S. EPA',
    NULL,
    NULL,
    'https://www.epa.gov/sustainable-management-food/approaches-composting',
    'government_guidance',
    'General composting guidance covering C:N balance, oxygen, moisture, pile structure and temperature.'
),
(
    'G4',
    'National Engineering Handbook, Part 637, Chapter 2 - Composting',
    'USDA Natural Resources Conservation Service',
    'USDA NRCS',
    2010,
    NULL,
    'https://directives.nrcs.usda.gov/sites/default/files2/1720464003/Chapter%202%20-%20Composting.pdf',
    'government_technical_document',
    'Technical composting guidance including an initial C:N recommendation of 20:1 to 40:1 for rapid composting.'
),
(
    'P1',
    'Effects of the feeding ratio of food waste on fed-batch aerobic composting and its microbial community',
    'Xiaojun Wang; Songqing Pan; Zhaoji Zhang; Xiangyu Lin; Yuzhen Zhang; Shaohua Chen',
    'Bioresource Technology',
    2017,
    '10.1016/j.biortech.2016.11.076',
    'https://doi.org/10.1016/j.biortech.2016.11.076',
    'peer_reviewed_article',
    'Food-waste fed-batch aerobic composting study with microbial-community analysis.'
),
(
    'P5',
    'Optimization of vegetable waste composting and the exploration of microbial mechanisms related to fungal communities during composting',
    'X. Lu; Y. Yang; C. Hong; W. Zhu; Y. Yao; F. Zhu; L. Hong; W. Wang',
    'Journal of Environmental Management',
    2022,
    '10.1016/j.jenvman.2022.115694',
    'https://doi.org/10.1016/j.jenvman.2022.115694',
    'peer_reviewed_article',
    'Vegetable-waste composting study examining microbial succession, extracellular enzymes and compost maturation.'
),
(
    'P6',
    'Stability and microbial community analysis during rotary drum composting of vegetable waste',
    'V. Sudharsan Varma; Ajay S. Kalamdhad',
    'International Journal of Recycling of Organic Waste in Agriculture',
    2014,
    '10.1007/s40093-014-0052-4',
    'https://doi.org/10.1007/s40093-014-0052-4',
    'peer_reviewed_article',
    'Rotary-drum vegetable-waste composting study reporting temperature and microbial-population changes.'
),
(
    'P8',
    'Succession and diversity of microorganisms and their association with physicochemical properties during green waste thermophilic composting',
    'Ling Liu; Shuqi Wang; Xiaoping Guo; Tingning Zhao; Bolin Zhang',
    'Waste Management',
    2018,
    '10.1016/j.wasman.2017.12.026',
    'https://doi.org/10.1016/j.wasman.2017.12.026',
    'peer_reviewed_article',
    'Green-waste thermophilic composting study examining bacterial diversity and physicochemical variables.'
),
(
    'P10',
    'Material conversion, microbial community composition and metabolic functional succession during green soybean hull composting',
    'Chao Zhang; Zheng Gao; Wencong Shi; Linchao Li; Renmao Tian; Jian Huang; Rongshan Lin; Bing Wang; Bo Zhou',
    'Bioresource Technology',
    2020,
    '10.1016/j.biortech.2020.123823',
    'https://doi.org/10.1016/j.biortech.2020.123823',
    'peer_reviewed_article',
    'Green soybean hull and maize-straw composting study with bacterial, fungal and metabolic succession analysis.'
),
(
    'P12',
    'Microbial Community Succession and Response to Environmental Variables During Cow Manure and Corn Straw Composting',
    'Q. Meng; W. Yang; M. Men; A. Bello; X. Xu; B. Xu; L. Deng; X. Jiang; S. Sheng; X. Wu; Y. Han; H. Zhu',
    'Frontiers in Microbiology',
    2019,
    '10.3389/fmicb.2019.00529',
    'https://doi.org/10.3389/fmicb.2019.00529',
    'peer_reviewed_article',
    'Corn-straw co-composting study linking microbial succession with physicochemical variables.'
)
ON CONFLICT (source_ref) DO UPDATE
SET
    title = EXCLUDED.title,
    authors = EXCLUDED.authors,
    publication = EXCLUDED.publication,
    publication_year = EXCLUDED.publication_year,
    doi = EXCLUDED.doi,
    url = EXCLUDED.url,
    source_type = EXCLUDED.source_type,
    notes = EXCLUDED.notes;


-- ============================================================
-- 2. Microorganisms / microbial groups
-- ============================================================

INSERT INTO microorganisms (
    scientific_name,
    common_name,
    microbial_type,
    taxonomic_group,
    role_description,
    notes
)
VALUES
(
    'Firmicutes',
    NULL,
    'microbial_group',
    'Bacterial phylum',
    'Reported as an abundant/dominant bacterial phylum in multiple composting studies.',
    'Abundance varies with feedstock, treatment and composting stage.'
),
(
    'Proteobacteria',
    NULL,
    'microbial_group',
    'Bacterial phylum',
    'Reported as a major bacterial phylum in food-, green-waste- and crop-residue composting studies.',
    'Presence does not imply one universal functional role.'
),
(
    'Bacteroidetes',
    NULL,
    'microbial_group',
    'Bacterial phylum',
    'Reported among major bacterial phyla in food-waste and corn-straw composting studies.',
    NULL
),
(
    'Actinobacteria',
    NULL,
    'microbial_group',
    'Bacterial phylum',
    'Reported in composting communities and associated with different stages depending on the study.',
    NULL
),
(
    'Chloroflexi',
    NULL,
    'microbial_group',
    'Bacterial phylum',
    'Reported among abundant bacterial phyla in green-waste and corn-straw composting.',
    NULL
),
(
    'Saccharomonospora',
    NULL,
    'actinomycete',
    'Actinobacteria',
    'Reported enriched in middle/late stages of the vegetable-waste treatment studied by Lu et al. (2022).',
    'Study-specific observation.'
),
(
    'Aspergillus',
    NULL,
    'fungus',
    'Ascomycota',
    'Reported in vegetable/plant-residue composting studies; Zhang et al. (2020) reported an important role in lignocellulose degradation.',
    'Role depends on feedstock and study conditions.'
),
(
    'Thermomyces',
    NULL,
    'fungus',
    'Ascomycota',
    'Reported in vegetable/plant-residue composting studies; Zhang et al. (2020) reported an important role in lignocellulose degradation.',
    'Role depends on feedstock and study conditions.'
),
(
    'Microascus',
    NULL,
    'fungus',
    'Ascomycota',
    'Identified as a keystone taxon in the vegetable-waste treatment reported by Lu et al. (2022).',
    'Study-specific observation.'
),
(
    'Fungi',
    NULL,
    'microbial_group',
    'Fungal community',
    'Fungal populations were measured during rotary-drum vegetable-waste composting.',
    'Broad community-level record.'
),
(
    'Actinomycetes',
    NULL,
    'microbial_group',
    'Actinobacteria',
    'Actinomycete populations were measured during rotary-drum vegetable-waste composting.',
    'Broad community-level record.'
),
(
    'Streptomycetes',
    NULL,
    'microbial_group',
    'Actinobacteria',
    'Streptomycete populations were measured during rotary-drum vegetable-waste composting.',
    'Broad community-level record.'
),
(
    'Spore-forming bacteria',
    NULL,
    'microbial_group',
    'Bacteria',
    'Reported as a major population associated with degradation during the thermophilic stage of the vegetable-waste rotary-drum study.',
    'Study-specific community description, not a single taxon.'
),
(
    'Streptosporangiaceae',
    NULL,
    'microbial_group',
    'Actinobacteria',
    'Reported as a biomarker in the thermophilic phase of green soybean hull composting.',
    'Study-specific biomarker.'
),
(
    'Chaetomiaceae',
    NULL,
    'microbial_group',
    'Ascomycota',
    'Reported as a fungal biomarker in thermophilic and cooling stages of green soybean hull composting.',
    'Study-specific biomarker.'
),
(
    'Ascomycota',
    NULL,
    'microbial_group',
    'Fungal phylum',
    'Reported among major fungal groups during cow-manure and corn-straw composting.',
    NULL
),
(
    'Basidiomycota',
    NULL,
    'microbial_group',
    'Fungal phylum',
    'Reported among major fungal groups during cow-manure and corn-straw composting.',
    NULL
),
(
    'Actinomycetales',
    NULL,
    'microbial_group',
    'Actinobacteria',
    'Reported as a bacterial indicator of the maturation phase in the corn-straw co-composting study.',
    'Study-specific indicator.'
),
(
    'Sordariomycetes',
    NULL,
    'microbial_group',
    'Ascomycota',
    'Reported as a fungal indicator of the maturation phase in the corn-straw co-composting study.',
    'Study-specific indicator.'
)
ON CONFLICT (scientific_name, microbial_type) DO UPDATE
SET
    common_name = EXCLUDED.common_name,
    taxonomic_group = EXCLUDED.taxonomic_group,
    role_description = EXCLUDED.role_description,
    notes = EXCLUDED.notes;


-- ============================================================
-- 3. General multi-source composting profiles
--
-- EPA G1:
--   * aerobic composting
--   * roughly 30:1 C:N ideal balance
--   * adequate moisture and oxygen required
--   * 131-160 F (55.0-71.1 C) supports optimal activity
--
-- USDA/NRCS G4:
--   * initial C:N 20:1-40:1 recommended for rapid composting
--
-- We therefore store 20-40 as a broad initial C:N guidance
-- range and 55.0-71.11 C as EPA's microorganism activity range.
-- ============================================================

INSERT INTO decomposition_profiles (
    waste_subtype_id,
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
)
SELECT
    ws.id,
    'aerobic composting',
    'multiple_stages',
    55.00,
    71.11,
    NULL,
    NULL,
    NULL,
    NULL,
    20.00,
    40.00,
    NULL,
    NULL,
    'multi_source_synthesis',
    'Maintain aerobic conditions and adequate moisture; manage carbon and nitrogen balance and monitor compost temperature.',
    'General guidance synthesized from EPA G1 and USDA/NRCS G4. Temperature is EPA''s 131-160 F range converted to Celsius; initial C:N range is USDA/NRCS 20:1-40:1.'
FROM waste_subtypes ws
WHERE ws.slug IN (
    'food_kitchen',
    'fruit_vegetable',
    'yard_green',
    'plant_crop_residues'
)
AND NOT EXISTS (
    SELECT 1
    FROM decomposition_profiles dp
    WHERE dp.waste_subtype_id = ws.id
      AND dp.treatment_method = 'aerobic composting'
      AND dp.evidence_scope = 'multi_source_synthesis'
);


-- ============================================================
-- 4. Study-specific decomposition profiles
-- ============================================================

-- P1: Food waste
INSERT INTO decomposition_profiles (
    waste_subtype_id,
    treatment_method,
    compost_stage,
    evidence_scope,
    recommendation_text,
    notes
)
SELECT
    ws.id,
    'fed-batch aerobic composting',
    'multiple_stages',
    'study_reported',
    'Study observation: 5% and 10% daily food-waste feeding treatments maintained thermophilic composting, while the 15% treatment performed poorly in association with excessive moisture.',
    'P1 reported initial moisture of approximately 62% and C:N of approximately 38:1 in the experiment. Firmicutes, Proteobacteria, Bacteroidetes and Actinobacteria were dominant phyla; temperature was identified as a key factor in community succession.'
FROM waste_subtypes ws
WHERE ws.slug = 'food_kitchen'
AND NOT EXISTS (
    SELECT 1
    FROM decomposition_profiles dp
    WHERE dp.waste_subtype_id = ws.id
      AND dp.treatment_method = 'fed-batch aerobic composting'
);

-- P5: Vegetable waste
INSERT INTO decomposition_profiles (
    waste_subtype_id,
    treatment_method,
    compost_stage,
    evidence_scope,
    recommendation_text,
    notes
)
SELECT
    ws.id,
    'vegetable-waste aerobic composting',
    'multiple_stages',
    'study_reported',
    'Study observation: microbial succession and extracellular-enzyme activity changed across vegetable-waste composting and were associated with compost maturation.',
    'P5 reported increased Firmicutes in the thermophilic stage under the combined-additive treatment; Saccharomonospora, Aspergillus and Thermomyces were enriched in middle/late stages, and Microascus was among reported keystone taxa.'
FROM waste_subtypes ws
WHERE ws.slug = 'fruit_vegetable'
AND NOT EXISTS (
    SELECT 1
    FROM decomposition_profiles dp
    WHERE dp.waste_subtype_id = ws.id
      AND dp.treatment_method = 'vegetable-waste aerobic composting'
);

-- P6: Rotary-drum vegetable waste
INSERT INTO decomposition_profiles (
    waste_subtype_id,
    treatment_method,
    compost_stage,
    temperature_min_c,
    temperature_max_c,
    expected_days_min,
    expected_days_max,
    evidence_scope,
    recommendation_text,
    notes
)
SELECT
    ws.id,
    'rotary-drum aerobic composting',
    'multiple_stages',
    54.00,
    56.00,
    20,
    20,
    'study_reported',
    'Study observation: trial 3 maintained an average temperature of 54-56 C for seven days and showed strong organic-matter degradation during the 20-day experiment.',
    'P6 reported an early thermophilic phase within 18-24 hours, a maximum of 61.4 C in trial 3, and fungal, actinomycete and streptomycete population changes over the composting period. The stored 54-56 C range is the reported sustained average for trial 3, not a universal optimum.'
FROM waste_subtypes ws
WHERE ws.slug = 'fruit_vegetable'
AND NOT EXISTS (
    SELECT 1
    FROM decomposition_profiles dp
    WHERE dp.waste_subtype_id = ws.id
      AND dp.treatment_method = 'rotary-drum aerobic composting'
);

-- P8: Green waste
INSERT INTO decomposition_profiles (
    waste_subtype_id,
    treatment_method,
    compost_stage,
    evidence_scope,
    recommendation_text,
    notes
)
SELECT
    ws.id,
    'green-waste thermophilic composting',
    'thermophilic',
    'study_reported',
    'Study observation: bacterial-community composition during green-waste thermophilic composting was associated with composting stage and physicochemical properties.',
    'P8 reported Firmicutes, Chloroflexi and Proteobacteria as the most abundant phyla among treatments; bacterial diversity was associated with humic acid indicators and temperature.'
FROM waste_subtypes ws
WHERE ws.slug = 'yard_green'
AND NOT EXISTS (
    SELECT 1
    FROM decomposition_profiles dp
    WHERE dp.waste_subtype_id = ws.id
      AND dp.treatment_method = 'green-waste thermophilic composting'
);

-- P10: Plant/crop residues
INSERT INTO decomposition_profiles (
    waste_subtype_id,
    treatment_method,
    compost_stage,
    evidence_scope,
    recommendation_text,
    notes
)
SELECT
    ws.id,
    'green-soybean-hull and maize-straw composting',
    'multiple_stages',
    'study_reported',
    'Study observation: bacterial and fungal communities showed temporal succession during composting of green soybean hulls and maize straw.',
    'P10 identified Streptosporangiaceae as a thermophilic-stage biomarker and Chaetomiaceae as a thermophilic/cooling-stage biomarker; Thermomyces and Aspergillus were reported as important in lignocellulose degradation.'
FROM waste_subtypes ws
WHERE ws.slug = 'plant_crop_residues'
AND NOT EXISTS (
    SELECT 1
    FROM decomposition_profiles dp
    WHERE dp.waste_subtype_id = ws.id
      AND dp.treatment_method = 'green-soybean-hull and maize-straw composting'
);

-- P12: Corn-straw co-composting
INSERT INTO decomposition_profiles (
    waste_subtype_id,
    treatment_method,
    compost_stage,
    evidence_scope,
    recommendation_text,
    notes
)
SELECT
    ws.id,
    'cow-manure and corn-straw co-composting',
    'multiple_stages',
    'study_reported',
    'Study observation: bacterial and fungal communities changed across composting stages and were significantly associated with multiple physicochemical variables.',
    'P12 reported Proteobacteria, Bacteroidetes, Firmicutes, Chloroflexi and Actinobacteria among major bacterial phyla and Ascomycota/Basidiomycota among fungal groups. Actinomycetales and Sordariomycetes were reported as maturation-phase indicators.'
FROM waste_subtypes ws
WHERE ws.slug = 'plant_crop_residues'
AND NOT EXISTS (
    SELECT 1
    FROM decomposition_profiles dp
    WHERE dp.waste_subtype_id = ws.id
      AND dp.treatment_method = 'cow-manure and corn-straw co-composting'
);


-- ============================================================
-- 5. Link profiles to sources
-- ============================================================

WITH profile_source_map (
    waste_slug,
    treatment_method,
    source_ref,
    evidence_note
) AS (
    VALUES
    ('food_kitchen', 'aerobic composting', 'G1',
     'EPA general aerobic-composting guidance, including oxygen, moisture, C:N balance and temperature.'),
    ('food_kitchen', 'aerobic composting', 'G4',
     'USDA/NRCS general composting guidance, including initial C:N 20:1-40:1 for rapid composting.'),

    ('fruit_vegetable', 'aerobic composting', 'G1',
     'EPA general aerobic-composting guidance.'),
    ('fruit_vegetable', 'aerobic composting', 'G4',
     'USDA/NRCS initial C:N guidance.'),

    ('yard_green', 'aerobic composting', 'G1',
     'EPA guidance explicitly includes dry leaves and other organic compost feedstocks.'),
    ('yard_green', 'aerobic composting', 'G4',
     'USDA/NRCS general composting guidance.'),

    ('plant_crop_residues', 'aerobic composting', 'G1',
     'EPA general aerobic-composting principles.'),
    ('plant_crop_residues', 'aerobic composting', 'G4',
     'USDA/NRCS composting guidance applicable to agricultural organic materials.'),

    ('food_kitchen', 'fed-batch aerobic composting', 'P1',
     'Direct experimental source for the stored food-waste profile.'),

    ('fruit_vegetable', 'vegetable-waste aerobic composting', 'P5',
     'Direct experimental source for microbial succession in vegetable-waste composting.'),

    ('fruit_vegetable', 'rotary-drum aerobic composting', 'P6',
     'Direct experimental source for the stored rotary-drum temperature and duration observations.'),

    ('yard_green', 'green-waste thermophilic composting', 'P8',
     'Direct experimental source for green-waste microbial-community observations.'),

    ('plant_crop_residues', 'green-soybean-hull and maize-straw composting', 'P10',
     'Direct experimental source for plant-residue microbial succession and lignocellulose-related taxa.'),

    ('plant_crop_residues', 'cow-manure and corn-straw co-composting', 'P12',
     'Direct experimental source for corn-straw microbial succession and environmental associations.')
)
INSERT INTO decomposition_profile_sources (
    profile_id,
    source_id,
    evidence_note
)
SELECT
    dp.id,
    s.id,
    psm.evidence_note
FROM profile_source_map psm
JOIN waste_subtypes ws
    ON ws.slug = psm.waste_slug
JOIN decomposition_profiles dp
    ON dp.waste_subtype_id = ws.id
   AND dp.treatment_method = psm.treatment_method
JOIN sources s
    ON s.source_ref = psm.source_ref
ON CONFLICT (profile_id, source_id) DO UPDATE
SET evidence_note = EXCLUDED.evidence_note;


-- ============================================================
-- 6. Link study profiles to microorganisms
-- ============================================================

WITH profile_microbe_map (
    waste_slug,
    treatment_method,
    scientific_name,
    microbial_type,
    role_in_profile
) AS (
    VALUES
    -- P1 food waste
    ('food_kitchen', 'fed-batch aerobic composting', 'Firmicutes', 'microbial_group',
     'Reported among the dominant phyla in the food-waste composting community.'),
    ('food_kitchen', 'fed-batch aerobic composting', 'Proteobacteria', 'microbial_group',
     'Reported among the dominant phyla in the food-waste composting community.'),
    ('food_kitchen', 'fed-batch aerobic composting', 'Bacteroidetes', 'microbial_group',
     'Reported among the dominant phyla in the food-waste composting community.'),
    ('food_kitchen', 'fed-batch aerobic composting', 'Actinobacteria', 'microbial_group',
     'Reported among the dominant phyla in the food-waste composting community.'),

    -- P5 vegetable waste
    ('fruit_vegetable', 'vegetable-waste aerobic composting', 'Firmicutes', 'microbial_group',
     'Reported at increased relative abundance in the thermophilic stage of the combined-additive treatment.'),
    ('fruit_vegetable', 'vegetable-waste aerobic composting', 'Saccharomonospora', 'actinomycete',
     'Reported enriched in the middle/late stages of the combined-additive treatment.'),
    ('fruit_vegetable', 'vegetable-waste aerobic composting', 'Aspergillus', 'fungus',
     'Reported enriched in the middle/late stages and associated with measured compost properties.'),
    ('fruit_vegetable', 'vegetable-waste aerobic composting', 'Thermomyces', 'fungus',
     'Reported enriched in the middle/late stages and associated with measured compost properties.'),
    ('fruit_vegetable', 'vegetable-waste aerobic composting', 'Microascus', 'fungus',
     'Reported as one of the keystone taxa in network analysis.'),

    -- P6 vegetable waste
    ('fruit_vegetable', 'rotary-drum aerobic composting', 'Spore-forming bacteria', 'microbial_group',
     'Reported as a major population contributing during the thermophilic degradation stage.'),
    ('fruit_vegetable', 'rotary-drum aerobic composting', 'Fungi', 'microbial_group',
     'Fungal populations were measured and declined during the thermophilic stage.'),
    ('fruit_vegetable', 'rotary-drum aerobic composting', 'Actinomycetes', 'microbial_group',
     'Actinomycete populations were measured across the composting process.'),
    ('fruit_vegetable', 'rotary-drum aerobic composting', 'Streptomycetes', 'microbial_group',
     'Streptomycete populations were measured across the composting process.'),

    -- P8 green waste
    ('yard_green', 'green-waste thermophilic composting', 'Firmicutes', 'microbial_group',
     'Reported among the most abundant phyla across the green-waste treatments.'),
    ('yard_green', 'green-waste thermophilic composting', 'Chloroflexi', 'microbial_group',
     'Reported among the most abundant phyla across the green-waste treatments.'),
    ('yard_green', 'green-waste thermophilic composting', 'Proteobacteria', 'microbial_group',
     'Reported among the most abundant phyla across the green-waste treatments.'),

    -- P10 plant/crop residues
    ('plant_crop_residues', 'green-soybean-hull and maize-straw composting', 'Streptosporangiaceae', 'microbial_group',
     'Reported as a biomarker in the thermophilic stage.'),
    ('plant_crop_residues', 'green-soybean-hull and maize-straw composting', 'Chaetomiaceae', 'microbial_group',
     'Reported as a biomarker in thermophilic and cooling stages.'),
    ('plant_crop_residues', 'green-soybean-hull and maize-straw composting', 'Thermomyces', 'fungus',
     'Reported to play an important role in lignocellulose degradation.'),
    ('plant_crop_residues', 'green-soybean-hull and maize-straw composting', 'Aspergillus', 'fungus',
     'Reported to play an important role in lignocellulose degradation.'),

    -- P12 corn straw
    ('plant_crop_residues', 'cow-manure and corn-straw co-composting', 'Proteobacteria', 'microbial_group',
     'Reported among the major bacterial phyla.'),
    ('plant_crop_residues', 'cow-manure and corn-straw co-composting', 'Bacteroidetes', 'microbial_group',
     'Reported among the major bacterial phyla.'),
    ('plant_crop_residues', 'cow-manure and corn-straw co-composting', 'Firmicutes', 'microbial_group',
     'Reported among the major bacterial phyla.'),
    ('plant_crop_residues', 'cow-manure and corn-straw co-composting', 'Chloroflexi', 'microbial_group',
     'Reported among the major bacterial phyla.'),
    ('plant_crop_residues', 'cow-manure and corn-straw co-composting', 'Actinobacteria', 'microbial_group',
     'Reported among the major bacterial phyla.'),
    ('plant_crop_residues', 'cow-manure and corn-straw co-composting', 'Ascomycota', 'microbial_group',
     'Reported among the major fungal groups.'),
    ('plant_crop_residues', 'cow-manure and corn-straw co-composting', 'Basidiomycota', 'microbial_group',
     'Reported among the major fungal groups.'),
    ('plant_crop_residues', 'cow-manure and corn-straw co-composting', 'Actinomycetales', 'microbial_group',
     'Reported as an indicator of the maturation phase.'),
    ('plant_crop_residues', 'cow-manure and corn-straw co-composting', 'Sordariomycetes', 'microbial_group',
     'Reported as a fungal indicator of the maturation phase.')
)
INSERT INTO decomposition_profile_microorganisms (
    profile_id,
    microorganism_id,
    role_in_profile
)
SELECT
    dp.id,
    m.id,
    pmm.role_in_profile
FROM profile_microbe_map pmm
JOIN waste_subtypes ws
    ON ws.slug = pmm.waste_slug
JOIN decomposition_profiles dp
    ON dp.waste_subtype_id = ws.id
   AND dp.treatment_method = pmm.treatment_method
JOIN microorganisms m
    ON m.scientific_name = pmm.scientific_name
   AND m.microbial_type = pmm.microbial_type
ON CONFLICT (profile_id, microorganism_id) DO UPDATE
SET role_in_profile = EXCLUDED.role_in_profile;


-- ============================================================
-- 7. Link microorganisms directly to supporting sources
-- ============================================================

WITH microbe_source_map (
    scientific_name,
    microbial_type,
    source_ref,
    evidence_note
) AS (
    VALUES
    ('Firmicutes', 'microbial_group', 'P1',
     'Reported among dominant phyla in fed-batch food-waste composting.'),
    ('Proteobacteria', 'microbial_group', 'P1',
     'Reported among dominant phyla in fed-batch food-waste composting.'),
    ('Bacteroidetes', 'microbial_group', 'P1',
     'Reported among dominant phyla in fed-batch food-waste composting.'),
    ('Actinobacteria', 'microbial_group', 'P1',
     'Reported among dominant phyla in fed-batch food-waste composting.'),

    ('Firmicutes', 'microbial_group', 'P5',
     'Reported at increased relative abundance in the thermophilic stage of the combined-additive treatment.'),
    ('Saccharomonospora', 'actinomycete', 'P5',
     'Reported enriched in the middle/late stages.'),
    ('Aspergillus', 'fungus', 'P5',
     'Reported enriched in the middle/late stages.'),
    ('Thermomyces', 'fungus', 'P5',
     'Reported enriched in the middle/late stages.'),
    ('Microascus', 'fungus', 'P5',
     'Reported as a keystone taxon.'),

    ('Spore-forming bacteria', 'microbial_group', 'P6',
     'Reported during thermophilic vegetable-waste composting.'),
    ('Fungi', 'microbial_group', 'P6',
     'Fungal population measured during the rotary-drum experiment.'),
    ('Actinomycetes', 'microbial_group', 'P6',
     'Actinomycete population measured during the rotary-drum experiment.'),
    ('Streptomycetes', 'microbial_group', 'P6',
     'Streptomycete population measured during the rotary-drum experiment.'),

    ('Firmicutes', 'microbial_group', 'P8',
     'One of the most abundant phyla in the green-waste treatments.'),
    ('Chloroflexi', 'microbial_group', 'P8',
     'One of the most abundant phyla in the green-waste treatments.'),
    ('Proteobacteria', 'microbial_group', 'P8',
     'One of the most abundant phyla in the green-waste treatments.'),

    ('Streptosporangiaceae', 'microbial_group', 'P10',
     'Reported thermophilic-stage biomarker.'),
    ('Chaetomiaceae', 'microbial_group', 'P10',
     'Reported thermophilic/cooling-stage fungal biomarker.'),
    ('Thermomyces', 'fungus', 'P10',
     'Reported important in lignocellulose degradation.'),
    ('Aspergillus', 'fungus', 'P10',
     'Reported important in lignocellulose degradation.'),

    ('Proteobacteria', 'microbial_group', 'P12',
     'Reported major bacterial phylum.'),
    ('Bacteroidetes', 'microbial_group', 'P12',
     'Reported major bacterial phylum.'),
    ('Firmicutes', 'microbial_group', 'P12',
     'Reported major bacterial phylum.'),
    ('Chloroflexi', 'microbial_group', 'P12',
     'Reported major bacterial phylum.'),
    ('Actinobacteria', 'microbial_group', 'P12',
     'Reported major bacterial phylum.'),
    ('Ascomycota', 'microbial_group', 'P12',
     'Reported major fungal group.'),
    ('Basidiomycota', 'microbial_group', 'P12',
     'Reported major fungal group.'),
    ('Actinomycetales', 'microbial_group', 'P12',
     'Reported maturation-phase bacterial indicator.'),
    ('Sordariomycetes', 'microbial_group', 'P12',
     'Reported maturation-phase fungal indicator.')
)
INSERT INTO microorganism_sources (
    microorganism_id,
    source_id,
    evidence_note
)
SELECT
    m.id,
    s.id,
    msm.evidence_note
FROM microbe_source_map msm
JOIN microorganisms m
    ON m.scientific_name = msm.scientific_name
   AND m.microbial_type = msm.microbial_type
JOIN sources s
    ON s.source_ref = msm.source_ref
ON CONFLICT (microorganism_id, source_id) DO UPDATE
SET evidence_note = EXCLUDED.evidence_note;


COMMIT;


-- ============================================================
-- Optional verification queries
-- ============================================================

-- SELECT * FROM sources ORDER BY source_ref;
-- SELECT * FROM microorganisms ORDER BY scientific_name;
--
-- SELECT
--     ws.name AS waste_subtype,
--     dp.treatment_method,
--     dp.compost_stage,
--     dp.evidence_scope
-- FROM decomposition_profiles dp
-- JOIN waste_subtypes ws ON ws.id = dp.waste_subtype_id
-- ORDER BY ws.name, dp.treatment_method;
--
-- SELECT
--     ws.name AS waste_subtype,
--     dp.treatment_method,
--     m.scientific_name,
--     dpm.role_in_profile
-- FROM decomposition_profile_microorganisms dpm
-- JOIN decomposition_profiles dp ON dp.id = dpm.profile_id
-- JOIN waste_subtypes ws ON ws.id = dp.waste_subtype_id
-- JOIN microorganisms m ON m.id = dpm.microorganism_id
-- ORDER BY ws.name, dp.treatment_method, m.scientific_name;
