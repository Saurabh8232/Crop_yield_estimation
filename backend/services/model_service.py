import joblib
import pandas as pd

from backend.config import MODEL_DIR


class ModelService:
    def __init__(self) -> None:
        self.model = joblib.load(MODEL_DIR / "ann_model.joblib")
        self.preprocessor = joblib.load(MODEL_DIR / "ann_preprocessor.joblib")
        self.target_scaler = joblib.load(MODEL_DIR / "ann_target_scaler.joblib")

    def predict(self, inputs: dict) -> float:
        frame = pd.DataFrame([inputs])
        transformed = self.preprocessor.transform(frame)
        scaled_prediction = self.model.predict(transformed).reshape(-1, 1)
        prediction = self.target_scaler.inverse_transform(scaled_prediction)
        return float(prediction[0, 0])
