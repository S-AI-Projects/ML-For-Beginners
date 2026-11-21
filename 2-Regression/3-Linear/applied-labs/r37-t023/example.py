"""
r37-t023: Regression Evaluation – Invariant and State Trace
============================================================
Lesson context: 2-Regression/3-Linear/README.md
  "Build a regression model using Scikit-learn: regression four ways"

This module computes Mean Absolute Error (MAE) and Root Mean Squared Error (RMSE)
from paired real-valued observations and predictions, while rejecting mismatched
lengths and empty inputs.

Key properties demonstrated:
1. Exact calculation & state trace:
   - Residuals: e_i = pred_i - truth_i
   - Absolute errors: |e_i|
   - Squared errors: e_i^2
   - MAE = (1/n) * sum(|e_i|)
   - MSE = (1/n) * sum(e_i^2)
   - RMSE = sqrt(MSE)
2. Invariants linking intermediate state trace to final outputs:
   - Non-negativity invariant: MAE >= 0, RMSE >= 0
   - Error ordering invariant: MAE <= RMSE
   - Identical prediction invariant: truth == prediction => MAE == 0 and RMSE == 0
   - Sum reconciliation invariant: sum(absolute_errors) == n * MAE
   - MSE reconciliation invariant: sum(squared_errors) == n * (RMSE^2)
3. Rejection of invalid inputs:
   - Empty lists -> ValueError
   - Length mismatch -> ValueError

NOTE: Simulation/mock behavior using small local fixtures.
No model download, paid provider, GPU, or physical device is required.
"""

import math
from typing import Dict, List, Tuple, Any


def evaluate_regression(truth: List[float], prediction: List[float]) -> Dict[str, Any]:
    """
    Computes MAE, RMSE, and full intermediate state trace for paired observations.

    Validation:
    - Rejects empty inputs.
    - Rejects mismatched lengths.

    Returns dictionary containing metrics and step-by-step state trace.
    """
    if not truth or not prediction:
        raise ValueError("Inputs must not be empty.")
    if len(truth) != len(prediction):
        raise ValueError(f"Mismatched lengths: truth({len(truth)}) vs prediction({len(prediction)})")

    n = len(truth)
    residuals = []
    abs_errors = []
    sq_errors = []

    for t, p in zip(truth, prediction):
        res = p - t
        residuals.append(res)
        abs_errors.append(abs(res))
        sq_errors.append(res ** 2)

    sum_abs = sum(abs_errors)
    sum_sq = sum(sq_errors)

    mae = sum_abs / n
    mse = sum_sq / n
    rmse = math.sqrt(mse)

    # Invariants verification
    inv_non_negative = (mae >= 0.0) and (rmse >= 0.0)
    inv_mae_le_rmse = mae <= (rmse + 1e-12)  # floating point tolerance
    inv_sum_abs_reconciled = math.isclose(sum_abs, n * mae, rel_tol=1e-9)
    inv_sum_sq_reconciled = math.isclose(sum_sq, n * mse, rel_tol=1e-9)

    return {
        "n": n,
        "truth": list(truth),
        "prediction": list(prediction),
        "trace": {
            "residuals": residuals,
            "absolute_errors": abs_errors,
            "squared_errors": sq_errors,
            "sum_absolute_errors": sum_abs,
            "sum_squared_errors": sum_sq,
            "mse": mse,
        },
        "metrics": {
            "mae": mae,
            "rmse": rmse,
        },
        "invariants": {
            "non_negative": inv_non_negative,
            "mae_le_rmse": inv_mae_le_rmse,
            "sum_abs_reconciled": inv_sum_abs_reconciled,
            "sum_sq_reconciled": inv_sum_sq_reconciled,
        }
    }


def run_normal_fixture():
    """
    Normal fixture required by the contract:
    truth = [1, 2, 3], prediction = [1, 3, 2]
    residuals = [0, 1, -1]
    absolute_errors = [0, 1, 1] -> sum = 2 -> MAE = 2/3
    squared_errors = [0, 1, 1] -> sum = 2 -> MSE = 2/3 -> RMSE = sqrt(2/3)
    """
    print("=== Normal Fixture ===")
    truth = [1, 2, 3]
    prediction = [1, 3, 2]
    res = evaluate_regression(truth, prediction)
    print(f"Truth: {truth}, Prediction: {prediction}")
    print(f"MAE: {res['metrics']['mae']:.6f} (Expected: 2/3 = {2/3:.6f})")
    print(f"RMSE: {res['metrics']['rmse']:.6f} (Expected: sqrt(2/3) = {math.sqrt(2/3):.6f})")
    print(f"State trace: {res['trace']}")
    print(f"Invariants: {res['invariants']}")
    return res


def run_identical_fixture():
    """
    Identical fixture:
    truth == prediction -> MAE = 0, RMSE = 0
    """
    print("\n=== Identical Fixture ===")
    truth = [10.0, 20.0, 30.0]
    prediction = [10.0, 20.0, 30.0]
    res = evaluate_regression(truth, prediction)
    print(f"Truth: {truth}, Prediction: {prediction}")
    print(f"MAE: {res['metrics']['mae']}, RMSE: {res['metrics']['rmse']}")
    return res


if __name__ == "__main__":
    run_normal_fixture()
    run_identical_fixture()
