"""Classification evaluation — refactor the teaching example for 4-Classification/4-Applied."""

from typing import Any, Dict, List, Tuple

MOCK_LIMITATIONS = [
    "Binary classification evaluation only (labels 0 and 1); does not compute multi-class or multi-label metrics.",
    "Does not calculate threshold-varying curves (ROC-AUC, Precision-Recall AUC).",
    "Uses discrete pre-computed binary arrays; does not evaluate continuous model probability logits.",
    "Zero-denominator policy returns 0.0 rather than raising ZeroDivisionError or returning NaN.",
]


class BinaryMetricsCalculator:
    """Refactored calculation engine separating pure metric calculation from presentation."""

    def __init__(self, zero_division: float = 0.0):
        self.zero_division = zero_division

    def validate_inputs(self, y_true: List[int], y_pred: List[int]) -> None:
        """Validates input sequence lengths and binary values."""
        if len(y_true) != len(y_pred):
            raise ValueError(f"Length mismatch: len(y_true)={len(y_true)} != len(y_pred)={len(y_pred)}.")
        for val in y_true + y_pred:
            if val not in (0, 1):
                raise ValueError(f"Invalid label {val}. Binary labels must be 0 or 1.")

    def compute_confusion_matrix(self, y_true: List[int], y_pred: List[int]) -> Dict[str, int]:
        """Computes true positives, false negatives, false positives, and true negatives."""
        self.validate_inputs(y_true, y_pred)
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
        return {"tp": tp, "fn": fn, "fp": fp, "tn": tn}

    def compute_precision(self, tp: int, fp: int) -> float:
        """Computes precision: TP / (TP + FP) with explicit zero-denominator policy."""
        denominator = tp + fp
        if denominator == 0:
            return self.zero_division
        return tp / denominator

    def compute_recall(self, tp: int, fn: int) -> float:
        """Computes recall: TP / (TP + FN) with explicit zero-denominator policy."""
        denominator = tp + fn
        if denominator == 0:
            return self.zero_division
        return tp / denominator

    def evaluate(self, y_true: List[int], y_pred: List[int]) -> Dict[str, Any]:
        """Computes complete metrics report."""
        cm = self.compute_confusion_matrix(y_true, y_pred)
        prec = self.compute_precision(cm["tp"], cm["fp"])
        rec = self.compute_recall(cm["tp"], cm["fn"])
        acc = (cm["tp"] + cm["tn"]) / len(y_true) if len(y_true) > 0 else self.zero_division

        return {
            "confusion_matrix": cm,
            "precision": prec,
            "recall": rec,
            "accuracy": acc,
            "zero_division_policy": f"zero_division={self.zero_division}",
        }


class MetricsPresenter:
    """Refactored presentation layer for formatting and rendering metrics."""

    @staticmethod
    def format_summary(evaluation: Dict[str, Any]) -> str:
        cm = evaluation["confusion_matrix"]
        return (
            f"TP={cm['tp']}, FN={cm['fn']}, FP={cm['fp']}, TN={cm['tn']} | "
            f"Precision={evaluation['precision']:.3f}, Recall={evaluation['recall']:.3f}, Accuracy={evaluation['accuracy']:.3f}"
        )


def evaluate_binary_classification(y_true: List[int], y_pred: List[int], zero_division: float = 0.0) -> Dict[str, Any]:
    """Convenience facade function executing the refactored evaluator."""
    calc = BinaryMetricsCalculator(zero_division=zero_division)
    return calc.evaluate(y_true, y_pred)


if __name__ == "__main__":
    import json
    y_true = [1, 1, 0, 0]
    y_pred = [1, 0, 1, 0]
    res = evaluate_binary_classification(y_true, y_pred)
    print("Normal Case Evaluation:")
    print(json.dumps(res, indent=2))
    print("Formatted Summary:", MetricsPresenter.format_summary(res))
