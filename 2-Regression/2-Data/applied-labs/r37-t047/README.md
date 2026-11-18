# R37-T047: MAE and RMSE evaluation experiment

Applied lab for [Build a regression model using Scikit-learn: prepare and visualize data](../../README.md).

## Prerequisites

Python 3 standard library and a local checkout. The local fixture is mandatory; any optional real-service extension needs separately supplied credentials/hardware and is not part of this task.

**Label:** controlled toy configurations, not a measure of real-world model accuracy.

## Invocation

From the repository root:

```bash
python3 2-Regression/2-Data/applied-labs/r37-t047/example.py
python3 -m unittest discover -s 2-Regression/2-Data/applied-labs/r37-t047 -p "test_*.py"
```

## Fixture

- Headline pair: truth `[1, 2, 3]`, prediction `[1, 3, 2]`. Expected MAE 2/3, RMSE sqrt(2/3).
- Fixed truth for the experiment: `[1, 2, 3, 4]`.
- A "uniform error": prediction `[2, 3, 4, 5]`. Expected MAE 1.0, RMSE 1.0.
- B "one outlier": prediction `[1, 2, 3, 8]`. Expected MAE 1.0, RMSE 2.0.
- C "small error": prediction `[1.5, 2.5, 3.5, 4.5]`. Expected MAE 0.5, RMSE 0.5.

## Expected output

Real stdout of `example.py`:

```text
Headline: MAE 0.6667, RMSE 0.8165
Config  Name            MAE     RMSE
A       uniform error   1.0000  1.0000
B       one outlier     1.0000  2.0000
C       small error     0.5000  0.5000
Trade-off: A and B share MAE 1.0000; B RMSE 2.0000 vs A 1.0000
```

## Metrics and units

- MAE (mean absolute error) is the mean of `|truth - prediction|`.
- RMSE (root mean squared error) is the square root of the mean of `(truth - prediction)**2`.
- Both are in the same units as the target values. RMSE squares the residuals internally, then takes the square root, so its result is also in target units.

## Validation

- `truth` and `prediction` must have equal length, otherwise `ValueError`.
- Both inputs must be non-empty, otherwise `ValueError`. Two empty lists and one empty list both raise.

## Experiment and correctness check

`compare()` runs the three configurations A, B and C against the fixed truth list. `test_example.py` checks each configuration's MAE and RMSE against explicit hand-computed values (table in Fixture above). The tests also cover the headline pair, identical lists (0 and 0), a single-element pair, negative and float values, and the validation errors.

## Observed trade-off

A and B have the same MAE (1.0), but B's RMSE is 2.0 against A's 1.0. RMSE squares each residual, so the single large error in B is weighted more heavily. RMSE is at least MAE in every configuration, and the two are equal only when all absolute errors are equal (true for A and C).

## How it relates to the lesson

The lesson covers preparing data and visualizing it before a regression model is built. A regression model predicts numeric values, and evaluation compares those predictions with the actual values, pair by pair. This lab shows two common error measures on paired lists, in the units of the target.

## Where the simplifications stop

- No model is trained. The predictions are typed in by hand.
- No real data is used. The truth list is four values.
- Only three configurations are compared, chosen by hand.

A real evaluation would use a trained model and held-out data. None of that is done here.

## Limitations

- Standard library only. No model download, paid provider, GPU or device.
- The results describe these toy inputs only. They make no claim about real-world model accuracy, real hardware, cloud behavior or trained-model performance.
- The tests do not read files by path relative to the test file, so a copy of the folder elsewhere runs the same way.
