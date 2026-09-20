from types import SimpleNamespace

import backend.app.api.predict as predict_api


def test_predict_rejects_invalid_content_type(client):
    response = client.post(
        "/api/predict",
        files={
            "image": (
                "notes.txt",
                b"not-an-image",
                "text/plain",
            )
        },
    )

    assert response.status_code == 415
    assert response.json()["error"]["code"] == "http_error"


def test_predict_returns_prediction_json(
    client,
    monkeypatch,
):
    def fake_predict_image_bytes(image_bytes):
        return {
            "predicted_class": "plastic",
            "confidence": 0.91,
            "probabilities": {
                "biodegradable": 0.01,
                "e-waste": 0.01,
                "glass": 0.01,
                "metal": 0.02,
                "paper": 0.04,
                "plastic": 0.91,
            },
            "model_name": "MobileNetV3Small",
        }

    def fake_save_prediction(
        db,
        *,
        filename,
        prediction_result,
    ):
        return SimpleNamespace(id=123)

    monkeypatch.setattr(
        predict_api,
        "predict_image_bytes",
        fake_predict_image_bytes,
    )

    monkeypatch.setattr(
        predict_api,
        "save_prediction",
        fake_save_prediction,
    )

    response = client.post(
        "/api/predict",
        files={
            "image": (
                "plastic.jpg",
                b"fake-image-bytes",
                "image/jpeg",
            )
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["prediction_id"] == 123
    assert data["filename"] == "plastic.jpg"
    assert data["predicted_class"] == "plastic"
    assert data["confidence"] == 0.91
    assert data["model_name"] == "MobileNetV3Small"
