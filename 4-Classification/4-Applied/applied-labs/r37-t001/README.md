# R37-T001: Classification Evaluation - Runnable Concept Example

**Label:** minimal complete local example, not a trained classifier.

## Prerequisites

Python 3 standard library and a local checkout. The local fixture is mandatory; any optional real-service extension needs separately supplied credentials/hardware and is not part of this task.

## What It Is

A minimal, deterministic, runnable concept example evaluating binary classification predictions against ground-truth labels. It computes:
- Confusion matrix counts: True Positives (TP), False Negatives (FN), False Positives (FP), and True Negatives (TN).
- Precision: `TP / (TP + FP)`.
- Recall: `TP / (TP + FN)`.
- Zero-denominator policy: when denominators are zero (`TP + FP == 0` or `TP + FN == 0`), metrics evaluate to `0.0` under the documented policy.

## Invocation

From the repository root:

```bash
python3 4-Classification/4-Applied/applied-labs/r37-t001/example.py
```

Run unit tests from the repository root:

```bash
python3 -m unittest discover -s 4-Classification/4-Applied/applied-labs/r37-t001 -p "test_*.py"
```

## Fixture and Expected Output

Fixture inputs:
- Headline: `y_true = [1, 1, 0, 0]`, `y_pred = [1, 0, 1, 0]`
- Zero positive predictions: `y_true = [1, 1, 0, 0]`, `y_pred = [0, 0, 0, 0]`

Expected CLI output:

```text
headline: y_true=[1, 1, 0, 0], y_pred=[1, 0, 1, 0]
  TP=1 FN=1 FP=1 TN=1
  precision=0.5000 recall=0.5000
no positive predictions: y_true=[1, 1, 0, 0], y_pred=[0, 0, 0, 0]
  TP=0 FN=2 FP=0 TN=2
  precision=0.0000 recall=0.0000
```

## Lesson Concept Connection

| Name | Concept in Lesson | Purpose |
|------|-------------------|---------|
| `y_true` | Ground Truth | Known class outcomes for evaluation |
| `y_pred` | Classifier Predictions | Labels assigned by classifier model |
| `TP` | True Positive | Positive item correctly identified |
| `FN` | False Negative | Positive item missed by classifier |
| `FP` | False Positive | Negative item mistakenly flagged |
| `TN` | True Negative | Negative item correctly rejected |
| `precision` | Precision Metric | Exactness of positive predictions |
| `recall` | Recall Metric | Completeness of positive capture |

## Limitations

- Uses fixed toy binary labels (0/1); no multiclass classification.
- No model training, dataset ingestion, or feature transformation.
- Makes no claims about real hardware, cloud services, or trained-model accuracy.
