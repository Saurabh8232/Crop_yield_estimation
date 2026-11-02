from flask import Flask, jsonify
from flask_cors import CORS

from backend.config import DATA_PATH, DATABASE_PATH, METRICS_PATH
from backend.database.db import initialize
from backend.routes.analytics import bp as analytics_bp
from backend.routes.health import bp as health_bp
from backend.routes.history import bp as history_bp
from backend.routes.options import bp as options_bp
from backend.routes.prediction import bp as prediction_bp
from backend.services.data_service import DataService
from backend.services.model_service import ModelService


def create_app(test_config=None) -> Flask:
    app = Flask(__name__)
    app.config.from_mapping(
        DATABASE_PATH=DATABASE_PATH,
        METRICS_PATH=METRICS_PATH,
    )
    if test_config:
        app.config.update(test_config)

    CORS(
        app,
        resources={
            r"/api/*": {
                "origins": ["https://crop-yield-estimation-ten.vercel.app"],
                "methods": ["GET", "POST", "OPTIONS"],
            }
        },
    )

    initialize(app.config["DATABASE_PATH"])
    app.extensions["model_service"] = ModelService()
    app.extensions["data_service"] = DataService(DATA_PATH)

    app.register_blueprint(health_bp)
    app.register_blueprint(options_bp)
    app.register_blueprint(prediction_bp)
    app.register_blueprint(history_bp)
    app.register_blueprint(analytics_bp)

    @app.errorhandler(404)
    def not_found(_error):
        return jsonify({"error": "Not found."}), 404

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=False)
