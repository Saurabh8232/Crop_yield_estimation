# Backend API documentation

The Flask backend uses the saved ANN model and preprocessing artifacts without
retraining. The `Yield` unit is unknown and is never represented as kg/ha or
tonnes/ha. The system estimates retrospective, season-level historical records;
it is not an operational pre-season or during-season forecasting service.

## Run

```powershell
python -m pip install -r backend\requirements.txt
python -m backend.app
```

## Endpoints

| Method | Path | Response |
|---|---|---|
| GET | `/api/health` | Backend/model availability |
| GET | `/api/crops` | Dataset crop names |
| GET | `/api/states` | Dataset states |
| GET | `/api/districts?state=...` | Dataset districts, optionally filtered |
| GET | `/api/seasons` | Dataset seasons |
| POST | `/api/predict` | Prediction and saved prediction ID |
| GET | `/api/model-info` | Model, features, metrics, and limitations |
| GET | `/api/history?limit=100` | Saved predictions |
| GET | `/api/analytics` | Dataset and prediction statistics |

## Prediction request

Send JSON with these exact fields:

```json
{
  "Year": 1966,
  "State": "Andhra Pradesh",
  "District": "Anantapur",
  "Crop": "Castor",
  "Season": "Kharif",
  "Temperature": 25.85,
  "Rainfall": 623.8,
  "Humidity": 59.9,
  "Soil Type": "Alfisols",
  "pH": 6.2,
  "Nitrogen": 2.8,
  "Phosphorus": 0.28,
  "Potassium": 0,
  "Fertilizer": 3.07,
  "Pesticide": 0.44
}
```

The response includes `predicted_yield`, `prediction_id`, and
`yield_unit: "Unknown; not specified by the dataset documentation."`.
Missing fields, non-numeric numeric values, and empty/non-string categorical
values return HTTP 422. Unknown categorical strings are accepted because the
saved encoder was trained with `handle_unknown="ignore"`.

Prediction history stores the input JSON, prediction, and UTC timestamp in
SQLite. No historical predictions are fabricated or inserted.
