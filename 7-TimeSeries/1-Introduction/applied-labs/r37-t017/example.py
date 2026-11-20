"""Split timestamped observations into chronological train/validation/test sets.

This small local example demonstrates time-ordered splitting only. It does not
fit a forecasting model or access a remote service, dataset, or device.
"""

from datetime import datetime, timezone
import json


# Ten synthetic daily readings, deliberately supplied out of timestamp order.
FIXTURE = [
    {"timestamp": "2024-01-06T00:00:00Z", "value": 60},
    {"timestamp": "2024-01-02T00:00:00Z", "value": 20},
    {"timestamp": "2024-01-10T00:00:00Z", "value": 100},
    {"timestamp": "2024-01-01T00:00:00Z", "value": 10},
    {"timestamp": "2024-01-07T00:00:00Z", "value": 70},
    {"timestamp": "2024-01-04T00:00:00Z", "value": 40},
    {"timestamp": "2024-01-09T00:00:00Z", "value": 90},
    {"timestamp": "2024-01-03T00:00:00Z", "value": 30},
    {"timestamp": "2024-01-08T00:00:00Z", "value": 80},
    {"timestamp": "2024-01-05T00:00:00Z", "value": 50},
]


def _parse_timestamp(value):
    if not isinstance(value, str):
        raise ValueError("timestamp must be an ISO 8601 string")
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as error:
        raise ValueError("timestamp must be an ISO 8601 string") from error
    return parsed


def split_observations(observations):
    """Return earliest 60%, next 20%, and latest 20% of unique observations.

    Each observation must be a mapping with an ISO 8601 ``timestamp`` string.
    Rows are sorted before splitting. The 60% and 80% cut points are rounded
    down; any remainder belongs to test so no observation is discarded.
    Naive and timezone-aware timestamps cannot be mixed.
    """
    rows = list(observations)
    parsed_rows = []
    timestamp_mode = None
    seen = set()

    for row in rows:
        if not isinstance(row, dict) or "timestamp" not in row:
            raise ValueError("each observation must be a mapping with a timestamp")
        parsed = _parse_timestamp(row["timestamp"])
        aware = parsed.utcoffset() is not None
        if timestamp_mode is None:
            timestamp_mode = aware
        elif timestamp_mode != aware:
            raise ValueError("timestamps must consistently include a timezone or omit it")
        key = parsed.astimezone(timezone.utc) if aware else parsed
        if key in seen:
            raise ValueError("timestamps must be unique")
        seen.add(key)
        parsed_rows.append((key, row))

    ordered = [row for _, row in sorted(parsed_rows, key=lambda item: item[0])]
    train_end = (len(ordered) * 3) // 5
    validation_end = (len(ordered) * 4) // 5
    return {
        "train": ordered[:train_end],
        "validation": ordered[train_end:validation_end],
        "test": ordered[validation_end:],
    }


if __name__ == "__main__":
    print(json.dumps(split_observations(FIXTURE), indent=2))
