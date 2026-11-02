# Frontend documentation

## Pages

- **Dashboard:** actual dataset counts, year range, ANN test metrics, crop and
  season charts.
- **Predict yield:** exact 15-feature form with backend-backed dropdowns,
  state-dependent districts, validation, and prediction result.
- **History:** saved prediction ID, crop, state, district, Yield, and timestamp.
- **Analytics:** year, state, and crop aggregations returned by Flask.
- **About model:** architecture, metrics, features, and limitations.

## Development

```powershell
Set-Location frontend
npm install
npm run dev
```

`frontend/.env` sets `VITE_API_BASE_URL=/api`. The Vite development proxy
forwards this path to `http://127.0.0.1:5000`. Components use the centralized
Axios service in `src/services/api.js`.

## UI behavior

Loading, error, empty-history, disabled-district, and prediction-result states
are implemented. Yield is shown only in the dataset's native scale and the UI
states that its physical unit is unknown. No fake records or sensor readings
are generated.
