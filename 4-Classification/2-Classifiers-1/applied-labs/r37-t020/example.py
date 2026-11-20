"""Tiny, local binary-classification metrics fixture for the cuisine lesson."""

from __future__ import annotations

import argparse
from dataclasses import dataclass


@dataclass(frozen=True)
class BinaryMetrics:
    tp: int
    fn: int
    fp: int
    tn: int
    precision: float
    recall: float


def binary_metrics(*, y_true: list[int], y_pred: list[int]) -> BinaryMetrics:
    """Compute positive-class metrics; zero denominator yields 0.0."""
    if len(y_true) != len(y_pred):
        raise ValueError("y_true and y_pred must have the same length")
    if any(label not in (0, 1) for label in (*y_true, *y_pred)):
        raise ValueError("labels must be binary integers 0 or 1")

    tp = sum(actual == 1 and predicted == 1 for actual, predicted in zip(y_true, y_pred))
    fn = sum(actual == 1 and predicted == 0 for actual, predicted in zip(y_true, y_pred))
    fp = sum(actual == 0 and predicted == 1 for actual, predicted in zip(y_true, y_pred))
    tn = sum(actual == 0 and predicted == 0 for actual, predicted in zip(y_true, y_pred))
    predicted_positive = tp + fp
    actual_positive = tp + fn
    precision = tp / predicted_positive if predicted_positive else 0.0
    recall = tp / actual_positive if actual_positive else 0.0
    return BinaryMetrics(tp, fn, fp, tn, precision, recall)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--scenario", choices=("normal", "boundary", "failure"), default="normal")
    scenario = parser.parse_args().scenario
    if scenario == "normal":
        y_true, y_pred = [1, 1, 0, 0], [1, 0, 1, 0]
    elif scenario == "boundary":
        y_true, y_pred = [1, 0], [0, 0]
    else:
        y_true, y_pred = [1, 0], [1]

    metrics = binary_metrics(y_true=y_true, y_pred=y_pred)
    print(f"y_true={y_true}, y_pred={y_pred}")
    print(f"TP={metrics.tp}, FN={metrics.fn}, FP={metrics.fp}, TN={metrics.tn}")
    print(f"precision={metrics.precision:.1f}, recall={metrics.recall:.1f}")


if __name__ == "__main__":
    main()
