# Microbial Decomposition References

## AI-Based Waste Segregation and Microbial Decomposition Recommendation System

**Research log date:** 19 September 2026

This file records credible sources that will support the microbial-decomposition knowledge base used by the project.

The purpose of this research phase is **not** to prescribe laboratory culturing procedures. The project will store literature-backed information about composting conditions, microbial-community succession, degradation pathways, and suitable waste-management methods.

---

## 1. Initial Biodegradable Sub-types

For the first version of the knowledge base, biodegradable waste is divided into four practical sub-types:

1. **Food / kitchen waste**
2. **Fruit and vegetable waste**
3. **Yard / green waste**
4. **Plant and crop residues**

These sub-types can be expanded later if the image classifier or recommendation system becomes more detailed.

---

## 2. Source Quality Rules

A source is accepted when it is one of the following:

- Peer-reviewed research article
- Peer-reviewed review article
- U.S. EPA guidance/resource
- USDA / NRCS technical guidance
- PubMed-indexed publication
- Reputable scientific publisher page with DOI

For each recommendation added to the database, the supporting source should be recorded.

---

## 3. Source Coverage Matrix

The same source may support more than one biodegradable sub-type when its scope is relevant.

| Ref | Food / Kitchen | Fruit & Vegetable | Yard / Green | Plant / Crop Residues |
|---|:---:|:---:|:---:|:---:|
| G1 | ✓ | ✓ | ✓ | ✓ |
| G2 | ✓ | ✓ |  |  |
| G3 |  |  | ✓ | ✓ |
| G4 | ✓ | ✓ | ✓ | ✓ |
| P1 | ✓ |  |  |  |
| P2 | ✓ | ✓ | ✓ | ✓ |
| P3 | ✓ | ✓ |  |  |
| P4 | ✓ |  |  |  |
| P5 |  | ✓ |  |  |
| P6 |  | ✓ |  |  |
| P7 |  | ✓ |  |  |
| P8 |  |  | ✓ |  |
| P9 |  |  | ✓ | ✓ |
| P10 |  |  |  | ✓ |
| P11 | ✓ |  | ✓ | ✓ |
| P12 |  |  | ✓ | ✓ |

### Coverage count

- **Food / kitchen waste:** 8 sources
- **Fruit and vegetable waste:** 8 sources
- **Yard / green waste:** 8 sources
- **Plant and crop residues:** 8 sources

---

# 4. Government and Technical Sources

## G1 — U.S. EPA: Approaches to Composting

**Organization:** United States Environmental Protection Agency  
**Type:** Government technical guidance

**Source:**  
https://www.epa.gov/sustainable-management-food/approaches-composting

### Why it is useful

Supports the general composting process and explains the importance of:

- carbon-to-nitrogen balance,
- oxygen,
- moisture,
- particle size,
- pile structure,
- microbial decomposition,
- temperature changes during decomposition.

The EPA describes an ideal feedstock balance of roughly 30:1 elemental carbon to nitrogen as a general composting target.

### Applicable sub-types

- Food / kitchen waste
- Fruit and vegetable waste
- Yard / green waste
- Plant and crop residues

---

## G2 — U.S. EPA: Composting at Home

**Organization:** United States Environmental Protection Agency  
**Type:** Government guidance

**Source:**  
https://www.epa.gov/recycle/composting-home

### Why it is useful

Provides practical, non-laboratory guidance for household composting, including:

- balancing green and brown materials,
- maintaining moisture,
- maintaining airflow,
- reducing particle size,
- curing finished compost,
- suitable and unsuitable household feedstocks.

### Applicable sub-types

- Food / kitchen waste
- Fruit and vegetable waste

---

## G3 — U.S. EPA: Composting Yard Trimmings and Municipal Solid Waste

**Organization:** United States Environmental Protection Agency  
**Type:** Government technical document

**Source:**  
https://archive.epa.gov/composting/web/pdf/cytmsw.pdf

### Why it is useful

Contains technical information on:

- yard-trimming feedstocks,
- C:N ratios,
- moisture,
- temperature,
- aeration,
- green versus brown plant material,
- decomposition-rate factors.

