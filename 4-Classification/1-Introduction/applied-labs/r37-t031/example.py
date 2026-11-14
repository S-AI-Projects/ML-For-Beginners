"""R37-T031: confusion matrix, precision and recall for a binary classifier.

Standard library only. Labels are 1 (positive) and 0 (negative).
Order matters: arguments are (y_true, y_pred), in that order.

Zero-denominator policy: if precision or recall has a denominator of 0,
the metric is defined as 0.0 (no positive predictions -> precision 0.0;
no actual positives -> recall 0.0).

Simplification: this uses fixed labels only. It says nothing about how a
trained model would perform on real data.
"""

ZERO_DENOMINATOR_VALUE = 0.0


def _validate(y_true, y_pred):
    if len(y_true) != len(y_pred):
        raise ValueError("y_true and y_pred must have the same length")
    if len(y_true) == 0:
        raise ValueError("labels must not be empty")
    for label in list(y_true) + list(y_pred):
        if label not in (0, 1):
            raise ValueError(f"labels must be 0 or 1, got {label!r}")


def confusion_matrix(y_true, y_pred):
    """Return counts as {"TP", "FN", "FP", "TN"}."""
    _validate(y_true, y_pred)
    counts = {"TP": 0, "FN": 0, "FP": 0, "TN": 0}
    for t, p in zip(y_true, y_pred):
        if t == 1 and p == 1:
            counts["TP"] += 1
        elif t == 1 and p == 0:
            counts["FN"] += 1
        elif t == 0 and p == 1:
            counts["FP"] += 1
        else:
            counts["TN"] += 1
    return counts


def precision(tp, fp):
    denominator = tp + fp
    return tp / denominator if denominator else ZERO_DENOMINATOR_VALUE


def recall(tp, fn):
    denominator = tp + fn
    return tp / denominator if denominator else ZERO_DENOMINATOR_VALUE


def evaluate(y_true, y_pred):
    counts = confusion_matrix(y_true, y_pred)
    return {
        **counts,
        "precision": precision(counts["TP"], counts["FP"]),
        "recall": recall(counts["TP"], counts["FN"]),
    }


if __name__ == "__main__":
    result = evaluate([1, 1, 0, 0], [1, 0, 1, 0])
    print(
        f"TP={result['TP']} FN={result['FN']} FP={result['FP']} TN={result['TN']} "
        f"precision={result['precision']} recall={result['recall']}"
    )