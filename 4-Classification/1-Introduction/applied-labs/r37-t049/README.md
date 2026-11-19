# Classification evaluation: scenario assessment (R37-T049)

A small lab that computes confusion counts, precision and recall for two
fixed 0/1 label lists, then answers three applied questions about them.

**Label:** fixed toy labels, not a trained classifier.

## Prerequisites

Python 3 standard library and a local checkout. The local fixture is mandatory; any optional real-service extension needs separately supplied credentials/hardware and is not part of this task.

## Run it

From the repository root:

```bash
python3 4-Classification/1-Introduction/applied-labs/r37-t049/example.py
```

Run the tests (the required check):

```bash
python3 -m unittest discover -s 4-Classification/1-Introduction/applied-labs/r37-t049 -p "test_*.py"
```

## Fixture

Two hard-coded label lists live in `example.py`:

- Headline: `y_true = [1, 1, 0, 0]`, `y_pred = [1, 0, 1, 0]`
- Q1 and Q2: `y_true = [1, 1, 1, 0]`, `y_pred = [1, 0, 0, 1]`

No file is read, no model is trained and nothing is downloaded.

## Expected output

This is the CLI's real stdout (`work/R37-T049/example_output.txt`):

```text
headline TP=1 FN=1 FP=1 TN=1
precision=0.5000 recall=0.5000
Q1 Predict an output for Q1 data: TP=1 FN=2 FP=1 TN=0 precision=0.5000 recall=0.3333
Q2 Diagnose a swapped-argument failure: precision(y_pred, y_true)=0.3333 equals recall=0.3333
Q3 Choose a boundary policy for no positives: precision with no positive predictions=0.0000
```

## Definitions

Each label is 0 (negative) or 1 (positive). `confusion(y_true, y_pred)`
returns `(TP, FN, FP, TN)`, counting pairs where the true label is 1 and
the prediction is 1 (TP), true 1 and predicted 0 (FN), true 0 and
predicted 1 (FP), and true 0 and predicted 0 (TN).

- `precision = TP / (TP + FP)`
- `recall = TP / (TP + FN)`

Argument order is always `(y_true, y_pred)`. The lists must have equal
length and contain only the integers 0 and 1; otherwise a `ValueError`
is raised.

**Zero-denominator policy:** precision is `0.0` when there are no
positive predictions (`TP + FP == 0`), and recall is `0.0` when there
are no actual positives (`TP + FN == 0`).

## Applied questions

### Q1: Predict an output

- **Question:** For `y_true = [1, 1, 1, 0]` and `y_pred = [1, 0, 0, 1]`,
  what are TP, FN, FP, TN, precision and recall?
- **Answer:** TP=1, FN=2, FP=1, TN=0; precision 0.5; recall 1/3 (0.3333).
- **Rationale:** Walk the four pairs. Only the first pair is a true
  positive. Two actual positives are missed, so recall is 1 out of 3
  actual positives found. One negative is predicted positive, so
  precision is 1 out of 2 positive predictions correct.
- **Check:** `test_q1_predict_output`

### Q2: Diagnose a failure

- **Question:** A caller passes the arguments in the wrong order,
  `precision(y_pred, y_true)`, on the Q1 data and gets 1/3 instead of 0.5.
  Why?
- **Answer:** Swapping the arguments swaps FP and FN, so precision and
  recall trade places. `precision(y_pred, y_true)` equals
  `recall(y_true, y_pred)` (both 1/3).
- **Rationale:** With the arguments swapped, the old false positives
  become false negatives and the reverse. Precision divides by
  predicted positives, recall by actual positives, so the two metrics
  change places.
- **Check:** `test_q2_swapped_arguments` asserts
  `precision(y_pred, y_true) == recall(y_true, y_pred) == 1/3` and that
  this differs from `precision(y_true, y_pred) == 0.5`.

### Q3: Choose a boundary policy

- **Question:** What should precision be when the model predicts no
  positives?
- **Answer:** `0.0`, documented as the policy.
- **Rationale:** It keeps the metric defined and numeric for reporting,
  and a reader sees that no positive was found. The alternatives were
  considered and rejected:
  - *Raise an error:* stops a whole report for one empty class and
    makes a valid case look like a crash.
  - *Return NaN:* keeps the value honest but breaks ordering and
    comparisons, and NaN propagates silently through averages.
  - *Return 1.0:* would say a perfect score when nothing was predicted.
- **Check:** `test_q3_no_positive_predictions` asserts that
  `precision([1, 1, 0, 0], [0, 0, 0, 0])` returns `0.0` without raising.

## How this relates to the lesson

The lesson's introduction says classification is supervised: the data is
labeled and the algorithm uses those labels. This lab works with labels
only; it shows how predicted and true labels are compared, which the
lesson does not cover. The order of `(y_true, y_pred)` matters, and each
metric's denominator decides what it measures (predicted positives for
precision, actual positives for recall). The lesson's "Balance the
dataset" section is about class counts; the headline example has 2
positives out of 4, and the lab does not use balance to pick a metric.

## Limitations

- Fixed toy labels only: four and four items, not a real dataset.
- Binary 0/1 only; no multiclass, no probabilities, no thresholds.
- No model is trained; predictions are typed in as lists.
- The zero-denominator policy is a choice of this lab, not a standard
  rule in the lesson.
