# R37-T031: Classification evaluation (confusion matrix, precision, recall)

A small local example for the lesson [Introduction to classification](../../README.md).

## What it shows

It compares a binary classifier's predictions (`y_pred`) with the true labels (`y_true`) and computes TP, FN, FP, TN, precision and recall. This links to the lesson's class balance idea: if one class dominates, "percent correct" can look good while the model never finds the rare class. Precision and recall expose that.

Argument order matters: `evaluate(y_true, y_pred)`. Swapping them swaps FN and FP.

## Zero-denominator policy

- Precision = TP / (TP + FP). If there are no positive predictions, precision is defined as 0.0.
- Recall = TP / (TP + FN). If there are no actual positives, recall is defined as 0.0.

## How to run

Requires Python 3 and the standard library only.

```bash
python3 4-Classification/1-Introduction/applied-labs/r37-t031/example.py
```

Fixture: `y_true=[1,1,0,0]`, `y_pred=[1,0,1,0]`. Expected output:

```
TP=1 FN=1 FP=1 TN=1 precision=0.5 recall=0.5
```

## Tests

```bash
python3 -m unittest discover -s 4-Classification/1-Introduction/applied-labs/r37-t031 -p "test_*.py"
```

The tests cover a normal case, boundary cases (no positive predictions, no actual positives) and failure cases (length mismatch, empty input, invalid labels).

## Limits

This uses fixed, hand-written labels. It does not train a model, use real data, or say anything about how well any real model performs. Nothing here is simulated hardware or a cloud service.