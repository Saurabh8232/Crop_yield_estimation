# Installation and execution

## Requirements

- Python with pip
- Node.js with npm

## Install

From the project root:

```powershell
python -m pip install -r backend\requirements.txt
Set-Location frontend
npm install
Set-Location ..
```

## Start the backend

```powershell
python -m backend.app
```

The Flask API listens on `http://127.0.0.1:5000`.

## Start the frontend

In a second terminal:

```powershell
Set-Location frontend
npm run dev
```

Open `http://127.0.0.1:5173`. The Vite proxy sends `/api` requests to Flask.

## Verify

```powershell
python -m pytest backend\tests -q
Set-Location frontend
npm run build
```

Do not run `train_ann.py` as part of application startup. The application
loads the existing artifacts in `models/` only.
