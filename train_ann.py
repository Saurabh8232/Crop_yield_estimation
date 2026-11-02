import json
import warnings
from pathlib import Path

import joblib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.neural_network import MLPRegressor
from sklearn.preprocessing import OneHotEncoder, StandardScaler


ROOT = Path(__file__).resolve().parent
DATA_PATH = ROOT / "data" / "processed" / "crop_yield_model_ready.csv"
MODEL_DIR = ROOT / "models"
REPORT_DIR = ROOT / "reports"
PLOT_DIR = REPORT_DIR / "plots"
MODEL_DIR.mkdir(exist_ok=True)
REPORT_DIR.mkdir(exist_ok=True)
PLOT_DIR.mkdir(parents=True, exist_ok=True)

TARGET = "Yield"
NUMERIC_FEATURES = [
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
]
CATEGORICAL_FEATURES = [
    "State",
    "District",
    "Crop",
    "Season",
    "Soil Type",
]
FEATURES = NUMERIC_FEATURES + CATEGORICAL_FEATURES
EXCLUDED = ["record_id", "Region", "temp_src", "rain_src", "pest_src"]


def metrics(y_true, y_pred):
    return {
        "mae": float(mean_absolute_error(y_true, y_pred)),
        "rmse": float(np.sqrt(mean_squared_error(y_true, y_pred))),
        "r2": float(r2_score(y_true, y_pred)),
    }


