import backend.app.api.history as history_api


def test_feedback_returns_404_for_missing_prediction(
    client,
    monkeypatch,
):
    def fake_create_feedback(db, payload):
        raise LookupError("Prediction not found.")

    monkeypatch.setattr(
        history_api,
        "create_feedback",
        fake_create_feedback,
    )

    response = client.post(
        "/api/feedback",
        json={
            "prediction_id": 999,
            "rating": 3,
            "was_prediction_correct": False,
            "comments": "Wrong prediction.",
        },
    )

    assert response.status_code == 404
    assert (
        response.json()["error"]["message"]
        == "Prediction not found."
    )
