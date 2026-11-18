"""Compare MAE and RMSE on three controlled toy configurations.

Scope: controlled toy configurations, not a measure of real-world model
accuracy.

Prerequisites: Python 3 standard library and a local checkout. The local
fixture is mandatory; any optional real-service extension needs separately
supplied credentials/hardware and is not part of this task.
"""
import math

TRUTH = [1, 2, 3, 4]

CONFIGS = (
    ("A", "uniform error", [2, 3, 4, 5]),
    ("B", "one outlier", [1, 2, 3, 8]),
    ("C", "small error", [1.5, 2.5, 3.5, 4.5]),
)


def _check(truth, prediction):
    if len(truth) != len(prediction):
        raise ValueError("truth and prediction must have equal length")
    if not truth:
        raise ValueError("inputs must be non-empty")


def mae(truth, prediction):
    """Mean absolute error, in the same units as the target."""
    _check(truth, prediction)
    errors = [abs(t - p) for t, p in zip(truth, prediction)]
    return sum(errors) / len(errors)


def rmse(truth, prediction):
    """Root mean squared error, in the same units as the target."""
    _check(truth, prediction)
    squares = [(t - p) ** 2 for t, p in zip(truth, prediction)]
    return math.sqrt(sum(squares) / len(squares))


def compare():
    """Return (key, name, MAE, RMSE) for each configuration."""
    rows = []
    for key, name, prediction in CONFIGS:
        rows.append((key, name, mae(TRUTH, prediction),
                     rmse(TRUTH, prediction)))
    return rows


def main():
    head_mae = mae([1, 2, 3], [1, 3, 2])
    head_rmse = rmse([1, 2, 3], [1, 3, 2])
    print(f"Headline: MAE {head_mae:.4f}, RMSE {head_rmse:.4f}")
    print("Config  Name            MAE     RMSE")
    rows = compare()
    for key, name, m, r in rows:
        print(f"{key:<7} {name:<15} {m:.4f}  {r:.4f}")
    a, b = rows[0], rows[1]
    print(f"Trade-off: A and B share MAE {a[2]:.4f};"
          f" B RMSE {b[3]:.4f} vs A {a[3]:.4f}")


if __name__ == "__main__":
    main()
