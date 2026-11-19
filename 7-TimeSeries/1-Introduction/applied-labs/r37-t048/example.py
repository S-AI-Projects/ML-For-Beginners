"""Chronological train/validation/test split for a toy time series.

toy timestamped fixture, not a forecasting model

Observations are (timestamp, value) pairs with integer timestamps. The
split sorts them by timestamp, keeps the earliest 60% for training, the
next 20% for validation and the latest 20% for testing. Sizes use integer
floor division: n_train = n * 60 // 100 and n_val = n * 20 // 100; the
remainder goes to test.

Python 3 standard library and a local checkout. The local fixture is
mandatory; any optional real-service extension needs separately supplied
credentials/hardware and is not part of this task.
"""

MIN_OBSERVATIONS = 5


def chronological_split(observations):
    """Split (timestamp, value) pairs into train, validation and test.

    Raises ValueError for fewer than five observations, a duplicate
    timestamp, or a missing (None) value. The input is never mutated.
    """
    rows = list(observations)
    if len(rows) < MIN_OBSERVATIONS:
        raise ValueError(
            f"need at least {MIN_OBSERVATIONS} observations, "
            f"got {len(rows)}"
        )
    seen = set()
    for timestamp, value in rows:
        if value is None:
            raise ValueError(f"missing value at timestamp {timestamp}")
        if timestamp in seen:
            raise ValueError(f"duplicate timestamp {timestamp}")
        seen.add(timestamp)
    rows = sorted(rows, key=lambda row: row[0])
    n = len(rows)
    n_train = n * 60 // 100
    n_val = n * 20 // 100
    train = rows[:n_train]
    validation = rows[n_train:n_train + n_val]
    test = rows[n_train + n_val:]
    return train, validation, test


def _span(part):
    return f"{part[0][0]}-{part[-1][0]}"


def _show(batch):
    names = ("train", "validation", "test")
    for name, part in zip(names, chronological_split(batch)):
        print(f"  {name:<10} n={len(part)}  t={_span(part)}")


def main():
    print("toy timestamped fixture, not a forecasting model")
    valid = [(t, t * 1.5) for t in range(1, 11)]
    print(f"valid batch ({len(valid)} observations):")
    _show(valid)
    broken = [(t, None if t == 4 else t * 1.5) for t in range(1, 11)]
    print("invalid batch (missing value):")
    try:
        chronological_split(broken)
    except ValueError as error:
        print(f"  error: {error}")
    nxt = [(t, t * 1.5) for t in range(11, 21)]
    print(f"recovered, next valid batch ({len(nxt)} observations):")
    _show(nxt)


if __name__ == "__main__":
    main()
