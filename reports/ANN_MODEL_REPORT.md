# ANN Model Development Report

## Scenario

This model estimates historical crop yield at the retrospective, season-level
record level. It is **not** an operational pre-season or during-season
forecasting model.

The target is `Yield`. Its physical unit is **unknown** because the dataset
does not provide a unit or target definition. Metric values below are therefore
reported in the dataset's native target scale, without assigning a physical
unit.

## Inputs

The ANN uses these 15 predictors:

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

Excluded from predictors:

```text
record_id
Region
temp_src
rain_src
pest_src
```

`record_id` is retained only for traceability. `Region` is excluded because it
is exactly redundant with `District` and `State`. Source columns are retained
in the dataset but excluded from model inputs to reduce provenance and
backfill-related leakage risk.

## Leakage-safe preprocessing

- Numeric predictors were standardized with `StandardScaler`, fitted only on
  the training partition.
- Categorical predictors were one-hot encoded with
  `OneHotEncoder(handle_unknown="ignore")`, fitted only on the training
  partition.
- The target was standardized using a scaler fitted only on training targets.
- No records were removed or synthesized.

## Chronological split

| Partition | Years | Records |
|---|---:|---:|
| Training | 1966–2011 | 178,433 |
| Validation | 2012–2014 | 11,148 |
| Test | 2015–2017 | 7,660 |

The test set contains later historical years than the training set. It should
not be interpreted as a guarantee of future operational performance.

## ANN configuration

- Implementation: `sklearn.neural_network.MLPRegressor`
- Hidden layers: 64 and 32 neurons
- Activation: ReLU
- Optimizer: Adam
- Epochs: 40
- Batch size: 1,024
- Random seed: 42

## Measured results

| Partition | MAE | RMSE | R² |
|---|---:|---:|---:|
| Training | 216.3145 | 365.6806 | 0.9366 |
| Validation | 367.3294 | 588.0670 | 0.8740 |
| Test | 423.3793 | 736.4141 | 0.8096 |

These are genuine results produced by reopening the processed dataset,
training the configured ANN, and evaluating predictions on the held-out
chronological partitions. They are expressed in the dataset's unknown native
`Yield` scale.

## Saved artifacts

- `models/ann_model.joblib`
- `models/ann_preprocessor.joblib`
- `models/ann_target_scaler.joblib`
- `reports/ann_metrics.json`
- `reports/ann_training_history.json`
- `reports/plots/ann_training_validation_loss.png`
- `reports/plots/ann_actual_vs_predicted.png`

## Limitations

1. The `Yield` unit and measurement definition are unknown.
2. Weather aggregation and exact availability timing are undocumented.
3. Fertilizer and pesticide values are not documented as planned or actual
   applications.
4. The model is retrospective and season-level, not an operational forecast.
5. The chronological test covers 2015–2017 historical records and does not
   establish performance under future climate, management, or distribution
   shifts.
6. Outliers and quality-flagged observations were retained; no automatic
   agricultural observation deletion was performed.
7. Source and backfill metadata were excluded from predictors, but the
   underlying source construction may still affect model generalization.
8. A strong non-neural baseline and domain validation should be compared before
   selecting this ANN for practical use.
