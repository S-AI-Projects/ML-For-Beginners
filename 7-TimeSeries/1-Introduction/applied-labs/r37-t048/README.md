# Chronological split: failure and recovery example

**Label:** toy timestamped fixture, not a forecasting model.

This lab shows a chronological train/validation/test split for timestamped
observations. It includes one invalid batch (a missing value) that the
function rejects, followed by the next valid batch, which it splits
correctly.

## Prerequisites

Python 3 standard library and a local checkout. The local fixture is
mandatory; any optional real-service extension needs separately supplied
credentials/hardware and is not part of this task.

## Invocation

From this directory:

```bash
python3 example.py
```

Tests, from the repository root:

```bash
python3 -m unittest discover -s 7-TimeSeries/1-Introduction/applied-labs/r37-t048 -p "test_*.py"
```

## Fixture

Each observation is a `(timestamp, value)` pair with an integer timestamp.
The CLI builds three batches in code, with no files read:

- a valid batch of ten observations, timestamps 1 to 10;
- an invalid batch of the same ten timestamps, where timestamp 4 has the
  value `None`;
- the next valid batch of ten observations, timestamps 11 to 20.

## Expected output

This block is the CLI's real stdout, copied byte for byte from a run of
`python3 example.py`:

```text
toy timestamped fixture, not a forecasting model
valid batch (10 observations):
  train      n=6  t=1-6
  validation n=2  t=7-8
  test       n=2  t=9-10
invalid batch (missing value):
  error: missing value at timestamp 4
recovered, next valid batch (10 observations):
  train      n=6  t=11-16
  validation n=2  t=17-18
  test       n=2  t=19-20
```

## Split rule and rounding

`chronological_split(observations)` works in four steps:

1. It validates the input (see the invalid cases below).
2. It copies the input into a new list and sorts the copy by timestamp,
   so shuffled input gives the same result. The caller's list is not
   changed.
3. It takes sizes from the sorted length `n` with integer floor division:
   `n_train = n * 60 // 100` and `n_val = n * 20 // 100`. The remainder
   is `n_test`. For ten observations this gives 6, 2 and 2.
4. It returns the earliest `n_train` rows as training data, the next
   `n_val` rows as validation data, and the rest as test data.

## Leakage prevention

Because the rows are sorted and cut at fixed positions, every training
timestamp is earlier than every validation timestamp, and every validation
timestamp is earlier than every test timestamp. The tests check this
(`max(train) < min(validation)` and `max(validation) < min(test)`) for
twenty observations.

## Invalid cases and messages

Each case raises `ValueError` with a message that names the offending
timestamp (or the count):

| Case | Message |
| --- | --- |
| Timestamp appears twice | `duplicate timestamp 4` |
| Value is `None` | `missing value at timestamp 4` |
| Fewer than 5 observations | `need at least 5 observations, got 4` |

Five is the minimum because a three-way split of fewer rows would leave
at least one part empty.

## Failure and recovery

The invalid batch fails on the missing value at timestamp 4, so the call
raises `ValueError`, and the CLI prints the message and continues.
The function keeps no state between calls, so the failed call leaves
nothing behind. The next valid batch goes through the same function and
splits into train 11 to 16, validation 17 to 18 and test 19 to 20. The
test `test_recovery_after_invalid_batch` checks this sequence.

## How it relates to the lesson

The lesson describes a time series as data "indexed (or listed or graphed)
in time order", and it notes that ARIMA models work on ordered data. This
lab uses that ordering: the split keeps the time order, so the training
part comes before the test part. Leakage prevention and the idea of a
split point are this lab's additions, not claims from the lesson text.

## Limitations

- Timestamps must be integers. The code does not parse dates.
- There are no gap or frequency checks, so missing time steps are not
  detected.
- No model is trained, and no forecast or error metric is computed. The
  output shows only how the rows are split.
- The fixture is a toy example and not a forecasting model.
