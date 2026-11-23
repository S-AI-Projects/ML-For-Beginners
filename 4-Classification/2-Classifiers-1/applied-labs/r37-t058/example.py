"""Classification evaluation — failure and recovery example for 4-Classification/2-Classifiers-1."""

from typing import Any, Dict, List, Optional

MOCK_LIMITATIONS = [
    "Binary classification evaluation only (labels 0 and 1); does not calculate multi-class confusion matrices.",
    "Does not compute threshold curves (ROC-AUC, Precision-Recall AUC).",
    "Uses discrete pre-computed binary arrays; does not evaluate continuous model probability logits.",
    "Zero-denominator policy returns 0.0 rather than raising ZeroDivisionError.",
]


class BinaryEvaluationSession:
    """Evaluation session with structured error handling, error explanation, and clean recovery."""

    def __init__(self, zero_division: float = 0.0):
        self.zero_division = zero_division
        self.last_error: Optional[Dict[str, Any]] = None
        self.history: List[Dict[str, Any]] = []

    def evaluate(self, y_true: Any, y_pred: Any) -> Dict[str, Any]:
        """Evaluates binary predictions with validation, failure capture, and recovery."""
        # 1. Validation checks
        if not isinstance(y_true, list) or not isinstance(y_pred, list):
            err = {
                "error_type": "TypeError",
                "message": f"Inputs must be lists of binary integers, got y_true={type(y_true).__name__}, y_pred={type(y_pred).__name__}.",
                "recovery_guidance": "Provide Python lists containing only integers 0 and 1.",
            }
            self.last_error = err
            return {"status": "error", "error": err, "metrics": None}

        if len(y_true) != len(y_pred):
            err = {
                "error_type": "LengthMismatchError",
                "message": f"Input length mismatch: len(y_true)={len(y_true)} != len(y_pred)={len(y_pred)}.",
                "recovery_guidance": "Ensure y_true and y_pred contain the exact same number of observations.",
            }
            self.last_error = err
            return {"status": "error", "error": err, "metrics": None}

        if len(y_true) == 0:
            err = {
                "error_type": "EmptyInputError",
                "message": "Input lists are empty. At least one observation is required.",
                "recovery_guidance": "Pass non-empty observation arrays.",
            }
            self.last_error = err
            return {"status": "error", "error": err, "metrics": None}

        for idx, val in enumerate(y_true + y_pred):
            if val not in (0, 1):
                err = {
                    "error_type": "InvalidLabelError",
                    "message": f"Invalid binary label '{val}'. All labels must be 0 or 1.",
                    "recovery_guidance": "Clean dataset labels to binary 0 or 1 integers.",
                }
                self.last_error = err
                return {"status": "error", "error": err, "metrics": None}

        # 2. Calculation phase
        tp = fn = fp = tn = 0
        for yt, yp in zip(y_true, y_pred):
            if yt == 1 and yp == 1:
                tp += 1
            elif yt == 1 and yp == 0:
                fn += 1
            elif yt == 0 and yp == 1:
                fp += 1
            elif yt == 0 and yp == 0:
                tn += 1

        precision = (tp / (tp + fp)) if (tp + fp) > 0 else self.zero_division
        recall = (tp / (tp + fn)) if (tp + fn) > 0 else self.zero_division
        accuracy = (tp + tn) / len(y_true)

        # Clear error on successful execution (Recovery achieved)
        self.last_error = None
        metrics = {
            "confusion_matrix": {"tp": tp, "fn": fn, "fp": fp, "tn": tn},
            "precision": precision,
            "recall": recall,
            "accuracy": accuracy,
        }
        record = {"status": "success", "error": None, "metrics": metrics}
        self.history.append(record)
        return record


def run_failure_and_recovery_demonstration() -> Dict[str, Any]:
    """Demonstrates initial normal execution, intentional failure, and seamless recovery."""
    session = BinaryEvaluationSession()

    # Step 1: Normal execution
    res1 = session.evaluate([1, 1, 0, 0], [1, 0, 1, 0])

    # Step 2: Intentional failure (length mismatch)
    res2 = session.evaluate([1, 1, 0, 0], [1, 0])

    # Step 3: Recovery on next valid input (all zeros / no positive predictions)
    res3 = session.evaluate([1, 1, 0, 0], [0, 0, 0, 0])

    return {
        "step_1_normal": res1,
        "step_2_failure": res2,
        "step_3_recovery": res3,
        "recovered_successfully": (session.last_error is None),
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run_failure_and_recovery_demonstration(), indent=2))
