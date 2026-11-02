# Final Prediction Scenario and Feature Audit

## Scope and evidence

This audit was performed without modifying either the original CSV or the
processed datasets. No records were removed and no model was trained.

Evidence reviewed:

- `crop_yield_model_ready.csv`
- `data/processed/crop_yield_model_ready.csv`
- `data/processed/crop_yield_cleaned.csv`
- `data/reports/dataset_summary.json`
- `data/reports/data_quality_report.json`
- `data/reports/cleaning_report.json`
- `data/reports/final_dataset_summary.json`
- `docs/DATASET_DOCUMENTATION.md`

The workspace contains no data dictionary, source URL, README from the
dataset creator, query files, field-unit metadata, collection protocol, or
documentation describing when the measurements were available.

## 1. Yield measurement unit

The target column is `Yield`. Its unit **cannot be established from the
available evidence**.

The CSV contains no unit suffix, unit column, area column, production column,
or definition of whether `Yield` means yield per hectare, total production, or
another measure. The local documentation also explicitly records the unit as
unspecified. The value range (`0.01` to `17,500`) is not sufficient to infer a
unit safely because several different agricultural measures could produce
similar numeric ranges.

**Conclusion:** the yield unit is **unknown**. It must be confirmed from the
dataset creator or an authoritative source before reporting physical
quantities, comparing results with external benchmarks, or claiming practical
forecast accuracy.

## 2. Region redundancy verification

`Region` is completely redundant with `District` and `State` in the available
records.

Verification over all **197,241** records found:

```text
Region == District + ", " + State: 197,241 records
Mismatches: 0
```

Examples follow the same deterministic format, such as:

```text
District: Anantapur
State: Andhra Pradesh
Region: Anantapur, Andhra Pradesh
```

`Region` is therefore excluded from model predictors. This is a feature
selection decision only; no records are removed.

## 3. Weather-field provenance and timing

### Temperature

The `temp_src` values are:

| Source label | Records |
|---|---:|
| `NASA_POWER` | 144,830 |
| `NASA_climatic_normal` | 52,411 |

NASA POWER's official temporal API documentation distinguishes climatology,
monthly, daily, and hourly products. Its climatology products provide values
for a predefined period, while monthly, daily, and hourly products have
different temporal meanings:

<https://power.larc.nasa.gov/docs/services/api/temporal/>

However, this dataset does not contain the NASA POWER request URL, parameter
name, temporal endpoint, averaging period, coordinates, or extraction script.
Therefore:

- `NASA_climatic_normal` is consistent with a climatological normal or
  long-period average.
- `NASA_POWER` alone does **not** establish whether the value is daily,
  monthly, annual, reanalysis-derived, or otherwise aggregated.
- There is no evidence that these values are operational forecasts.
- There is no evidence that the values are actual field measurements.

### Rainfall

The `rain_src` values are:

| Source label | Records |
|---|---:|
| `ICRISAT_gauge` | 175,028 |
| `NASA_POWER` | 17,624 |
| `ICRISAT_30yr_normal` | 4,589 |

`ICRISAT_gauge` suggests a gauge-derived source by its label, and
`ICRISAT_30yr_normal` explicitly suggests a 30-year normal. These labels do
not document the observation dates, aggregation period, gauge location, or
whether the value was available before the associated yield was known.

The `NASA_POWER` rainfall values have the same unresolved temporal extraction
as the temperature values. The dataset does not prove that rainfall is a
forecast or a season-total observation.

### Humidity

There is no `humidity_src` column. The dataset contains only the numeric
`Humidity` field, so its source, temporal aggregation, measurement method, and
availability time cannot be established from the workspace.

### Weather conclusion

The available evidence supports a cautious conclusion:

```text
The weather fields are historical or climatological covariates of mixed,
partly undocumented temporal resolution. They are not demonstrably
pre-season forecasts, and they are not demonstrably direct field observations
for each crop-year record.
```

They must not be described as forecasts without additional source metadata.

## 4. Fertilizer and pesticide semantics

### Fertilizer

`Fertilizer` is numeric, but there is no fertilizer unit, product definition,
application date, number of applications, treated area, or collection method.
The value cannot be classified as planned quantity or actual applied quantity.

**Conclusion:** fertilizer timing and semantics are unknown.

### Pesticide

`Pesticide` is numeric and has a `pest_src` provenance label:

| Source label | Records |
|---|---:|
| `FAOSTAT_India` | 111,438 |
| `FAOSTAT_India_backfilled` | 85,803 |

The label indicates the provenance category used by the dataset, and
`FAOSTAT_India_backfilled` indicates a backfilled provenance label. It does
not establish the unit, whether the number is a farm-level application,
regional usage, a rate, or another statistic. It also does not establish
whether the quantity was planned or actually applied to the crop represented
by the row.

**Conclusion:** pesticide timing and semantics are unknown.

