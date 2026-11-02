import json

import pandas as pd
import pytest

from backend.app import create_app
from backend.config import FEATURES


@pytest.fixture()
def client(tmp_path):
    app = create_app({"TESTING": True, "DATABASE_PATH": tmp_path / "predictions.sqlite3"})
    return app.test_client()


def genuine_input():
    row = pd.read_csv("data/processed/crop_yield_model_ready.csv").iloc[0]
    return {name: row[name].item() if hasattr(row[name], "item") else row[name] for name in FEATURES}


def test_health_and_options(client):
    assert client.get("/api/health").status_code == 200
    assert client.get("/api/crops").get_json()["crops"]
    assert client.get("/api/states").get_json()["states"]
    assert client.get("/api/districts").get_json()["districts"]
    assert client.get("/api/seasons").get_json()["seasons"]


def test_prediction_history_and_unknown_category(client):
    payload = genuine_input()
    payload["Crop"] = "Unseen crop"
    response = client.post("/api/predict", data=json.dumps(payload), content_type="application/json")
    assert response.status_code == 200
    assert isinstance(response.get_json()["predicted_yield"], float)
    history = client.get("/api/history").get_json()["predictions"]
    assert len(history) == 1


def test_prediction_validation(client):
    payload = genuine_input()
    payload.pop("Year")
    assert client.post("/api/predict", json=payload).status_code == 422
    payload = genuine_input()
    payload["Year"] = "not a number"
    assert client.post("/api/predict", json=payload).status_code == 422


def test_cors_headers_on_api_responses_and_preflight(client):
    origin = "https://crop-yield-estimation-ten.vercel.app"
    response = client.get("/api/health", headers={"Origin": origin})
    assert response.status_code == 200
    assert response.headers["Access-Control-Allow-Origin"] == origin

    preflight = client.options(
        "/api/predict",
        headers={
            "Origin": origin,
            "Access-Control-Request-Method": "POST",
            "Access-Control-Request-Headers": "content-type",
        },
    )
    assert preflight.status_code == 200
    assert preflight.headers["Access-Control-Allow-Origin"] == origin
    assert "POST" in preflight.headers["Access-Control-Allow-Methods"]

    not_found = client.get("/api/not-found", headers={"Origin": origin})
    assert not_found.status_code == 404
    assert not_found.headers["Access-Control-Allow-Origin"] == origin
