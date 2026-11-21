"""
r37-t021: Classification Evaluation – Boundary-Case Lesson Extension
=====================================================================
Lesson context: 4-Classification/4-Applied/README.md
  "Build a Cuisine Recommender Web App"

This example extends the lesson by computing a confusion matrix, precision,
and recall for a *binary* classifier using small, fixed local fixtures —
no model download, paid provider, GPU, or physical device is required.
All behaviour here is simulated/mock: the "predictions" are hard-coded
lists, not outputs of a trained model.

Where the lesson simplification stops
--------------------------------------
The lesson trains an SVC on 380-ingredient cuisine data and exports it
to ONNX for browser inference.  It reports a full multi-class
classification_report (precision, recall, f1 per cuisine).  This example
strips away the multi-class complexity and the ONNX runtime to focus on
*how* the binary metrics are computed and what happens at the edges:

  * Smallest valid case  – exactly the four cells of a 2×2 matrix
  * Boundary case        – no positive predictions → denominator is 0
  * Invalid / failure    – a deliberately wrong expected value that makes
                           the test suite exit non-zero

Confusion matrix layout (binary, positive class = 1)
------------------------------------------------------
                  Predicted 1   Predicted 0
  Actual 1  (P)      TP            FN
  Actual 0  (N)      FP            TN

Zero-denominator policy
------------------------
When there are no positive predictions (TP + FP == 0), precision is
defined as 0.0 and a warning is emitted.  This matches scikit-learn's
default behaviour with zero_division=0.
"""

import sys

# ---------------------------------------------------------------------------
# Core metric helpers
# ---------------------------------------------------------------------------

def confusion_matrix_binary(y_true, y_pred):
    """Return (TP, FN, FP, TN) for binary labels (positive class = 1)."""
    if len(y_true) != len(y_pred):
        raise ValueError(
            f"Length mismatch: y_true has {len(y_true)} items, "
            f"y_pred has {len(y_pred)} items."
        )
    TP = FN = FP = TN = 0
    for t, p in zip(y_true, y_pred):
        if t == 1 and p == 1:
            TP += 1
        elif t == 1 and p == 0:
            FN += 1
        elif t == 0 and p == 1:
            FP += 1
        else:
            TN += 1
    return TP, FN, FP, TN


def precision_binary(TP, FP):
    """
    Precision = TP / (TP + FP).

    Zero-denominator policy: returns 0.0 and prints a warning when
    TP + FP == 0 (no positive predictions at all).
    """
    denom = TP + FP
    if denom == 0:
        print(
            "WARNING: no positive predictions (TP + FP = 0). "
            "Precision set to 0.0 under the documented zero-denominator policy.",
            file=sys.stderr,
        )
        return 0.0
    return TP / denom


def recall_binary(TP, FN):
    """
    Recall = TP / (TP + FN).

    Zero-denominator policy: returns 0.0 and prints a warning when
    TP + FN == 0 (no actual positives in the ground truth).
    """
    denom = TP + FN
    if denom == 0:
        print(
            "WARNING: no actual positives (TP + FN = 0). "
            "Recall set to 0.0 under the documented zero-denominator policy.",
            file=sys.stderr,
        )
        return 0.0
    return TP / denom


# ---------------------------------------------------------------------------
# Demonstration fixtures
# ---------------------------------------------------------------------------

def run_normal_case():
    """
    Smallest valid fixture with a balanced confusion matrix.

    y_true = [1, 1, 0, 0]  (two positives, two negatives)
    y_pred = [1, 0, 1, 0]  (one correct positive, one miss, one false alarm, one correct negative)

    Expected:
        TP=1, FN=1, FP=1, TN=1
        precision = 1/(1+1) = 0.5
        recall    = 1/(1+1) = 0.5

    NOTE: This is a mock/simulation fixture — labels are hard-coded, not
    produced by a trained model or any external service.
    """
    y_true = [1, 1, 0, 0]
    y_pred = [1, 0, 1, 0]

    TP, FN, FP, TN = confusion_matrix_binary(y_true, y_pred)
    prec = precision_binary(TP, FP)
    rec  = recall_binary(TP, FN)

    print("=== Normal case ===")
    print(f"  y_true : {y_true}")
    print(f"  y_pred : {y_pred}")
    print(f"  TP={TP}  FN={FN}  FP={FP}  TN={TN}")
    print(f"  precision = {prec:.4f}")
    print(f"  recall    = {rec:.4f}")

    return dict(TP=TP, FN=FN, FP=FP, TN=TN, precision=prec, recall=rec)


def run_boundary_case_no_positive_predictions():
    """
    Boundary case: the classifier never predicts 1.

    y_true = [1, 0]   (one actual positive)
    y_pred = [0, 0]   (no predicted positives → TP=0, FP=0)

    Exact boundary decision
    -----------------------
    The denominator for precision is TP + FP = 0 + 0 = 0.
    Rather than raising ZeroDivisionError, we return 0.0 and emit a
    warning.  This is the boundary between "some positive predictions"
    (where precision is well-defined) and "no positive predictions"
    (where the formula is undefined and we apply the documented default).

    NOTE: Simulation/mock fixture — no model is involved.
    """
    y_true = [1, 0]
    y_pred = [0, 0]

    TP, FN, FP, TN = confusion_matrix_binary(y_true, y_pred)
    prec = precision_binary(TP, FP)   # triggers zero-denominator warning
    rec  = recall_binary(TP, FN)

    print("\n=== Boundary case: no positive predictions ===")
    print(f"  y_true : {y_true}")
    print(f"  y_pred : {y_pred}")
    print(f"  TP={TP}  FN={FN}  FP={FP}  TN={TN}")
    print(f"  precision = {prec:.4f}  (zero-denominator policy applied)")
    print(f"  recall    = {rec:.4f}")

    return dict(TP=TP, FN=FN, FP=FP, TN=TN, precision=prec, recall=rec)


def run_invalid_case_length_mismatch():
    """
    Invalid case: y_true and y_pred have different lengths.

    Demonstrates that the helper raises ValueError instead of silently
    producing wrong numbers.
    """
    print("\n=== Invalid case: length mismatch ===")
    try:
        confusion_matrix_binary([1, 0], [1])
        print("  ERROR: expected ValueError but none was raised!")
    except ValueError as exc:
        print(f"  Caught expected ValueError: {exc}")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    run_normal_case()
    run_boundary_case_no_positive_predictions()
    run_invalid_case_length_mismatch()
