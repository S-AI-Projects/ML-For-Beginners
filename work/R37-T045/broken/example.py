"""Offline confusion-matrix lab: precision and recall.

offline mock adapter, not a real model service

Prerequisites

Python 3 standard library and a local checkout. The local fixture is
mandatory; any optional real-service extension needs separately
supplied credentials/hardware and is not part of this task.

Zero-denominator policy: precision is 0.0 when there are no positive
predictions (TP + FP == 0); recall is 0.0 when there are no actual
positives (TP + FN == 0).
"""

ZERO_DENOMINATOR_VALUE = 0.0

# Fixed predictions for the local fixture, one per input.
LOOKUP = {"a": 1, "b": 0, "c": 1, "d": 0}


def mock_adapter(x):
    """Return the fixed prediction for input x (deterministic, offline)."""
    return LOOKUP[x]


def _check_binary(values, name):
    for v in values:
        if v not in (0, 1):
            raise ValueError(f"{name} must contain only 0 or 1, got {v!r}")


def _ratio(num, den):
    if den == 0:
        return ZERO_DENOMINATOR_VALUE
    return num / den


def evaluate(y_true, inputs, predict):
    """Return confusion counts, precision and recall for predict(x)."""
    if len(y_true) != len(inputs):
        raise ValueError(
            f"length mismatch: {len(y_true)} labels, {len(inputs)} inputs")
    _check_binary(y_true, "y_true")
    y_pred = []
    for x in inputs:
        pred = predict(x)
        if pred not in (0, 1):
            raise ValueError(f"predict({x!r}) returned {pred!r}, not 0 or 1")
        y_pred.append(pred)
    pairs = list(zip(y_true, y_pred))
    tp = sum(1 for t, p in pairs if t == 1 and p == 1)
    fn = sum(1 for t, p in pairs if t == 1 and p == 0)
    fp = sum(1 for t, p in pairs if t == 0 and p == 1)
    tn = sum(1 for t, p in pairs if t == 0 and p == 0)
    return {
        "y_pred": y_pred,
        "tp": tp,
        "fn": fn,
        "fp": fp,
        "tn": tn,
        "precision": _ratio(tp, tp + fp),
        "recall": _ratio(tp, tp + fn),
    }


def main():
    y_true = [1, 1, 0, 0]
    inputs = ["a", "b", "c", "d"]
    r = evaluate(y_true, inputs, mock_adapter)
    print("offline mock adapter, not a real model service")
    print("inputs:  " + " ".join(inputs))
    print("y_true:  " + " ".join(map(str, y_true)))
    print("y_pred:  " + " ".join(map(str, r["y_pred"])))
    print(f"TP={r['tp']} FN={r['fn']} FP={r['fp']} TN={r['tn']}")
    print(f"precision={r['precision']} recall={r['recall']}")
    z = evaluate([1, 1, 0, 0], inputs, lambda x: 0)
    print("zero-denominator case (predict all 0):")
    print(f"  TP={z['tp']} FP={z['fp']} precision={z['precision']}")
    n = evaluate([0, 0, 0, 0], inputs, lambda x: 1)
    print("zero-denominator case (no actual positives):")
    print(f"  TP={n['tp']} FN={n['fn']} recall={n['recall']}")


if __name__ == "__main__":
    main()
