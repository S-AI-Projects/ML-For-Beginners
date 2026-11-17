# R37-T045: classification evaluation, offline service adapter

**Label:** offline mock adapter, not a real model service.

This lab computes a binary confusion matrix, precision and recall from true
labels and predicted labels. The predictions come from a callable that stands
in for a hosted model service. The callable is a local, deterministic lookup
table, so the lab runs offline.

## Prerequisites

Python 3 standard library and a local checkout. The local fixture is mandatory; any optional real-service extension needs separately supplied credentials/hardware and is not part of this task.

## Files

- `example.py`: the evaluation function, the local adapter and a small CLI.
- `test_example.py`: unittest suite for the evaluation contract.

## Invocation

Run from the repository root:

```bash
python3 2-Regression/4-Logistic/applied-labs/r37-t045/example.py
```

Run the tests (the required check):

```bash
python3 -m unittest discover -s 2-Regression/4-Logistic/applied-labs/r37-t045 -p "test_*.py"
```

## Fixture

- Inputs: `"a"`, `"b"`, `"c"`, `"d"`.
- True labels `y_true = [1, 1, 0, 0]`.
- The local adapter returns fixed predictions from a lookup table:
  `a -> 1`, `b -> 0`, `c -> 1`, `d -> 0`, so `y_pred = [1, 0, 1, 0]`.

## Expected output

This is the CLI's real stdout:

```text
offline mock adapter, not a real model service
inputs:  a b c d
y_true:  1 1 0 0
y_pred:  1 0 1 0
TP=1 FN=1 FP=1 TN=1
precision=0.5 recall=0.5
zero-denominator case (predict all 0):
  TP=0 FP=0 precision=0.0
zero-denominator case (no actual positives):
  TP=0 FN=0 recall=0.0
```

## Definitions

For binary labels, with a positive class of `1`:

- TP (true positive): actual 1, predicted 1.
- FN (false negative): actual 1, predicted 0.
- FP (false positive): actual 0, predicted 1.
- TN (true negative): actual 0, predicted 0.
- precision = TP / (TP + FP): of the items predicted positive, the share that
  really are positive.
- recall = TP / (TP + FN): of the actual positives, the share that were found.

## Zero-denominator policy

- precision is `0.0` when there are no positive predictions (TP + FP == 0).
- recall is `0.0` when there are no actual positives (TP + FN == 0).
- Empty input gives all counts 0 and precision = recall = `0.0`.

The policy is stated in code as `ZERO_DENOMINATOR_VALUE` in `example.py`. It is
a convention chosen so the output is always a number. It is not a claim that the
metric is meaningful in those cases.

## Validation

- `y_true` and the inputs must have equal length, otherwise `ValueError`.
- `y_true` may contain only `0` or `1`, otherwise `ValueError`.
- The callable must return `0` or `1` for each input, otherwise `ValueError`.

## Interface and adapter

`evaluate(y_true, inputs, predict)` takes a list of labels, a list of inputs and
a callable `predict(x)` that returns `0` or `1`. `evaluate` never names a
concrete service, so any callable with that signature can be used. The tests
check this with a different callable.

`mock_adapter(x)` is the local adapter. It returns `LOOKUP[x]` and is called
exactly once per input, in order. An exception raised by the adapter is not
caught.

## How this relates to the lesson

The lesson's confusion-matrix section explains that the matrix counts true and
false positives and negatives, and that precision and recall are read from it.
This lab uses the same definitions and shows how the denominators can be zero.
The lesson also points out that the order of predicted and true labels matters
for the counts. The validation and fixed inputs here make that order explicit.
Class balance is only shown through the small fixture (two positives, two
negatives).

## Not established by this mock

A real model service behaves differently in ways this lab does not test:

- network latency, timeouts and retries;
- authentication, authorization and rate limits;
- error responses and partial failures;
- nondeterminism of the model or the service;
- the real model's decision threshold and its accuracy;
- schema drift between client and service;
- cost.

## Limitations

- This is not a trained model. It says nothing about model performance,
  accuracy or the quality of any real classifier.
- The predictions are a fixed table, not a function of the inputs.
- Only binary labels are supported.
- The fixture has four items, so the numbers illustrate the arithmetic and
  nothing more.
- No claim is made about real hardware or cloud-service behaviour.
