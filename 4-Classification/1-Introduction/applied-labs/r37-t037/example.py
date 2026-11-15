"""Binary confusion matrix, precision and recall with a worked trace (standard library only).

Label convention: 1 = positive class, 0 = negative class.
Argument order is ALWAYS (y_true, y_pred); swapping them swaps FP and FN.

Zero-denominator policy (documented decision):
    precision = TP / (TP + FP); if TP + FP == 0 (no positive predictions)
    precision is defined as 0.0.
    recall    = TP / (TP + FN); if TP + FN == 0 (no actual positives)
    recall is defined as 0.0.
Returning 0.0 keeps the result a plain float. Other libraries may choose
differently, so state the policy whenever you report these numbers.

Simulation: hand-written labels, NOT predictions from a trained model. It
says nothing about how any real classifier performs.
"""


def validate(y_true, y_pred):
    if len(y_true) != len(y_pred):
        raise ValueError(f"length mismatch: y_true={len(y_true)}, y_pred={len(y_pred)}")
    if len(y_true) == 0:
        raise ValueError("inputs must not be empty")
    for name, labels in (("y_true", y_true), ("y_pred", y_pred)):
        for v in labels:
            if isinstance(v, bool) or v not in (0, 1):
                raise ValueError(f"{name} contains invalid label {v!r}; use 0 or 1")


def outcome(t, p):
    if t == 1 and p == 1:
        return "TP"
    if t == 1 and p == 0:
        return "FN"
    if t == 0 and p == 1:
        return "FP"
    return "TN"


def worked_rows(y_true, y_pred):
    """One row per sample: (index, true, predicted, outcome)."""
    validate(y_true, y_pred)
    return [(i, t, p, outcome(t, p)) for i, (t, p) in enumerate(zip(y_true, y_pred), start=1)]


def confusion_matrix(y_true, y_pred):
    """Return (tp, fn, fp, tn)."""
    counts = {"TP": 0, "FN": 0, "FP": 0, "TN": 0}
    for _, _, _, o in worked_rows(y_true, y_pred):
        counts[o] += 1
    return counts["TP"], counts["FN"], counts["FP"], counts["TN"]


def precision_recall(y_true, y_pred):
    tp, fn, fp, _ = confusion_matrix(y_true, y_pred)
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    return precision, recall


def worked_report(y_true, y_pred):
    """Return the worked input-to-output explanation as text."""
    rows = worked_rows(y_true, y_pred)
    tp, fn, fp, tn = confusion_matrix(y_true, y_pred)
    p, r = precision_recall(y_true, y_pred)
    lines = [f"y_true={list(y_true)} y_pred={list(y_pred)}", "sample true pred outcome"]
    for i, t, pr, o in rows:
        lines.append(f"{i} {t} {pr} {o}")
    lines.append(f"TP={tp} FN={fn} FP={fp} TN={tn}")
    lines.append(f"precision=TP/(TP+FP)={tp}/{tp + fp}={p}")
    lines.append(f"recall=TP/(TP+FN)={tp}/{tp + fn}={r}")
    return "\n".join(lines)


if __name__ == "__main__":
    print(worked_report([1, 1, 0, 0], [1, 0, 1, 0]))
