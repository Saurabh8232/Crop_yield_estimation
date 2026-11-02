from flask import Blueprint, current_app, jsonify


bp = Blueprint("health", __name__)


@bp.get("/api/health")
def health():
    model_available = current_app.extensions["model_service"] is not None
    return jsonify({"status": "ok" if model_available else "degraded", "model_available": model_available})
