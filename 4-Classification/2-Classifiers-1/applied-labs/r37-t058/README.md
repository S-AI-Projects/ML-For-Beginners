# Applied Lab R37-T058: Classification Evaluation — Failure and Recovery Example

## Overview

This lab extends [Cuisine classifiers 1](../../README.md) by demonstrating structured failure handling, actionable diagnostic error envelopes, and seamless state recovery during binary classification evaluation.

In production machine learning pipelines, evaluation datasets frequently contain data anomalies (e.g., mismatched array lengths from missing rows, non-binary label encoding, or empty input batches). Rather than crashing silently or corrupting session state, evaluators must emit actionable diagnostics and recover immediately on subsequent valid inputs.

## Handled Failure Modes & Recovery Protocol

| Failure Mode | Invalid Input | Error Envelope | Recovery Action |
| :--- | :--- | :--- | :--- |
| **Length Mismatch** | `y_true=[1,1,0,0], y_pred=[1,0]` | `LengthMismatchError` | Aligns observation dimensions |
| **Non-Binary Label** | `y_true=[1, 2], y_pred=[1, 0]` | `InvalidLabelError` | Enforces 0/1 integer binarization |
| **Non-List Type** | `y_true=None, y_pred=[1, 0]` | `TypeError` | Validates container data types |
| **Empty Input** | `y_true=[], y_pred=[]` | `EmptyInputError` | Requires non-empty test batches |

## Baseline Fixture & Zero-Denominator Policy

- **Input**: `y_true=[1, 1, 0, 0]`, `y_pred=[1, 0, 1, 0]`
- **Confusion Matrix**: `TP=1, FN=1, FP=1, TN=1`
- **Scores**: Precision = `0.5`, Recall = `0.5`, Accuracy = `0.5`
- **Zero-Denominator Policy**: When no positive predictions exist (`y_pred=[0,0,0,0]`), precision explicitly defaults to `0.0`.

## Running Tests

```bash
python3 -m unittest discover -s 4-Classification/2-Classifiers-1/applied-labs/r37-t058 -p "test_*.py" -v
```
