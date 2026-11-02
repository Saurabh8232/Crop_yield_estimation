# Agricultural Dataset Inspection Report

## Scope

This report documents a read-only inspection of `crop_yield_model_ready.csv`. The original CSV was not moved, modified, or deleted. No model was trained.

## Dataset identity

- **Path:** `crop_yield_model_ready.csv`
- **Records:** 197,241
- **Columns:** 20
- **File size:** 35,285,366 bytes
- **Observed year range:** 1966–2017

## Schema

### Columns and roles

| Column | Role/type | Missing | Unique | Notes |
|---|---|---:|---:|---|
| `Year` | numeric feature | 0 | 52 | Observed directly from the CSV. |
| `State` | categorical/provenance feature | 0 | 20 | Observed directly from the CSV. |
| `District` | categorical/provenance feature | 0 | 309 | Observed directly from the CSV. |
| `Region` | categorical/provenance feature | 0 | 309 | Geographic text that matches District + State in all rows. |
| `Crop` | categorical/provenance feature | 0 | 21 | Observed directly from the CSV. |
| `Season` | categorical/provenance feature | 0 | 3 | Observed directly from the CSV. |
| `Temperature` | numeric feature | 0 | 1,107 | Observed directly from the CSV. |
| `Rainfall` | numeric feature | 0 | 9,718 | Observed directly from the CSV. |
| `Humidity` | numeric feature | 0 | 564 | Observed directly from the CSV. |
| `Soil Type` | categorical/provenance feature | 0 | 6 | Observed directly from the CSV. |
| `pH` | numeric feature | 0 | 65 | Observed directly from the CSV. |
| `Nitrogen` | numeric feature | 0 | 8,204 | Observed directly from the CSV. |
| `Phosphorus` | numeric feature | 0 | 4,849 | Observed directly from the CSV. |
| `Potassium` | numeric feature | 0 | 3,195 | Observed directly from the CSV. |
| `Fertilizer` | numeric feature | 0 | 9,803 | Observed directly from the CSV. |
| `Pesticide` | numeric feature | 0 | 16 | Observed directly from the CSV. |
| `Yield` | numeric feature | 0 | 87,154 | Numeric target; unit not specified. |
| `temp_src` | categorical/provenance feature | 0 | 2 | Source/provenance label; includes normal/backfill labels. |
| `rain_src` | categorical/provenance feature | 0 | 3 | Source/provenance label; includes normal/backfill labels. |
| `pest_src` | categorical/provenance feature | 0 | 2 | Source/provenance label; includes normal/backfill labels. |

### Numeric features

`Year`, `Temperature`, `Rainfall`, `Humidity`, `pH`, `Nitrogen`, `Phosphorus`, `Potassium`, `Fertilizer`, and `Pesticide` are numeric input candidates. `Yield` is numeric and is the target.

### Categorical features

`State`, `District`, `Region`, `Crop`, `Season`, and `Soil Type` are categorical input candidates. `temp_src`, `rain_src`, and `pest_src` are categorical provenance fields rather than direct agronomic measurements.

## Missing values and duplicates

- **Missing cells:** 0 across all columns.
- **Exact duplicate records:** 0.
- **Malformed rows:** 0; all rows contain 20 fields.

## Numerical distributions and outliers

The full quantile summaries are in `data/reports/dataset_summary.json`. Tukey IQR flags are statistical review indicators, not proof of bad data.

| Column | Minimum | Median | Mean | Maximum | IQR flags |
|---|---:|---:|---:|---:|---:|
| `Year` | 1966.0 | 1993.0 | 1992.122733 | 2017.0 | 0 |
| `Temperature` | -2.84 | 25.99 | 25.578893 | 29.12 | 10,798 |
| `Rainfall` | 7.0 | 902.7 | 1019.632822 | 8409.0 | 9,628 |
| `Humidity` | 24.6 | 53.0 | 54.405088 | 83.4 | 0 |
| `pH` | 5.6 | 6.9 | 7.063624 | 8.0 | 0 |
| `Nitrogen` | 0.0 | 30.86 | 45.813354 | 470.97 | 6,930 |
| `Phosphorus` | 0.0 | 12.2 | 17.424425 | 251.16 | 5,432 |
| `Potassium` | 0.0 | 2.78 | 7.288305 | 222.54 | 21,936 |
| `Fertilizer` | 0.0 | 48.69 | 70.526093 | 804.53 | 5,212 |
| `Pesticide` | 0.09 | 0.39 | 0.3453 | 0.44 | 0 |
| `Yield` | 0.01 | 793.63 | 1222.530324 | 17500.0 | 17,912 |

