from flask import Blueprint, current_app, request

from backend.database.db import list_predictions


bp = Blueprint("history", __name__)


@bp.get("/api/history")
def history():
    try:
        limit = min(max(int(request.args.get("limit", 100)), 1), 500)
    except ValueError:
        return {"error": "limit must be an integer."}, 422
    return {"predictions": list_predictions(current_app.config["DATABASE_PATH"], limit)}
