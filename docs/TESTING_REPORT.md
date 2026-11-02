# Testing report

Test date: 2026-11-02.

## Passed

| Check | Result |
|---|---|
| Backend pytest suite | 3 passed |
| Flask startup and artifact loading | Passed |
| GET health, crops, states, districts, seasons | HTTP 200 |
| GET model-info, history, analytics | HTTP 200 |
| Missing prediction field | HTTP 422 |
| Invalid numeric type | HTTP 422 |
| Unknown categorical value | HTTP 200; persisted encoder handled it |
| Genuine dataset-row prediction | Passed |
| Inverse-scaled numeric prediction | Passed; returned `220.1598579261754` in native Yield scale |
| SQLite history insertion and retrieval | Passed |
| Empty history in isolated database | Passed |
| Frontend production build | Passed with Vite |
| Vite dev server response | HTTP 200 |

## End-to-end record

The live API test used the first genuine row of
`data/processed/crop_yield_model_ready.csv`, including its real crop, state,
district, season, categorical soil type, and numeric values. The response was
stored in SQLite and retrieved through `/api/history`. Test-generated rows
were removed afterward so the project database does not contain fabricated
historical records.

## Unverified or skipped

- Automated browser click-through and pixel-level responsive checks were not
  run because no browser automation tool is configured.
- No production deployment, load, or concurrency test was requested.
- No model retraining or data mutation test was run; those actions were
  intentionally not performed.

Vite emitted a bundle-size advisory above 500 kB; this is a warning, not a
build failure.