## 5. Final feature treatment

| Column | Classification | Model decision | Reason |
|---|---|---|---|
| `record_id` | Identifier | Exclude | Traceability only; not a predictive input |
| `Year` | Candidate predictor | Keep provisionally | Known for a historical record; use depends on the intended scenario |
| `State` | Valid predictor | Keep | Geographic context |
| `District` | Valid predictor | Keep | More detailed geographic context |
| `Region` | Redundant/leakage-prone | Exclude | Exactly derived from `District` and `State` in all records |
| `Crop` | Valid predictor | Keep | Crop identity is required for crop-specific yield estimation |
| `Season` | Valid predictor | Keep | Season context |
| `Temperature` | Candidate predictor | Keep provisionally | Numeric weather covariate, but timing and aggregation are undocumented |
| `Rainfall` | Candidate predictor | Keep provisionally | Numeric weather covariate, but timing and aggregation are undocumented |
| `Humidity` | Candidate predictor | Keep provisionally | Numeric weather covariate, but source and timing are undocumented |
| `Soil Type` | Valid predictor | Keep | Soil context |
| `pH` | Candidate predictor | Keep provisionally | Soil measurement; timing and measurement protocol are undocumented |
| `Nitrogen` | Candidate predictor | Keep provisionally | Soil/input variable; unit and timing are undocumented |
| `Phosphorus` | Candidate predictor | Keep provisionally | Soil/input variable; unit and timing are undocumented |
| `Potassium` | Candidate predictor | Keep provisionally | Soil/input variable; unit and timing are undocumented |
| `Fertilizer` | Timing-dependent predictor | Keep only for retrospective/conditional scenario | Planned versus actual application is unknown |
| `Pesticide` | Timing-dependent predictor | Keep only for retrospective/conditional scenario | Planned versus actual application is unknown |
| `Yield` | Target | Use as target only | Numeric target; unit is unknown |
| `temp_src` | Provenance/metadata | Exclude | Source indicator can encode collection or imputation regime |
| `rain_src` | Provenance/metadata | Exclude | Source indicator can encode collection or imputation regime |
| `pest_src` | Provenance/metadata | Exclude | Includes backfilled source category and can create source leakage |

No additional records are removed. The dataset's outliers and flagged
observations remain available for later evaluation.

## 6. Prediction-time availability

The following fields are plausibly known before a crop season begins:

- `State`
- `District`
- `Crop`
- `Season`
- `Soil Type`, if mapped or previously measured
- `pH`, `Nitrogen`, `Phosphorus`, and `Potassium`, if soil testing occurs
  before planting
- `Year`

The following are timing-sensitive:

- `Temperature`
- `Rainfall`
- `Humidity`
- `Fertilizer`
- `Pesticide`

Their presence in a row does not prove they were available at prediction
time. Weather may be a historical aggregate or climatological normal rather
than a forecast. Fertilizer and pesticide may describe realized inputs rather
than pre-season plans. Using them for a pre-season model without resolving
their timing would produce a different task from the one the data can
defensibly support.

## 7. Pre-season versus during-season implications

### Pre-season prediction

A pre-season model should use only information known before planting, such as
location, crop, season, soil information, historical climate summaries, and
explicitly available planned inputs. This dataset does not provide enough
metadata to prove that its weather values are forecasts or that its input
quantities are pre-season plans. It therefore cannot currently support a
validated operational pre-season forecast claim.

### During-season prediction

A during-season model could use observed weather and realized applications
through a declared cutoff date. This dataset has no dates, week/month fields,
observation timestamps, or cutoff definition. It cannot establish a
during-season forecasting horizon either.

### Retrospective season-level estimation

A retrospective model can use the row's season-level covariates to estimate
or explain the yield associated with a historical crop/geography/season
record. This does not claim that all predictors were known before harvest.
It is the least assumption-heavy interpretation supported by the available
data.

## Recommendation

The most realistic current scenario is:

> **Retrospective, season-level tabular crop-yield estimation for historical
> crop–district–season records, not an operational pre-season or
> during-season forecast.**

For the ANN experiment, use the following provisional inputs:

```text
Year
State
District
Crop
Season
Temperature
Rainfall
Humidity
Soil Type
pH
Nitrogen
Phosphorus
Potassium
Fertilizer
Pesticide
```

Exclude:

```text
record_id
Region
temp_src
rain_src
pest_src
Yield
```

This recommendation is conditional on explicitly labeling the experiment as
retrospective and reporting the yield unit as unknown. Before production or
pre-season claims, obtain the source data dictionary and confirm:

1. the `Yield` unit and definition;
2. the temporal aggregation and extraction method for all weather fields;
3. whether fertilizer and pesticide are planned or actually applied;
4. the timing at which every predictor becomes available.

ANN preprocessing and training should wait until this scenario and the
unknown-unit limitation are approved.
