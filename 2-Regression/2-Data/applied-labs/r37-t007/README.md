# R37-T007: Regression Evaluation - Worked Example with Checks

**Label:** worked teaching example, not a scikit-learn training pipeline.

## Prerequisites

Python 3 standard library and a local checkout. The local fixture is mandatory; any optional real-service extension needs separately supplied credentials/hardware and is not part of this task.

## What It Is

A worked input-to-output regression evaluation module calculating Mean Absolute Error (MAE) and Root Mean Squared Error (RMSE) with a complete row-by-row numerical explanation and executable regression tests.

## Worked Input-to-Output Explanation

Given paired observations and predictions:
- `truth = [1, 2, 3]`
- `prediction = [1, 3, 2]`

### Row-by-Row Table

| $i$ | Observation ($y_i$) | Prediction ($\hat{y}_i$) | Error ($e_i = y_i - \hat{y}_i$) | Absolute Error ($|e_i|$) | Squared Error ($e_i^2$) |
|---|---|---|---|---|---|
| 0 | 1 | 1 | $1 - 1 = 0$ | $0$ | $0^2 = 0$ |
| 1 | 2 | 3 | $2 - 3 = -1$ | $|-1| = 1$ | $(-1)^2 = 1$ |
| 2 | 3 | 2 | $3 - 2 = 1$ | $|1| = 1$ | $1^2 = 1$ |
| **Sum** | | | | **2** | **2** |

### Formulas & Calculation

$$\text{MAE} = \frac{1}{n} \sum_{i=1}^n |y_i - \hat{y}_i| = \frac{0 + 1 + 1}{3} = \frac{2}{3} \approx 0.6667$$

$$\text{MSE} = \frac{1}{n} \sum_{i=1}^n (y_i - \hat{y}_i)^2 = \frac{0 + 1 + 1}{3} = \frac{2}{3}$$

$$\text{RMSE} = \sqrt{\text{MSE}} = \sqrt{\frac{2}{3}} \approx 0.8165$$

For identical arrays ($y_i = \hat{y}_i$), every residual is 0, giving $\text{MAE} = 0.0$ and $\text{RMSE} = 0.0$.

## Invocation

From the repository root:

```bash
python3 2-Regression/2-Data/applied-labs/r37-t007/example.py
```

Run unit tests from the repository root:

```bash
python3 -m unittest discover -s 2-Regression/2-Data/applied-labs/r37-t007 -p "test_*.py"
```

## Fixture and Expected Output

Expected CLI output:

```text
worked teaching example, not a scikit-learn training pipeline
worked breakdown for truth=[1, 2, 3], prediction=[1, 3, 2]:
  i | truth | pred | error (y - y_hat) | |error| | error^2
  0 | 1     | 1    | 0                 | 0       | 0
  1 | 2     | 3    | -1                | 1       | 1
  2 | 3     | 2    | 1                 | 1       | 1
  total absolute error = 2, n = 3 -> MAE = 2/3 = 0.6667
  total squared error = 2, n = 3 -> MSE = 2/3, RMSE = sqrt(2/3) = 0.8165
identical arrays [1, 2, 3]: MAE = 0.0000, RMSE = 0.0000
```

## Limitations

- Computes deterministic metrics on small hand-crafted numeric fixtures; no scikit-learn models are trained.
- No dataset loading or pandas DataFrame operations.
- Makes no claims about real hardware, cloud service behavior, or trained model performance.
