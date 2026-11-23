# Applied Lab R37-T053: Chronological Evaluation Split — Compare Two Approaches

## Overview

This lab extends [Introduction to time series forecasting](../../README.md) by implementing and comparing two chronological evaluation split strategies.

In time series modeling, standard random train/test splits (such as scikit-learn `train_test_split(shuffle=True)`) cause **data leakage** and **lookahead bias** because future observations leak into training data. A valid evaluation split must partition timestamped records strictly chronologically:
- **Train**: Earliest 60%
- **Validation**: Next 20%
- **Test**: Latest 20%

## Method Comparison

1. **Approach A (Direct Proportional Slicing)**:
   Computes integer split boundary indices directly using `math.floor(N * 0.6)` and `train_end + math.floor(N * 0.2)`.
2. **Approach B (Normalized Ordinal Percentile)**:
   Computes rank fraction `rank / N` and assigns observations to buckets where fraction $< 0.6$, $< 0.8$, and $\ge 0.8$.

Both approaches are verified on identical inputs to ensure complete deterministic agreement.

## Fixture Specifications

- **Input**: 10 ordered observations ($t \in [1 \dots 10]$).
- **Output**: 6 Train ($t=1\dots 6$), 2 Val ($t=7\dots 8$), 2 Test ($t=9\dots 10$).
- **Shuffled Input Handling**: Automatically sorted chronologically before partition.
- **Duplicate Validation**: Rejects duplicate timestamps with `ValueError`.
- **Temporal Invariant**: $\max(	ext{train.timestamp}) < \min(	ext{val.timestamp}) < \min(	ext{test.timestamp})$.

## Mock Limitations

- Fixed 60/20/20 partitioning without rolling/expanding cross-validation windows.
- Uniform integer/string timestamps without calendar/holiday adjustments.
- In-memory list structures without database cursor streaming.

## Running Tests

```bash
python3 -m unittest discover -s 7-TimeSeries/1-Introduction/applied-labs/r37-t053 -p "test_*.py" -v
```