### Applicable sub-types

- Yard / green waste
- Plant and crop residues

---

## G4 — USDA NRCS: National Engineering Handbook, Part 637, Chapter 2 — Composting

**Organization:** U.S. Department of Agriculture, Natural Resources Conservation Service  
**Type:** Government engineering guidance

**Source:**  
https://directives.nrcs.usda.gov/sites/default/files2/1720464003/Chapter%202%20-%20Composting.pdf

### Why it is useful

Provides technical guidance on composting fundamentals, including:

- microbial activity,
- carbon and nitrogen balance,
- moisture management,
- aeration,
- composting phases,
- feedstock properties.

The document recommends an initial C:N range of approximately 20:1 to 40:1 for rapid composting.

### Applicable sub-types

- Food / kitchen waste
- Fruit and vegetable waste
- Yard / green waste
- Plant and crop residues

---

# 5. Peer-Reviewed Sources

## P1 — Food-Waste Composting and Microbial Community

**Citation:**  
Wang, X., Pan, S., Zhang, Z., Lin, X., Zhang, Y., & Chen, S. (2017). *Effects of the feeding ratio of food waste on fed-batch aerobic composting and its microbial community*. Bioresource Technology, 224, 397–404.

**DOI:** 10.1016/j.biortech.2016.11.076

**Source:**  
https://doi.org/10.1016/j.biortech.2016.11.076

### Key relevance

The study links food-waste composting performance with moisture, temperature, and microbial succession. It reports Firmicutes, Proteobacteria, Bacteroidetes, and Actinobacteria among the dominant phyla and identifies temperature as an important environmental factor associated with succession.

### Applicable sub-types

- Food / kitchen waste

---

## P2 — Review of Microbes in Solid-Waste Composting

**Citation:**  
Rastogi, M., Nandal, M., & Khosla, B. (2020). *Microbes as vital additives for solid waste composting*. Heliyon, 6(2), e03343.

**DOI:** 10.1016/j.heliyon.2020.e03343

**Source:**  
https://doi.org/10.1016/j.heliyon.2020.e03343

### Key relevance

Review article covering microbial succession, municipal and food waste composting, microbial additives, degradation-rate factors, and compost quality.

### Applicable sub-types

- Food / kitchen waste
- Fruit and vegetable waste
- Yard / green waste
- Plant and crop residues

---

## P3 — Hydrolytically Active Microorganisms in Food-Waste Composting

**Citation:**  
Mironov, V., Zhukov, V., Efremova, K., & Brinton, W. F. (2024). *Enhancing aerobic composting of food waste by adding hydrolytically active microorganisms*. Frontiers in Microbiology, 15, 1487165.

**DOI:** 10.3389/fmicb.2024.1487165

**Source:**  
https://doi.org/10.3389/fmicb.2024.1487165

### Key relevance

Discusses food-waste degradation and compost-associated hydrolytic microorganisms, including bacterial and fungal groups studied in food-waste composting.

### Applicable sub-types

- Food / kitchen waste
- Fruit and vegetable waste

---

## P4 — Post-Consumption Food-Waste Composting

**Citation:**  
Wang, Q., Li, N., Jiang, S., Li, G., Yuan, J., Li, Y., Chang, R., & Gong, X. (2024). *Composting of post-consumption food waste enhanced by bioaugmentation with microbial consortium*. Science of the Total Environment, 907, 168107.

**DOI:** 10.1016/j.scitotenv.2023.168107

**Source:**  
https://doi.org/10.1016/j.scitotenv.2023.168107

### Key relevance

Examines microbial-community succession and humification during post-consumption food-waste composting, including associations between thermophilic groups and organic-matter degradation.

### Applicable sub-types

- Food / kitchen waste

---

## P5 — Vegetable-Waste Composting and Fungal Communities

**Citation:**  
Lu, X., Yang, Y., Hong, C., Zhu, W., Yao, Y., Zhu, F., Hong, L., & Wang, W. (2022). *Optimization of vegetable waste composting and the exploration of microbial mechanisms related to fungal communities during composting*. Journal of Environmental Management, 319, 115694.

