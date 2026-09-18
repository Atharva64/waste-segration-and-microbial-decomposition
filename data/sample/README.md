# Dataset Information

## AI-Based Waste Segregation and Microbial Decomposition Recommendation System

This directory contains documentation and small sample files related to the
waste-classification dataset used in this project.

The complete dataset is **not stored in this GitHub repository** because of
its large size.

---

## Primary Dataset

### Custom Waste Classification Dataset

**Source:** Kaggle  
**Author:** Wasif Mahmood  
**Dataset:** Custom Waste Classification Dataset

Dataset page:

https://www.kaggle.com/datasets/wasifmahmood01/custom-waste-classification-dataset

---

## Dataset Description

The dataset contains images from 9 waste categories:

1. E-Waste
2. Automobile Wastes
3. Battery Waste
4. Glass Waste
5. Light Bulbs
6. Metal Waste
7. Organic Waste
8. Paper Waste
9. Plastic Waste

The dataset contains:

- 9,213 training images
- 2,309 testing images

Total:

- 11,522 images

---

## Classes Used in This Project

The first version of our project will use six main waste categories:

| Original Dataset Class | Project Class |
|---|---|
| Organic Waste | Biodegradable |
| Plastic Waste | Plastic |
| Paper Waste | Paper |
| Glass Waste | Glass |
| Metal Waste | Metal |
| E-Waste | E-Waste |

The following classes are not initially included:

- Automobile Wastes
- Battery Waste
- Light Bulbs

These classes may be added later as future enhancements.

---

## Project Classification Classes

```text
biodegradable
plastic
paper
glass
metal
e-waste
