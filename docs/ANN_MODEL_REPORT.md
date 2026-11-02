# ANN model report

## Model

- Implementation: `sklearn.neural_network.MLPRegressor`
- Hidden layers: `(64, 32)`
- Activation: ReLU
- Optimizer: Adam
- Training epochs: 40
- Batch size: 1,024
- Random state: 42
- Target: `Yield`

## Preprocessing

The saved `ColumnTransformer` applies `StandardScaler` to the 10 numeric
features and `OneHotEncoder(handle_unknown="ignore")` to the 5 categorical
features. The saved target `StandardScaler` is applied to training targets.
API predictions are inverse-transformed back to the dataset's native Yield
scale.

## Chronological evaluation

| Partition | Years | MAE | RMSE | R² |
|---|---:|---:|---:|---:|
| Train | 1966–2011 | 216.3145 | 365.6806 | 0.9366 |
| Validation | 2012–2014 | 367.3294 | 588.0670 | 0.8740 |
| Test | 2015–2017 | 423.3793 | 736.4141 | 0.8096 |

Metrics are in the dataset's unknown native Yield scale.

## Limitations

Yield unit and definition, weather timing, input timing, and future
generalization are undocumented or unproven. The chronological test is not
evidence of operational forecasting performance. See
`PROJECT_LIMITATIONS_AND_FUTURE_SCOPE.md`.

Artifacts are in `models/`; the source training configuration is in
`train_ann.py`. The model was not retrained during integration testing.
