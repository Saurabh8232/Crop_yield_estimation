# System architecture

```text
React/Vite dashboard
        |
        | Axios /api/*
        v
Flask application
  routes -> services -> saved artifacts
        |                 |
        v                 v
     SQLite          ANN model + preprocessor + target scaler
        ^
        |
processed CSV -> DataService options and analytics
```

## Backend

- `backend/app.py` creates the Flask app and loads the model service once.
- `routes/` exposes health, options, prediction, history, and analytics APIs.
- `services/model_service.py` transforms input with the persisted
  `ColumnTransformer`, predicts with `MLPRegressor`, and inverse-scales Yield.
- `services/data_service.py` reads the processed dataset for actual options and
  grouped analytics.
- `database/db.py` stores prediction input JSON, predicted Yield, and UTC time
  in SQLite.

## Frontend

React Router provides Dashboard, Predict, History, Analytics, and About Model
pages. Axios is centralized in `src/services/api.js`. Vite proxies `/api` to
Flask during development. Recharts renders only values returned by the
analytics API.

## Integrity boundary

The frontend never loads or modifies model artifacts. The backend never
re-trains during a request. The original and processed datasets remain
read-only application inputs.