Notable observations:

- `Yield`, `Rainfall`, `Nitrogen`, `Phosphorus`, `Potassium`, and `Fertilizer` are highly right-skewed by their quantiles and standard deviations.
- `Temperature` has 382 negative values. These are flagged for domain validation, not automatically classified as invalid because the unit and geographic interpretation are undocumented.
- `pH` values are between 5.6 and 8.0; `Humidity` values are between 24.6 and 83.4.

## Categorical distributions

The complete value counts are stored in `data/reports/dataset_summary.json`. The most frequent values are:

- **State:** Uttar Pradesh (31,761), Madhya Pradesh (26,470), Maharashtra (19,748), Rajasthan (17,337), Karnataka (14,431)
- **District:** Dharwad (979), Belgaum (978), Osmanabad (942), Gulbarga Kalaburagi (929), Chitradurga (919)
- **Region:** Dharwad, Karnataka (979), Belgaum, Karnataka (978), Osmanabad, Maharashtra (942), Gulbarga Kalaburagi, Karnataka (929), Chitradurga, Karnataka (919)
- **Crop:** Rice (14,476), Chickpea (13,446), Maize (13,366), Sugarcane (13,253), Wheat (13,227)
- **Season:** Kharif (107,700), Rabi (58,311), Whole Year (31,230)
- **Soil Type:** Vertisols (66,412), Inceptisols (56,852), Alfisols (33,989), Mollisols (18,443), Aridisols (13,033)
- **temp_src:** NASA_POWER (144,830), NASA_climatic_normal (52,411)
- **rain_src:** ICRISAT_gauge (175,028), NASA_POWER (17,624), ICRISAT_30yr_normal (4,589)
- **pest_src:** FAOSTAT_India (111,438), FAOSTAT_India_backfilled (85,803)

## Invalid values and structural checks

- Negative temperature values: **382**; review required.
- Negative values in non-negative candidate fields: **0**.
- Humidity outside 0–100: **0**.
- pH outside the generic 0–14 scale: **0**.
- Non-positive yield values: **0**.
- Years outside the observed 1966–2017 range: **0**.
- Region not matching `District, State`: **0**.

## Target variable and unit

`Yield` is the likely supervised-learning target because it is numeric and is explicitly named `Yield`. The CSV does **not** specify its unit, whether it is yield per area, total production, or another definition. No unit is assumed in this inspection. The target unit and measurement definition must be confirmed before modeling or reporting results.

This dataset should not be confused with crop recommendation: crop recommendation predicts a crop choice, while this dataset supports estimating a numeric yield conditional on crop, location, season, environmental, soil, and input variables.

## Provenance and estimated observations

The only provenance evidence available in the workspace is the source-label columns:

- `temp_src`: NASA_POWER (144,830) and NASA_climatic_normal (52,411).
- `rain_src`: ICRISAT_gauge (175,028), NASA_POWER (17,624), and ICRISAT_30yr_normal (4,589).
- `pest_src`: FAOSTAT_India (111,438) and FAOSTAT_India_backfilled (85,803).

Based on labels containing `backfill` or `normal`, 85,803 records have at least one such source label. This is a provenance flag, not proof that the value itself was algorithmically imputed. No external source URLs, license, collection protocol, creator, or data dictionary were found in the workspace.

## Suitability for deep learning

The dataset is **structurally suitable for a supervised tabular yield-estimation experiment**: it has 197,241 rows, a numeric target candidate, mixed numeric/categorical inputs, and no missing cells or exact duplicates. Its size is potentially adequate for deep learning, although a strong tree-based baseline should be evaluated before using a neural network.

Limitations prevent treating it as production-ready without additional validation:

1. The target unit and yield definition are undocumented.
2. Provenance is partial, and some values are labeled normal-based or backfilled.
3. Source fields may introduce source-related leakage or distribution shifts.
4. Negative temperatures and extreme/heavy-tailed values require domain validation.
5. `Region` duplicates information encoded by `District` and `State`.
6. Repeated geography/crop/year contexts may cause leakage under random splitting; use a time- or group-aware evaluation design.
7. No external documentation establishes licensing, collection methods, or measurement quality.

## Generated artifacts

- `data/reports/dataset_summary.json` - measured schema, distributions, categorical counts, provenance, and target/feature notes.
- `data/reports/data_quality_report.json` - missingness, duplicates, validation checks, outlier flags, and recommendations.
- `docs/DATASET_DOCUMENTATION.md` - this human-readable inspection report.
