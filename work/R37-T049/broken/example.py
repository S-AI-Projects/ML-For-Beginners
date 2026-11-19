"""Classification evaluation on a fixed toy example.

Data: fixed toy labels, not a trained classifier. No model is trained
here; every input is a hard-coded list of 0/1 labels.

Prerequisites: Python 3 standard library and a local checkout. The local
fixture is mandatory; any optional real-service extension needs
separately supplied credentials/hardware and is not part of this task.

Zero-denominator policy (named, documented, tested):
precision is 0.0 when there are no positive predictions (TP + FP == 0);
recall is 0.0 when there are no actual positives (TP + FN == 0).
"""

ZERO_DENOMINATOR_VALUE = 0.0

Y_TRUE = [1, 1, 0, 0]
Y_PRED = [1, 0, 1, 0]
Q1_TRUE = [1, 1, 1, 0]
Q1_PRED = [1, 0, 0, 1]


def _check_labels(y_true, y_pred):
    if len(y_true) != len(y_pred):
        raise ValueError("y_true and y_pred must have equal length")
    for label in list(y_true) + list(y_pred):
        if type(label) is not int or label not in (0, 1):
            raise ValueError("labels must be 0 or 1, got %r" % (label,))


def confusion(y_true, y_pred):
    """Return (TP, FN, FP, TN) for binary 0/1 labels."""
    _check_labels(y_true, y_pred)
    tp = fn = fp = tn = 0
    for t, p in zip(y_true, y_pred):
        if t == 1 and p == 1:
            tp += 1
        elif t == 1:
            fn += 1
        elif p == 1:
            fp += 1
        else:
            tn += 1
    return tp, fn, fp, tn


def precision(y_true, y_pred):
    """TP / (TP + FP); 0.0 when there are no positive predictions."""
    tp, fn, fp, tn = confusion(y_true, y_pred)
    if tp + fp == 0:
        return ZERO_DENOMINATOR_VALUE
    return tp / (tp + fp)


def recall(y_true, y_pred):
    """TP / (TP + FN); 0.0 when there are no actual positives."""
    tp, fn, fp, tn = confusion(y_true, y_pred)
    if tp + fn == 0:
        return ZERO_DENOMINATOR_VALUE
    return tp / (tp + fn)


def questions():
    """Return the three applied questions as (id, question, answer)."""
    tp, fn, fp, tn = confusion(Q1_TRUE, Q1_PRED)
    q1 = "TP=%d FN=%d FP=%d TN=%d precision=%.4f recall=%.4f" % (
        tp, fn, fp, tn, precision(Q1_TRUE, Q1_PRED),
        recall(Q1_TRUE, Q1_PRED))
    q2 = "precision(y_pred, y_true)=%.4f equals recall=%.4f" % (
        precision(Q1_PRED, Q1_TRUE), recall(Q1_TRUE, Q1_PRED))
    q3 = "precision with no positive predictions=%.4f" % (
        precision([1, 1, 0, 0], [0, 0, 0, 0]))
    return [
        ("Q1", "Predict an output for Q1 data", q1),
        ("Q2", "Diagnose a swapped-argument failure", q2),
        ("Q3", "Choose a boundary policy for no positives", q3),
    ]


def main():
    tp, fn, fp, tn = confusion(Y_TRUE, Y_PRED)
    print("headline TP=%d FN=%d FP=%d TN=%d" % (tp, fn, fp, tn))
    print("precision=%.4f recall=%.4f" % (
        precision(Y_TRUE, Y_PRED), recall(Y_TRUE, Y_PRED)))
    for qid, question, answer in questions():
        print("%s %s: %s" % (qid, question, answer))


if __name__ == "__main__":
    main()
