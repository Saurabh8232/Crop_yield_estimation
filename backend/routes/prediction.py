from flask import Blueprint, current_app, jsonify, request

from backend.database.db import save_prediction
from backend.services.prediction_service import validate_inputs


bp = Blueprint("prediction", __name__)


@bp.post("/api/predict")
def predict():
    inputs, errors = validate_inputs(request.get_json(silent=True))
    if errors:
        return jsonify({"error": "Invalid prediction input.", "details": errors}), 422
    try:
        value = current_app.extensions["model_service"].predict(inputs)
        prediction_id = save_prediction(current_app.config["DATABASE_PATH"], inputs, value)
    except Exception:
        current_app.logger.exception("Prediction failed")
        return jsonify({"error": "Prediction failed."}), 500
    return jsonify(
        {
            "prediction_id": prediction_id,
            "predicted_yield": value,
            "yield_unit": "Unknown; not specified by the dataset documentation.",
            "limitations": [
                "Retrospective, season-level historical estimation only.",
                "Not an operational pre-season or during-season forecast.",
            ],
        }
    )
