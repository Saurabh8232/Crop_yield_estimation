from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = ROOT_DIR / "data" / "processed" / "crop_yield_model_ready.csv"
MODEL_DIR = ROOT_DIR / "models"
DATABASE_PATH = ROOT_DIR / "backend" / "predictions.sqlite3"
METRICS_PATH = ROOT_DIR / "reports" / "ann_metrics.json"

FEATURES = [
    "Year",
    "Temperature",
    "Rainfall",
    "Humidity",
    "pH",
    "Nitrogen",
    "Phosphorus",
    "Potassium",
    "Fertilizer",
    "Pesticide",
    "State",
    "District",
    "Crop",
    "Season",
    "Soil Type",
]
NUMERIC_FEATURES = FEATURES[:10]
CATEGORICAL_FEATURES = FEATURES[10:]
TARGET = "Yield"
