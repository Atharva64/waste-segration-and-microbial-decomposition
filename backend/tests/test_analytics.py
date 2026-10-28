import backend.app.api.analytics as analytics_api


def test_analytics_summary_returns_dashboard_data(
    client,
    monkeypatch,
):
    captured = {}

    def fake_get_analytics_summary(db, *, days):
        captured["days"] = days
        return {
            "days": days,
            "total_predictions": 3,
            "average_confidence": 0.9,
            "top_category": "plastic",
            "by_category": [
                {"slug": "plastic", "name": "Plastic", "count": 2},
                {"slug": "glass", "name": "Glass", "count": 1},
            ],
            "scans_per_day": [
                {"date": "2026-10-25", "count": 1},
                {"date": "2026-10-26", "count": 2},
            ],
            "feedback_total": 2,
            "feedback_correct": 1,
            "feedback_incorrect": 1,
        }

    monkeypatch.setattr(
        analytics_api,
        "get_analytics_summary",
        fake_get_analytics_summary,
    )

    response = client.get("/api/analytics/summary?days=2")

    assert response.status_code == 200
    assert captured["days"] == 2

    data = response.json()

    assert data["total_predictions"] == 3
    assert data["top_category"] == "plastic"
    assert data["scans_per_day"][1]["count"] == 2


def test_analytics_summary_rejects_invalid_days(client):
    response = client.get("/api/analytics/summary?days=0")

    assert response.status_code == 422
    assert response.json()["error"]["code"] == "validation_error"
