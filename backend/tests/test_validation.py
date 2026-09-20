def test_feedback_rating_must_be_1_to_5(client):
    response = client.post(
        "/api/feedback",
        json={
            "prediction_id": 1,
            "rating": 6,
            "was_prediction_correct": True,
        },
    )

    assert response.status_code == 422
    assert response.json()["error"]["code"] == "validation_error"


def test_correct_prediction_cannot_have_correction(client):
    response = client.post(
        "/api/feedback",
        json={
            "prediction_id": 1,
            "rating": 5,
            "was_prediction_correct": True,
            "corrected_category_id": 2,
        },
    )

    assert response.status_code == 422


def test_prediction_history_limit_validation(client):
    response = client.get(
        "/api/predictions?limit=101"
    )

    assert response.status_code == 422
