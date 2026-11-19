# R37-T010: Classification Evaluation - Scenario Assessment

**Label:** fixed toy labels, not a trained logistic regression model.

## Prerequisites

Python 3 standard library and a local checkout. The local fixture is mandatory; any optional real-service extension needs separately supplied credentials/hardware and is not part of this task.

## What It Is

A binary classification evaluation assessment for categorical predictions in logistic regression. It computes:
- Confusion matrix counts: True Positives (TP), False Negatives (FN), False Positives (FP), and True Negatives (TN).
- Precision: `TP / (TP + FP)`.
- Recall: `TP / (TP + FN)`.
- Explicit zero-denominator policy: `0.0` when denominators are zero.

## Applied Questions and Assessment

### Q1: Predict an Output
- **Question:** Given `y_true = [1, 1, 1, 0]` and `y_pred = [1, 0, 0, 1]`, predict the confusion matrix counts and resulting precision and recall.
- **Answer:** `TP=1 FN=2 FP=1 TN=0 precision=0.5000 recall=0.3333`.
- **Rationale:** Index 0 is an agreed positive ($1 \to 1$, TP=1). Indices 1 and 2 are positives predicted as negative ($1 \to 0$, FN=2). Index 3 is negative predicted as positive ($0 \to 1$, FP=1). No index is true negative ($0 \to 0$, TN=0). Precision $= 1 / (1 + 1) = 0.5000$. Recall $= 1 / (1 + 2) = 1/3 \approx 0.3333$.
- **Executable Check:** `test_q1_predict_output_executable_check`.

### Q2: Diagnose a Failure
- **Question:** A developer reports precision evaluates to `0.3333` instead of `0.5000` on the Q1 data. What failure explains this?
- **Answer:** Arguments were supplied in inverted order: `precision(y_pred, y_true)` instead of `precision(y_true, y_pred)`.
- **Rationale:** Inverting arguments exchanges False Positives with False Negatives in the confusion calculation. Consequently, $\frac{\text{TP}}{\text{TP} + \text{FP}}$ becomes $\frac{\text{TP}}{\text{TP} + \text{FN}}$, which calculates recall ($1/3$) instead of precision ($1/2$).
- **Executable Check:** `test_q2_diagnose_swapped_arguments_check`.

### Q3: Choose a Boundary Policy
- **Question:** When a classifier predicts zero positive instances ($y_{\text{pred}} = [0, 0, 0, 0]$), why adopt a policy returning `0.0` rather than `1.0`, `NaN`, or raising an exception?
- **Answer:** `0.0` safely preserves pipeline continuity while conservatively reflecting zero positive predictive utility.
- **Rationale:** Raising an exception crashes automated batch evaluation pipelines. Returning `NaN` propagates undefined IEEE floating point errors to downstream scoreboards. Returning `1.0` falsely rewards a model that made no positive predictions. `0.0` accurately reflects that zero predicted positives were correct.
- **Executable Check:** `test_q3_boundary_policy_executable_check`.

## Invocation

From the repository root:

```bash
python3 2-Regression/4-Logistic/applied-labs/r37-t010/example.py
```

Run unit tests from the repository root:

```bash
python3 -m unittest discover -s 2-Regression/4-Logistic/applied-labs/r37-t010 -p "test_*.py"
```

## Fixture and Expected Output

Expected CLI output:

```text
fixed toy labels, not a trained logistic regression model
headline TP=1 FN=1 FP=1 TN=1
precision=0.5000 recall=0.5000
Q1 Predict an output: TP=1 FN=2 FP=1 TN=0 precision=0.5000 recall=0.3333
Q2 Diagnose a failure: precision(y_pred, y_true)=0.3333 equals recall=0.3333
Q3 Choose a boundary policy: precision with no positive predictions=0.0000
```

## Limitations

- Uses fixed toy binary labels; no logistic regression coefficients, odds ratios, or sigmoid functions are computed.
- Binary classification only; does not extend to multiclass or multinomial logistic regression.
- Makes no claims about real hardware, cloud service behavior, or trained model performance.