**DOI:** 10.1016/j.jenvman.2022.115694

**Source:**  
https://doi.org/10.1016/j.jenvman.2022.115694

### Key relevance

Studies vegetable-waste composting and microbial succession. Reported taxa include Firmicutes, *Saccharomonospora*, *Aspergillus*, *Thermomyces*, and *Microascus*.

### Applicable sub-types

- Fruit and vegetable waste

---

## P6 — Rotary-Drum Composting of Vegetable Waste

**Citation:**  
Sudharsan Varma, V., & Kalamdhad, A. S. (2014). *Stability and microbial community analysis during rotary drum composting of vegetable waste*. International Journal of Recycling of Organic Waste in Agriculture, 3, 52.

**DOI:** 10.1007/s40093-014-0052-4

**Source:**  
https://doi.org/10.1007/s40093-014-0052-4

### Key relevance

Reports microbial-population changes during vegetable-waste composting, including mesophilic microorganisms, thermophilic stages, fungi, actinomycetes, and compost stability.

### Applicable sub-types

- Fruit and vegetable waste

---

## P7 — Household Fruit-and-Vegetable Waste Decomposition

**Citation:**  
Jirawatcharadech, P., & Sanongkiet, S. (2026). *Development of a household composting method for fruit and vegetable waste using a combination of decomposer bacteria and hydrolytic enzymes*. Environmental Technology & Innovation, 42, 104902.

**DOI:** 10.1016/j.eti.2026.104902

**Source:**  
https://doi.org/10.1016/j.eti.2026.104902

### Key relevance

Examines household fruit-and-vegetable waste decomposition and hydrolytic microbial activity.

### Applicable sub-types

- Fruit and vegetable waste

---

## P8 — Microbial Succession During Green-Waste Composting

**Citation:**  
Liu, L., Wang, S., Guo, X., Zhao, T., & Zhang, B. (2018). *Succession and diversity of microorganisms and their association with physicochemical properties during green waste thermophilic composting*. Waste Management, 73, 101–112.

**DOI:** 10.1016/j.wasman.2017.12.026

**Source:**  
https://doi.org/10.1016/j.wasman.2017.12.026

### Key relevance

Investigates bacterial diversity and environmental factors during green-waste composting. Reported dominant phyla include Firmicutes, Chloroflexi, and Proteobacteria.

### Applicable sub-types

- Yard / green waste

---

## P9 — Review of Green-Waste Compost Microbiomes

**Citation:**  
Parab, C., Yadav, K. D., & Prajapati, V. (2023). *Genomics and microbial dynamics in green waste composting: A mini review*. Ecological Genetics and Genomics, 29, 100206.

**DOI:** 10.1016/j.egg.2023.100206

**Source:**  
https://doi.org/10.1016/j.egg.2023.100206

### Key relevance

Reviews microbial-community dynamics across mesophilic, thermophilic, cooling, and maturation stages of green-waste composting.

### Applicable sub-types

- Yard / green waste
- Plant and crop residues

---

## P10 — Green Soybean Hull and Maize-Straw Composting

**Citation:**  
Zhang, C., Gao, Z., Shi, W., Li, L., Tian, R., Huang, J., Lin, R., Wang, B., & Zhou, B. (2020). *Material conversion, microbial community composition and metabolic functional succession during green soybean hull composting*. Bioresource Technology, 316, 123823.

**DOI:** 10.1016/j.biortech.2020.123823

**Source:**  
https://doi.org/10.1016/j.biortech.2020.123823

### Key relevance

Useful for lignocellulosic plant residues. The study reports stage-dependent bacterial and fungal succession and identifies *Thermomyces* and *Aspergillus* as important in lignocellulose degradation.

### Applicable sub-types

- Plant and crop residues

---

## P11 — Co-Composting Food-Waste Digestate and Garden Waste

