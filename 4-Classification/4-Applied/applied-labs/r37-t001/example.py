"""Classification evaluation on fixed toy labels.

Label: minimal complete local example, not a trained classifier.

Prerequisites: Python 3 standard library and a local checkout. The local
fixture is mandatory; any optional real-service extension needs
separately supplied credentials/hardware and is not part of this task.

Lesson concept connection:
- y_true: Ground truth actual labels (1 = positive class, 0 = negative class).
- y_pred: Predicted labels output by classifier.
- TP (True Positive): Actual positive correctly predicted as positive.
- FN (False Negative): Actual positive incorrectly predicted as negative.
- FP (False Positive): Actual negative incorrectly predicted as positive.
- TN (True Negative): Actual negative correctly predicted as negative.
- precision: TP / (TP + FP), proportion of positive predictions that were correct.
- recall: TP / (TP + FN), proportion of actual positives that were captured.

Zero-denominator policy:
- precision is 0.0 when there are no positive predictions (TP + FP == 0).
- recall is 0.0 when there are no actual positives (TP + FN == 0).
"""

ZERO_DENOMINATOR_VALUE = 0.0


def validate_labels(y_true, y_pred):
    """Validate that inputs are non-empty, equal-length lists of binary 0/1 integers."""
    if not isinstance(y_true, (list, tuple)) or not isinstance(y_pred, (list, tuple)):
        raise TypeError("y_true and y_pred must be lists or tuples")
    if len(y_true) == 0:
        raise ValueError("y_true and y_pred cannot be empty")
    if len(y_true) != len(y_pred):
        raise ValueError("y_true and y_pred must have equal length")
    for val in list(y_true) + list(y_pred):
        if type(val) is not int or val not in (0, 1):
            raise ValueError(f"labels must be binary 0 or 1 integers, got {val!r}")


def confusion(y_true, y_pred):
    """Compute confusion matrix counts (TP, FN, FP, TN) for binary labels."""
    validate_labels(y_true, y_pred)
    tp = fn = fp = tn = 0
    for t, p in zip(y_true, y_pred):
        if t == 1 and p == 1:
            tp += 1
        elif t == 1 and p == 0:
            fn += 1
        elif t == 0 and p == 1:
            fp += 1
        else:
            tn += 1
    return tp, fn, fp, tn


def precision(y_true, y_pred):
    """Compute precision: TP / (TP + FP). Returns 0.0 when TP + FP == 0."""
    tp, fn, fp, tn = confusion(y_true, y_pred)
    denom = tp + fp
    if denom == 0:
        return ZERO_DENOMINATOR_VALUE
    return tp / denom


def recall(y_true, y_pred):
    """Compute recall: TP / (TP + FN). Returns 0.0 when TP + FN == 0."""
    tp, fn, fp, tn = confusion(y_true, y_pred)
    denom = tp + fn
    if denom == 0:
        return ZERO_DENOMINATOR_VALUE
    return tp / denom


def run_contract():
    """Run contract scenarios and return output string."""
    lines = []
    # Headline contract
    y_true_head = [1, 1, 0, 0]
    y_pred_head = [1, 0, 1, 0]
    tp, fn, fp, tn = confusion(y_true_head, y_pred_head)
    prec = precision(y_true_head, y_pred_head)
    rec = recall(y_true_head, y_pred_head)
    lines.append("headline: y_true=[1, 1, 0, 0], y_pred=[1, 0, 1, 0]")
    lines.append(f"  TP={tp} FN={fn} FP={fp} TN={tn}")
    lines.append(f"  precision={prec:.4f} recall={rec:.4f}")

    # No positive predictions contract
    y_pred_none = [0, 0, 0, 0]
    tp0, fn0, fp0, tn0 = confusion(y_true_head, y_pred_none)
    prec0 = precision(y_true_head, y_pred_none)
    rec0 = recall(y_true_head, y_pred_none)
    lines.append("no positive predictions: y_true=[1, 1, 0, 0], y_pred=[0, 0, 0, 0]")
    lines.append(f"  TP={tp0} FN={fn0} FP={fp0} TN={tn0}")
    lines.append(f"  precision={prec0:.4f} recall={rec0:.4f}")
    return "\n".join(lines)


if __name__ == "__main__":
    print(run_contract())
