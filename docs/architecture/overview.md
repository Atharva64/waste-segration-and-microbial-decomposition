# System Architecture Overview

## AI-Based Waste Segregation and Microbial Decomposition Recommendation System

This document explains the overall architecture and data flow of the project.

---

## 1. System Overview

The system is designed to classify waste using Artificial Intelligence and provide appropriate waste-management recommendations.

A user uploads or captures an image of a waste item through the web application. The image is sent to the backend API, where it is processed and passed to the trained deep-learning model.

The AI model predicts the waste category and returns a confidence score.

Based on the predicted category, the system provides either:

- microbial decomposition information for biodegradable waste,
- recycling guidance for recyclable waste, or
- safe disposal recommendations for electronic waste.

The prediction and recommendation can also be stored in the database for history and analytics.

---

## 2. Main System Components

The project consists of the following major components:

### Frontend

The frontend will be developed using React.

Its main responsibilities are:

- image upload,
- webcam image capture,
- displaying predictions,
- showing confidence scores,
- showing recycling or decomposition information,
- displaying prediction history,
- presenting analytics through charts.

---

### Backend API

The backend will be developed using FastAPI.

The backend acts as the communication layer between:

- the React frontend,
- the AI model,
- the recommendation system,
- and the PostgreSQL database.

Main backend responsibilities include:

- receiving images,
- validating requests,
- preprocessing images,
- invoking the AI model,
- retrieving recommendations,
- storing prediction results,
- returning JSON responses.

---

### Image Preprocessing

Before an image is sent to the AI model, it will be processed.

Typical preprocessing operations include:

- image resizing,
- RGB conversion,
- normalization,
- image validation.

During training, additional data augmentation techniques may be used, including:

- random flipping,
- random rotation,
- random zoom,
- random contrast.

---

### AI Waste Classification Model

The AI component will use TensorFlow/Keras.

The initial model architecture will use transfer learning with MobileNetV3Small.

The planned waste classes are:

1. Biodegradable
2. Plastic
3. Paper
4. Glass
5. Metal
6. E-Waste

The model will generate:

- predicted waste category,
- confidence score.

Example:

```json
{
  "prediction": "Plastic",
  "confidence": 96.47
}
```
