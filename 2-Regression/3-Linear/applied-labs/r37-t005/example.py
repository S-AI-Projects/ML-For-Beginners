"""Regression evaluation behind an offline service adapter.

Label: offline service adapter, not a remote cloud metrics service.

Prerequisites: Python 3 standard library and a local checkout. The local
fixture is mandatory; any optional real-service extension needs
separately supplied credentials/hardware and is not part of this task.

Contract:
- truth=[1, 2, 3], prediction=[1, 3, 2] -> MAE = 2/3, RMSE = sqrt(2/3).
- Identical arrays give MAE = 0.0 and RMSE = 0.0.
- Rejects mismatched lengths and empty inputs.
- External dependency is placed behind a callable adapter interface.
- Local adapter provides deterministic in-process evaluation.
"""

import math


def validate_arrays(truth, prediction):
    """Validate observation and prediction sequences."""
    if not isinstance(truth, (list, tuple)) or not isinstance(prediction, (list, tuple)):
        raise TypeError("truth and prediction must be lists or tuples")
    if len(truth) == 0:
        raise ValueError("truth and prediction cannot be empty")
    if len(truth) != len(prediction):
        raise ValueError(f"mismatched lengths: truth has {len(truth)}, prediction has {len(prediction)}")
    for val in list(truth) + list(prediction):
        if type(val) is bool or not isinstance(val, (int, float)):
            raise TypeError(f"values must be numeric, got {val!r}")
        if math.isnan(val) or math.isinf(val):
            raise ValueError(f"values must be finite real numbers, got {val!r}")


class LocalRegressionEvaluatorAdapter:
    """Deterministic in-process service adapter for regression evaluation."""

    def __call__(self, truth, prediction):
        return self.evaluate(truth, prediction)

    def evaluate(self, truth, prediction):
        """Compute MAE and RMSE from paired observations and predictions."""
        validate_arrays(truth, prediction)
        n = len(truth)
        errors = [t - p for t, p in zip(truth, prediction)]
        mae = sum(abs(e) for e in errors) / n
        mse = sum(e * e for e in errors) / n
        rmse = math.sqrt(mse)
        return {"mae": mae, "rmse": rmse, "count": n}


class RegressionEvaluationClient:
    """Client consuming regression metrics via an injected callable service adapter."""

    def __init__(self, service_adapter=None):
        self.adapter = service_adapter if service_adapter is not None else LocalRegressionEvaluatorAdapter()

    def evaluate(self, truth, prediction):
        return self.adapter(truth, prediction)


# Default module-level client
_default_client = RegressionEvaluationClient()


def evaluate(truth, prediction, adapter=None):
    """Module-level convenience function."""
    if adapter is not None:
        client = RegressionEvaluationClient(adapter)
    else:
        client = _default_client
    return client.evaluate(truth, prediction)


def run_contract():
    """Run headline contract cases and print metrics."""
    lines = []
    lines.append("offline service adapter, not a remote cloud metrics service")

    # Contract 1: [1, 2, 3] vs [1, 3, 2]
    res1 = evaluate([1, 2, 3], [1, 3, 2])
    lines.append(f"truth=[1, 2, 3], prediction=[1, 3, 2]:")
    lines.append(f"  MAE={res1['mae']:.4f} (expected 2/3 = {2/3:.4f})")
    lines.append(f"  RMSE={res1['rmse']:.4f} (expected sqrt(2/3) = {math.sqrt(2/3):.4f})")

    # Contract 2: Identical arrays
    res2 = evaluate([1, 2, 3], [1, 2, 3])
    lines.append(f"identical arrays [1, 2, 3]:")
    lines.append(f"  MAE={res2['mae']:.4f}, RMSE={res2['rmse']:.4f}")
    return "\n".join(lines)


if __name__ == "__main__":
    print(run_contract())
