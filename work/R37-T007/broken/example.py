"""Worked example calculating MAE and RMSE with input-to-output breakdown.

Label: worked teaching example, not a scikit-learn training pipeline.

Prerequisites: Python 3 standard library and a local checkout. The local
fixture is mandatory; any optional real-service extension needs
separately supplied credentials/hardware and is not part of this task.

Contract:
- truth=[1, 2, 3], prediction=[1, 3, 2] -> MAE = 2/3, RMSE = sqrt(2/3).
- Identical arrays give MAE = 0.0 and RMSE = 0.0.
- Rejects mismatched lengths and empty inputs.
- Focus: Publishes a step-by-step worked input-to-output explanation and
  executes the exact example as a regression test.
"""

import math


def validate_inputs(truth, prediction):
    """Validate paired real-valued observations and predictions."""
    if not isinstance(truth, (list, tuple)) or not isinstance(prediction, (list, tuple)):
        raise TypeError("truth and prediction must be lists or tuples")
    if len(truth) == 0:
        raise ValueError("truth and prediction cannot be empty")
    if len(truth) != len(prediction):
        raise ValueError(f"mismatched lengths: truth has {len(truth)}, prediction has {len(prediction)}")
    for val in list(truth) + list(prediction):
        if type(val) is bool or not isinstance(val, (int, float)):
            raise TypeError(f"elements must be numeric real numbers, got {val!r}")
        if math.isnan(val) or math.isinf(val):
            raise ValueError(f"elements must be finite real numbers, got {val!r}")


def calculate_mae(truth, prediction):
    """Compute Mean Absolute Error: sum(|y - y_hat|) / n."""
    validate_inputs(truth, prediction)
    return sum(abs(t - p) for t, p in zip(truth, prediction)) / len(truth)


def calculate_rmse(truth, prediction):
    """Compute Root Mean Squared Error: sqrt(sum((y - y_hat)^2) / n)."""
    validate_inputs(truth, prediction)
    mse = sum((t - p) ** 2 for t, p in zip(truth, prediction)) / len(truth)
    return math.sqrt(mse)


def generate_worked_table(truth, prediction):
    """Generate row-by-row worked breakdown of errors, absolute errors, and squared errors."""
    validate_inputs(truth, prediction)
    rows = []
    for i, (t, p) in enumerate(zip(truth, prediction)):
        err = t - p
        abs_err = abs(err)
        sq_err = err ** 2
        rows.append({
            "index": i,
            "truth": t,
            "prediction": p,
            "error": err,
            "abs_error": abs_err,
            "sq_error": sq_err
        })
    return rows


def run_contract():
    """Run headline worked example and print input-to-output explanation."""
    lines = []
    lines.append("worked teaching example, not a scikit-learn training pipeline")
    truth = [1, 2, 3]
    prediction = [1, 3, 2]
    table = generate_worked_table(truth, prediction)
    mae = calculate_mae(truth, prediction)
    rmse = calculate_rmse(truth, prediction)

    lines.append("worked breakdown for truth=[1, 2, 3], prediction=[1, 3, 2]:")
    lines.append("  i | truth | pred | error (y - y_hat) | |error| | error^2")
    for r in table:
        lines.append(f"  {r['index']} | {r['truth']:<5} | {r['prediction']:<4} | {r['error']:<17} | {r['abs_error']:<7} | {r['sq_error']}")

    total_abs = sum(r['abs_error'] for r in table)
    total_sq = sum(r['sq_error'] for r in table)
    n = len(table)

    lines.append(f"  total absolute error = {total_abs}, n = {n} -> MAE = {total_abs}/{n} = {mae:.4f}")
    lines.append(f"  total squared error = {total_sq}, n = {n} -> MSE = {total_sq}/{n}, RMSE = sqrt({total_sq}/{n}) = {rmse:.4f}")

    # Identical check
    mae_id = calculate_mae([1, 2, 3], [1, 2, 3])
    rmse_id = calculate_rmse([1, 2, 3], [1, 2, 3])
    lines.append(f"identical arrays [1, 2, 3]: MAE = {mae_id:.4f}, RMSE = {rmse_id:.4f}")
    return "\n".join(lines)


if __name__ == "__main__":
    print(run_contract())
