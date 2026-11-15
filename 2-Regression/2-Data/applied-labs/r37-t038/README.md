# R37-T038: MAE and RMSE with a documented invalid-data case and recovery

Standard-library Python only. No model, download, GPU or paid service.

## Formulas
For pairs (truth, prediction), residual e = prediction - truth.
MAE = mean(|e|). RMSE = sqrt(mean(e^2)). Both are in the same units as the
values being predicted. RMSE penalises large errors more than MAE.

## Run
```
python3 2-Regression/2-Data/applied-labs/r37-t038/example.py
python3 -m unittest discover -s 2-Regression/2-Data/applied-labs/r37-t038 -p "test_*.py"
```

## Fixture and expected output
truth=[1,2,3], prediction=[1,3,2]: residuals 0, 1, -1 -> MAE = 2/3,
RMSE = sqrt(2/3). Identical arrays give both errors 0.

```text
valid: MAE=0.6667 RMSE=0.8165
missing value: ERROR prediction[1] is missing (None)
recovery: valid again: MAE=0.6667 RMSE=0.8165
identical: MAE=0.0000 RMSE=0.0000
length mismatch: ERROR length mismatch: truth has 3 values, prediction has 2
empty: ERROR inputs must not be empty
```

## Invalid or missing data (documented)
Each of these raises `ValueError` with a message naming the problem:
different lengths, empty inputs, a missing value (`None` or NaN), infinity,
or a non-number or bool. Example: prediction `[1, None, 2]` raises
"prediction[1] is missing (None)". The function keeps no state, so the very
next valid call works (see "recovery: valid again" above, which matches the
first line). `evaluate_batch` shows the pattern: report the bad case, carry on.

## Limits (simulation)
Hand-written numbers, not predictions from a trained model, so this says
nothing about any real model's error. Missing values are rejected, not
imputed or skipped; deciding how to handle them is up to the caller.
