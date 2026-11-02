# Final project completion report

Completion date: 2026-11-02.

## Completed features

- Preserved processed datasets and saved ANN artifacts.
- Flask backend with one-time model/preprocessor/scaler loading.
- Exact 15-feature validation and prediction endpoint.
- Dataset-backed crop, state, district, and season options.
- Inverse target scaling to native Yield scale.
- SQLite prediction history.
- Dataset-derived analytics APIs.
- React/Vite dashboard, prediction form, history, analytics, and model pages.
- Centralized Axios integration and Vite development proxy.
- Loading, error, validation, and empty states.
- Project, architecture, API, frontend, execution, testing, and limitation
  documentation.

## Verified components

- Model, preprocessor, and target scaler loaded successfully.
- Backend routes responded successfully.
- Frontend production bundle built successfully.
- Vite development server served the application.
- Genuine dataset-row prediction completed through the live API.
- Prediction was inverse-scaled, returned to the frontend API response, saved
  to SQLite, and retrieved from history.
- Unknown categorical values were accepted by the persisted encoder as
  designed.

## Test results

- Backend: `3 passed`.
- Live API route checks: all required GET routes HTTP 200.
- Validation: missing and invalid numeric input HTTP 422.
- Frontend build: passed.
- Empty history: passed in an isolated SQLite database.
- Browser automation: unverified; not configured.

The genuine integration prediction returned
`220.1598579261754` in the dataset's native Yield scale. This value is an
observed test response from the saved model, not a hardcoded or fabricated
result. Test rows were cleaned from the project database afterward.

## Integrity

SHA-256 hashes recorded before and after integration were unchanged:

| Artifact | SHA-256 |
|---|---|
| `data/processed/crop_yield_model_ready.csv` | `82C21E96176F8BC9B3D4349A39A74B72352802273E1F306A33B25628B57C818B` |
| `models/ann_model.joblib` | `672EDC2AD6C042337A99B706D656536DFF1636EFE2E799E710D2594AA5AC7B48` |
| `models/ann_preprocessor.joblib` | `0AAA77B9804436700DDFA4E9B72E853E097908C9931153CC158E0D9C78632AD2` |
| `models/ann_target_scaler.joblib` | `F5DF52E2FA011AD70CA6C543494F42D5C60BCC70F45D87DE7A79279C4111040D` |

No model retraining, original dataset modification, feature reclassification,
or fabricated historical record creation occurred.

## Known issues

- Vite reports a bundle-size advisory above 500 kB.
- Browser-level interaction and visual responsive checks remain unautomated.
- Yield unit remains unknown.

## Scientific limitations and future scope

This application is retrospective historical estimation only. It is not an
operational pre-season or during-season forecasting system and does not claim
real-time IoT functionality. Future work should validate units and semantics,
compare baselines, add model/version governance, and treat ESP32 integration
as future scope.
