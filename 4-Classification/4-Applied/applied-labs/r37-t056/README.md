# Applied Lab R37-T056: Classification Evaluation — Refactor Teaching Example

## Overview

This lab extends [Build a Cuisine Recommender Web App](../../README.md) by refactoring binary classification evaluation metrics into clean, modular components.

Evaluating recommender classifications requires rigorous tracking of confusion matrices, precision, and recall. This lab separates calculation logic from presentation formatting and provides an explicit zero-denominator policy.

## Architecture & Refactored Modules

- `BinaryMetricsCalculator`: Pure mathematical calculation engine for Confusion Matrix, Precision, Recall, and Accuracy.
- `MetricsPresenter`: Presentation layer generating formatted text summaries.
- `evaluate_binary_classification`: Facade function coordinating calculation and reporting.

## Core Fixture Results

- **Input**: `y_true=[1, 1, 0, 0]`, `y_pred=[1, 0, 1, 0]`
- **Confusion Matrix**:
  - True Positives (TP): `1`
  - False Negatives (FN): `1`
  - False Positives (FP): `1`
  - True Negatives (TN): `1`
- **Metrics**: Precision = `0.5`, Recall = `0.5`, Accuracy = `0.5`
- **Zero-Denominator Boundary Policy**: When `y_pred=[0, 0, 0, 0]`, $TP+FP=0$; precision explicitly defaults to `0.0`.

## Running Tests

```bash
python3 -m unittest discover -s 4-Classification/4-Applied/applied-labs/r37-t056 -p "test_*.py" -v
```
