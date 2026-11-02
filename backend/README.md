# Flask backend

## Setup

From the project root:

```powershell
python -m pip install -r backend\requirements.txt
python -m pytest backend\tests
python -m backend.app
```

The API runs at `http://127.0.0.1:5000`. It loads the existing ANN artifacts
once at startup and stores prediction history in `backend/predictions.sqlite3`.

`POST /api/predict` requires the 15 fields listed by `GET /api/model-info`.
The response is in the dataset's native `Yield` scale; its physical unit is
unknown. This is retrospective historical estimation, not live or operational
forecasting.