def main():
    df = pd.read_csv(DATA_PATH)
    required = FEATURES + [TARGET, "record_id"]
    missing = sorted(set(required) - set(df.columns))
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    train = df[df["Year"] <= 2011].copy()
    validation = df[df["Year"].between(2012, 2014)].copy()
    test = df[df["Year"] >= 2015].copy()
    if train.empty or validation.empty or test.empty:
        raise ValueError("Chronological split produced an empty partition.")

    preprocessor = ColumnTransformer(
        transformers=[
            ("numeric", StandardScaler(), NUMERIC_FEATURES),
            (
                "categorical",
                OneHotEncoder(handle_unknown="ignore", sparse_output=True),
                CATEGORICAL_FEATURES,
            ),
        ],
        remainder="drop",
    )
    x_train = preprocessor.fit_transform(train[FEATURES])
    x_validation = preprocessor.transform(validation[FEATURES])
    x_test = preprocessor.transform(test[FEATURES])

    target_scaler = StandardScaler()
    y_train = target_scaler.fit_transform(train[[TARGET]]).ravel()
    y_validation = target_scaler.transform(validation[[TARGET]]).ravel()
    y_test = target_scaler.transform(test[[TARGET]]).ravel()

    model = MLPRegressor(
        hidden_layer_sizes=(64, 32),
        activation="relu",
        solver="adam",
        batch_size=1024,
        learning_rate_init=0.001,
        max_iter=1,
        warm_start=True,
        shuffle=True,
        random_state=42,
    )

    history = {"epoch": [], "train_loss": [], "validation_loss": []}
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        for epoch in range(1, 41):
            model.fit(x_train, y_train)
            train_pred_scaled = model.predict(x_train)
            validation_pred_scaled = model.predict(x_validation)
            history["epoch"].append(epoch)
            history["train_loss"].append(float(mean_squared_error(y_train, train_pred_scaled)))
            history["validation_loss"].append(
                float(mean_squared_error(y_validation, validation_pred_scaled))
            )

    train_pred = target_scaler.inverse_transform(
        model.predict(x_train).reshape(-1, 1)
    ).ravel()
    validation_pred = target_scaler.inverse_transform(
        model.predict(x_validation).reshape(-1, 1)
    ).ravel()
    test_pred = target_scaler.inverse_transform(
        model.predict(x_test).reshape(-1, 1)
    ).ravel()

    result = {
        "scenario": "Retrospective, season-level historical crop-yield estimation",
        "target": TARGET,
        "yield_unit": "Unknown; not specified by the dataset documentation.",
        "features": FEATURES,
        "excluded_columns": EXCLUDED,
        "split": {
            "method": "Chronological by Year",
            "train_years": [1966, 2011],
            "validation_years": [2012, 2014],
            "test_years": [2015, 2017],
            "train_records": int(len(train)),
            "validation_records": int(len(validation)),
            "test_records": int(len(test)),
        },
        "preprocessing": {
            "numeric": "StandardScaler fitted on training records only",
            "categorical": "OneHotEncoder(handle_unknown='ignore') fitted on training records only",
            "target": "StandardScaler fitted on training records only",
            "record_removal": "None",
        },
        "model": {
            "implementation": "sklearn.neural_network.MLPRegressor",
            "architecture": [64, 32],
            "activation": "relu",
            "optimizer": "adam",
            "epochs": 40,
            "batch_size": 1024,
            "random_state": 42,
        },
        "metrics": {
            "train": metrics(train[TARGET], train_pred),
            "validation": metrics(validation[TARGET], validation_pred),
            "test": metrics(test[TARGET], test_pred),
        },
        "limitations": [
            "Yield unit and definition are unknown, so metric magnitudes have no confirmed physical unit.",
            "This is retrospective historical estimation, not operational pre-season or during-season forecasting.",
            "Weather temporal aggregation and input timing are undocumented.",
            "Fertilizer and pesticide semantics and timing are undocumented.",
            "Source and backfill metadata were excluded from predictors to reduce leakage risk.",
            "The chronological test evaluates later historical years, not future operational deployment.",
            "No records were removed; outliers and quality flags remain in the data.",
        ],
        "artifacts": {
            "model": "models/ann_model.joblib",
            "preprocessor": "models/ann_preprocessor.joblib",
            "target_scaler": "models/ann_target_scaler.joblib",
            "training_history": "reports/ann_training_history.json",
            "metrics": "reports/ann_metrics.json",
            "loss_plot": "reports/plots/ann_training_validation_loss.png",
            "actual_predicted_plot": "reports/plots/ann_actual_vs_predicted.png",
        },
    }

    joblib.dump(model, MODEL_DIR / "ann_model.joblib")
    joblib.dump(preprocessor, MODEL_DIR / "ann_preprocessor.joblib")
    joblib.dump(target_scaler, MODEL_DIR / "ann_target_scaler.joblib")
    (REPORT_DIR / "ann_training_history.json").write_text(
        json.dumps(history, indent=2) + "\n", encoding="utf-8"
    )
    (REPORT_DIR / "ann_metrics.json").write_text(
        json.dumps(result, indent=2) + "\n", encoding="utf-8"
    )

    plt.figure(figsize=(8, 5))
    plt.plot(history["epoch"], history["train_loss"], label="Training MSE")
    plt.plot(history["epoch"], history["validation_loss"], label="Validation MSE")
    plt.xlabel("Epoch")
    plt.ylabel("Scaled target MSE")
    plt.title("ANN Training and Validation Loss")
    plt.legend()
    plt.tight_layout()
    plt.savefig(PLOT_DIR / "ann_training_validation_loss.png", dpi=150)
    plt.close()

    plt.figure(figsize=(7, 7))
    plt.scatter(test[TARGET], test_pred, s=5, alpha=0.25)
    limits = [
        min(float(test[TARGET].min()), float(test_pred.min())),
        max(float(test[TARGET].max()), float(test_pred.max())),
    ]
    plt.plot(limits, limits, "r--", label="Ideal prediction")
    plt.xlabel("Actual Yield")
    plt.ylabel("Predicted Yield")
    plt.title("ANN Actual vs Predicted Yield — Chronological Test Set")
    plt.legend()
    plt.tight_layout()
    plt.savefig(PLOT_DIR / "ann_actual_vs_predicted.png", dpi=150)
    plt.close()

    print(json.dumps(result["metrics"], indent=2))


if __name__ == "__main__":
    main()
