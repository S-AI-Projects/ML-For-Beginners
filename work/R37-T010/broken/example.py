"""Classification evaluation on logistic regression predictions with applied questions.

Label: fixed toy labels, not a trained logistic regression model.

Prerequisites: Python 3 standard library and a local checkout. The local
fixture is mandatory; any optional real-service extension needs
separately supplied credentials/hardware and is not part of this task.

Contract:
- y_true=[1, 1, 0, 0], y_pred=[1, 0, 1, 0] gives TP=1, FN=1, FP=1, TN=1, precision=0.5, recall=0.5.
- No positive predictions (TP + FP == 0) gives precision=0.0 under the documented zero-denominator policy.
- Three applied questions with rationales and executable checks:
  1. Predict an output (Q1 data: [1, 1, 1, 0] vs [1, 0, 0, 1]).
  2. Diagnose a failure (argument order swapped in precision calculation).
  3. Choose a boundary policy (zero denominator handling).
"""

ZERO_DENOMINATOR_VALUE = 0.0

Y_TRUE = [1, 1, 0, 0]
Y_PRED = [1, 0, 1, 0]

Q1_TRUE = [1, 1, 1, 0]
Q1_PRED = [1, 0, 0, 1]


def validate_labels(y_true, y_pred):
    """Validate that inputs are non-empty, equal-length lists of binary 0/1 integers."""
    if not isinstance(y_true, (list, tuple)) or not isinstance(y_pred, (list, tuple)):
        raise TypeError("y_true and y_pred must be lists or tuples")
    if len(y_true) == 0:
        raise ValueError("labels cannot be empty")
    if len(y_true) != len(y_pred):
        raise ValueError("y_true and y_pred must have equal length")
    for val in list(y_true) + list(y_pred):
        if type(val) is not int or val not in (0, 1):
            raise ValueError(f"labels must be binary 0 or 1 integers, got {val!r}")


def confusion(y_true, y_pred):
    """Compute confusion matrix counts (TP, FN, FP, TN)."""
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


def questions():
    """Return the three applied questions with computed answers and rationales."""
    # Q1: Predict output for [1, 1, 1, 0] vs [1, 0, 0, 1]
    tp1, fn1, fp1, tn1 = confusion(Q1_TRUE, Q1_PRED)
    prec1 = precision(Q1_TRUE, Q1_PRED)
    rec1 = recall(Q1_TRUE, Q1_PRED)
    q1_answer = f"TP={tp1} FN={fn1} FP={fp1} TN={tn1} precision={prec1:.4f} recall={rec1:.4f}"
    q1_rationale = (
        "Item 0 is 1->1 (TP). Items 1 and 2 are 1->0 (FN=2). Item 3 is 0->1 (FP=1). "
        "No item is 0->0 (TN=0). Precision = 1/(1+1) = 0.5000. Recall = 1/(1+2) = 0.3333."
    )

    # Q2: Diagnose a failure (swapped argument order)
    swapped_prec = precision(Q1_PRED, Q1_TRUE)
    q2_answer = f"precision(y_pred, y_true)={swapped_prec:.4f} equals recall={rec1:.4f}"
    q2_rationale = (
        "Passing arguments in swapped order (y_pred, y_true) swaps FP and FN in the matrix. "
        "As a result, precision evaluates as TP/(TP+FN), which computes recall (0.3333) instead of precision (0.5000)."
    )

    # Q3: Choose a boundary policy
    y_pred_zero = [0, 0, 0, 0]
    p_zero = precision(Y_TRUE, y_pred_zero)
    q3_answer = f"precision with no positive predictions={p_zero:.4f}"
    q3_rationale = (
        "When no positive predictions exist (TP+FP=0), returning 0.0 avoids crashing downstream pipelines "
        "(unlike raising an exception), avoids propagating undefined IEEE floating NaN values, "
        "and avoids falsely reporting perfect precision (1.0). 0.0 conservatively reflects zero positive predictive utility."
    )

    return [
        {"id": "Q1", "topic": "predict an output", "answer": q1_answer, "rationale": q1_rationale},
        {"id": "Q2", "topic": "diagnose a failure", "answer": q2_answer, "rationale": q2_rationale},
        {"id": "Q3", "topic": "choose a boundary policy", "answer": q3_answer, "rationale": q3_rationale}
    ]


def run_contract():
    """Run headline contract cases and display applied questions."""
    lines = []
    lines.append("fixed toy labels, not a trained logistic regression model")

    tp, fn, fp, tn = confusion(Y_TRUE, Y_PRED)
    prec = precision(Y_TRUE, Y_PRED)
    rec = recall(Y_TRUE, Y_PRED)
    lines.append(f"headline TP={tp} FN={fn} FP={fp} TN={tn}")
    lines.append(f"precision={prec:.4f} recall={rec:.4f}")

    for q in questions():
        lines.append(f"{q['id']} {q['topic'].capitalize()}: {q['answer']}")
    return "\n".join(lines)


if __name__ == "__main__":
    print(run_contract())
