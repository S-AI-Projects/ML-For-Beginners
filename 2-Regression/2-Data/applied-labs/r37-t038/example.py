"""MAE and RMSE for paired observations and predictions (standard library only).

For paired values (truth_i, prediction_i), the residual is
    e_i = prediction_i - truth_i
    MAE  = mean(|e_i|)
    RMSE = sqrt(mean(e_i ** 2))
Both are in the SAME UNITS as the values being predicted (RMSE is not squared
units, because of the square root). RMSE punishes large errors more than MAE.

Documented invalid / missing-data cases (each raises ValueError):
    - different lengths for truth and prediction
    - empty inputs
    - a missing value (None or NaN), or infinity
    - a non-number (e.g. a string) or a bool
The functions keep no state, so the next valid call works normally
(recovery). evaluate_batch shows this: a bad case is reported and the batch
carries on.

Simulation: hand-written numbers, not predictions from a trained model.
"""
import math


def _check(name, values):
    for i, v in enumerate(values):
        if v is None:
            raise ValueError(f"{name}[{i}] is missing (None)")
        if isinstance(v, bool) or not isinstance(v, (int, float)):
            raise ValueError(f"{name}[{i}] is not a number: {v!r}")
        if not math.isfinite(v):
            raise ValueError(f"{name}[{i}] is not finite: {v!r}")


def mae_rmse(truth, prediction):
    """Return (mae, rmse). Raises ValueError on invalid input."""
    if len(truth) != len(prediction):
        raise ValueError(
            f"length mismatch: truth has {len(truth)} values, prediction has {len(prediction)}"
        )
    if len(truth) == 0:
        raise ValueError("inputs must not be empty")
    _check("truth", truth)
    _check("prediction", prediction)
    residuals = [p - t for t, p in zip(truth, prediction)]
    n = len(residuals)
    mae = sum(abs(e) for e in residuals) / n
    rmse = math.sqrt(sum(e * e for e in residuals) / n)
    return mae, rmse


def evaluate_batch(cases):
    """Run several (name, truth, prediction) cases; a bad case is recorded, not fatal."""
    results = []
    for name, truth, prediction in cases:
        try:
            mae, rmse = mae_rmse(truth, prediction)
            results.append({"case": name, "ok": True, "mae": mae, "rmse": rmse})
        except ValueError as exc:
            results.append({"case": name, "ok": False, "error": str(exc)})
    return results


DEMO_CASES = [
    ("valid", [1, 2, 3], [1, 3, 2]),
    ("missing value", [1, 2, 3], [1, None, 2]),
    ("recovery: valid again", [1, 2, 3], [1, 3, 2]),
    ("identical", [1, 2, 3], [1, 2, 3]),
    ("length mismatch", [1, 2, 3], [1, 2]),
    ("empty", [], []),
]

if __name__ == "__main__":
    for r in evaluate_batch(DEMO_CASES):
        if r["ok"]:
            print(f"{r['case']}: MAE={r['mae']:.4f} RMSE={r['rmse']:.4f}")
        else:
            print(f"{r['case']}: ERROR {r['error']}")
