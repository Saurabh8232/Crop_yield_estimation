import json

from flask import Blueprint, current_app

from backend.database.db import prediction_count


bp = Blueprint("analytics", __name__)


@bp.get("/api/model-info")
def model_info():
    with open(current_app.config["METRICS_PATH"], encoding="utf-8") as file:
        metrics = json.load(file)
    return {
        "model": metrics["model"],
        "features": metrics["features"],
        "target": metrics["target"],
        "yield_unit": metrics["yield_unit"],
        "metrics": metrics["metrics"],
        "limitations": metrics["limitations"],
    }


@bp.get("/api/analytics")
def analytics():
    return current_app.extensions["data_service"].analytics(
        prediction_count(current_app.config["DATABASE_PATH"])
    )