**Citation:**  
Wang, X., He, X., & Liang, J. (2022). *Succession of Microbial Community during the Co-Composting of Food Waste Digestate and Garden Waste*. International Journal of Environmental Research and Public Health, 19(16), 9945.

**DOI:** 10.3390/ijerph19169945

**Source:**  
https://doi.org/10.3390/ijerph19169945

### Key relevance

Provides evidence for mixed food and garden feedstocks and reports succession of bacterial and fungal communities during composting.

### Applicable sub-types

- Food / kitchen waste
- Yard / green waste
- Plant and crop residues

---

## P12 — Corn-Straw Composting and Environmental Variables

**Citation:**  
Meng, Q., Yang, W., Men, M., Bello, A., Xu, X., Xu, B., Deng, L., Jiang, X., Sheng, S., Wu, X., Han, Y., & Zhu, H. (2019). *Microbial Community Succession and Response to Environmental Variables During Cow Manure and Corn Straw Composting*. Frontiers in Microbiology, 10, 529.

**DOI:** 10.3389/fmicb.2019.00529

**Source:**  
https://doi.org/10.3389/fmicb.2019.00529

### Key relevance

Links microbial succession to environmental variables such as temperature, moisture, C:N ratio, pH, and nitrogen forms.

### Applicable sub-types

- Yard / green waste
- Plant and crop residues

---

# 6. General Evidence Summary for the Knowledge Base

The reviewed sources support several high-level principles:

1. **Composting is microbially driven.**
2. **Microbial communities change across composting stages.**
3. **Temperature is an important driver of microbial succession.**
4. **Moisture, oxygen, pH, particle size, and C:N balance influence decomposition.**
5. **Firmicutes are frequently associated with thermophilic stages.**
6. **Actinobacteria and fungi are often important during later-stage degradation and maturation, especially for complex plant material.**
7. **Food and vegetable wastes often have high moisture and may need carbon-rich structural material for effective aerobic composting.**
8. **The exact microbial community varies with feedstock, composting system, additives, and environmental conditions.**

Because microbial communities vary between studies, the project should avoid presenting one microorganism as universally “best” for a waste type.

Instead, the recommendation engine should distinguish between:

- **literature-reported microbial groups,**
- **general composting conditions,**
- **specific experimental findings,**
- **general waste-management guidance.**

---

# 7. Fields to Extract for Day 15

The next phase should convert the literature into structured database-ready records.

| Field | Example |
|---|---|
| `waste_subtype` | fruit_vegetable |
| `treatment_method` | aerobic composting |
| `microbial_group` | Firmicutes |
| `organism_or_taxon` | Bacillus spp. |
| `role` | degradation of readily available organic matter |
| `compost_stage` | thermophilic |
| `temperature_context` | study-reported |
| `moisture_context` | study-reported |
| `ph_context` | study-reported |
| `cn_ratio_context` | study-reported |
| `evidence_type` | peer-reviewed experimental study |
| `source_ref` | P3 |
| `doi` | DOI identifier |
| `notes` | short evidence summary |

---

# 8. Evidence-Handling Rules

When adding information to the recommendation database:

- Do not invent microbial properties.
- Do not infer a precise temperature, pH, or decomposition duration from an unrelated feedstock.
- Record whether a value came from a specific experiment or general guidance.
- Prefer ranges supported by multiple sources.
- Keep the source ID/DOI with every knowledge-base record.
- Do not treat correlation between a taxon and a composting stage as proof that the taxon alone caused decomposition.
- Keep household composting guidance separate from controlled research experiments.
- Update references when the knowledge base is expanded.

---

# 9. Day 14 Completion Checklist

- [x] Initial biodegradable sub-types defined
- [x] Government composting sources identified
- [x] Peer-reviewed food-waste sources identified
- [x] Peer-reviewed fruit/vegetable sources identified
- [x] Peer-reviewed green-waste sources identified
- [x] Peer-reviewed plant-residue sources identified
- [x] At least 6 credible sources mapped to each sub-type
- [x] DOI/source links recorded
- [x] Evidence-handling rules documented
- [ ] Database records created
- [ ] Microbial recommendation engine implemented
