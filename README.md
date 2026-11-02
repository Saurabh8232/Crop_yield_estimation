# Crop Yield Estimation System

This project estimates historical, season-level crop `Yield` from 15 approved
dataset features using a saved scikit-learn ANN model, a Flask API, and a
React/Vite dashboard.

**Scientific scope:** this is retrospective historical estimation, not an
operational pre-season or during-season forecasting system. The physical unit
of `Yield` is unknown in the source dataset. The project does not provide
real-time IoT functionality; ESP32 integration is future scope.

## Stack

- Python, pandas, scikit-learn, joblib, Flask, SQLite
- JavaScript, React, Vite, React Router, Axios, Recharts

## Run locally

```powershell
python -m pip install -r backend\requirements.txt
python -m backend.app
```

In another terminal:

```powershell
Set-Location frontend
npm install
npm run dev
```

Open `http://127.0.0.1:5173`.

## Main folders

- `data/processed/` - preserved processed datasets
- `models/` - saved ANN, preprocessor, and target scaler
- `backend/` - Flask application, services, routes, SQLite database, tests
- `frontend/` - React dashboard
- `docs/` - project, API, architecture, execution, testing, and limitation documentation
- `reports/` - ANN metrics and training report

See `docs/INSTALLATION_AND_EXECUTION.md` and
`docs/FINAL_PROJECT_COMPLETION_REPORT.md` for verified execution and
integration results.
