"""Chronological evaluation split — compare two approaches for 7-TimeSeries/1-Introduction."""

import math
from typing import Any, Dict, List, Tuple

MOCK_LIMITATIONS = [
    "Uses discrete integer/string timestamps; does not parse localized ISO-8601 or timezone offsets.",
    "Uniform fixed ratio (60/20/20); does not perform sliding/expanding window walk-forward validation.",
    "Does not handle seasonal frequency adjustment (e.g., business day calendars, holiday gaps).",
    "Local deterministic list partitioning only; does not load external time-series dataframes.",
]


def validate_and_sort_observations(records: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Validates uniqueness of timestamps and sorts observations chronologically."""
    if not records:
        return []

    seen = set()
    for r in records:
        ts = r.get("timestamp")
        if ts is None:
            raise ValueError("Observation missing 'timestamp' field.")
        if ts in seen:
            raise ValueError(f"Duplicate timestamp detected: '{ts}'. Observations must have unique timestamps.")
        seen.add(ts)

    # Sort strictly by timestamp ascending
    return sorted(records, key=lambda x: x["timestamp"])


def chronological_split_direct(records: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
    """Approach A: Direct index slicing based on exact proportional split (60% train, 20% val, 20% test)."""
    sorted_recs = validate_and_sort_observations(records)
    n = len(sorted_recs)
    if n == 0:
        return {"train": [], "val": [], "test": []}

    train_end = math.floor(n * 0.6)
    val_end = train_end + math.floor(n * 0.2)

    train = sorted_recs[:train_end]
    val = sorted_recs[train_end:val_end]
    test = sorted_recs[val_end:]

    return {"train": train, "val": val, "test": test}


def chronological_split_independent_calc(records: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
    """Approach B: Simpler independent calculation evaluating normalized ordinal rank percentiles."""
    sorted_recs = validate_and_sort_observations(records)
    n = len(sorted_recs)
    if n == 0:
        return {"train": [], "val": [], "test": []}

    train, val, test = [], [], []
    for rank, item in enumerate(sorted_recs):
        # Fractional position in [0.0, 1.0)
        fraction = rank / n
        if fraction < 0.6:
            train.append(item)
        elif fraction < 0.8:
            val.append(item)
        else:
            test.append(item)

    return {"train": train, "val": val, "test": test}


def compare_split_approaches(records: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Runs both split approaches on identical input and verifies strict agreement."""
    res_a = chronological_split_direct(records)
    res_b = chronological_split_independent_calc(records)

    identical = (res_a == res_b)
    return {
        "approach_a_direct": {
            "train_len": len(res_a["train"]),
            "val_len": len(res_a["val"]),
            "test_len": len(res_a["test"]),
        },
        "approach_b_independent": {
            "train_len": len(res_b["train"]),
            "val_len": len(res_b["val"]),
            "test_len": len(res_b["test"]),
        },
        "approaches_agree": identical,
        "splits": res_a,
    }


def make_ten_sample_observations() -> List[Dict[str, Any]]:
    """Creates 10 ordered observations."""
    return [{"timestamp": i, "value": 100 + i * 5} for i in range(1, 11)]


if __name__ == "__main__":
    import json
    sample = make_ten_sample_observations()
    print("Comparison of approaches on 10 observations:")
    print(json.dumps(compare_split_approaches(sample), indent=2))
