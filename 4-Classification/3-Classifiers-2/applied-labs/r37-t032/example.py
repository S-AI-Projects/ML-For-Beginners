"""Binary confusion matrix, precision and recall (standard library only).

Label convention: 1 = positive class, 0 = negative class.
Argument order is ALWAYS (y_true, y_pred) -- swapping them swaps FP and FN.

Zero-denominator policy (documented decision):
    precision = TP / (TP + FP). If TP + FP == 0 (no positive predictions),
    precision is defined as 0.0.
    recall    = TP / (TP + FN). If TP + FN == 0 (no actual positives),
    recall is defined as 0.0.
Returning 0.0 (rather than raising or returning NaN) keeps the result a plain
float; it means "no evidence of positive-class performance". Other libraries
may choose differently (scikit-learn warns and uses 0.0 by default).

Simulation note: this uses hand-written labels, NOT a trained model, so it
makes no claim about how any real classifier performs.
"""


def validate(y_true, y_pred):
    if len(y_true) != len(y_pred):
        raise ValueError(
            f"length mismatch: y_true={len(y_true)}, y_pred={len(y_pred)}"
        )
    if len(y_true) == 0:
        raise ValueError("inputs must not be empty")
    for name, labels in (("y_true", y_true), ("y_pred", y_pred)):
        for v in labels:
            # bool is a subclass of int, so reject it explicitly
            if isinstance(v, bool) or v not in (0, 1):
                raise ValueError(f"{name} contains invalid label {v!r}; use 0 or 1")


def confusion_matrix(y_true, y_pred):
    """Return (tp, fn, fp, tn)."""
    validate(y_true, y_pred)
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


def precision_recall(y_true, y_pred):
    tp, fn, fp, _ = confusion_matrix(y_true, y_pred)
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    return precision, recall


if __name__ == "__main__":
    y_true = [1, 1, 0, 0]
    y_pred = [1, 0, 1, 0]
    tp, fn, fp, tn = confusion_matrix(y_true, y_pred)
    p, r = precision_recall(y_true, y_pred)
    print(f"y_true={y_true} y_pred={y_pred}")
    print(f"TP={tp} FN={fn} FP={fp} TN={tn}")
    print(f"precision={p} recall={r}")
