# R37-T017: chronological split

This worked example takes ten synthetic timestamped readings in deliberately shuffled order, validates that every timestamp is unique, sorts them, and assigns the earliest 60% to training, the next 20% to validation, and the latest 20% to testing. The later partitions never enter training. This makes the forecast origin visible: training ends on January 6, validation ends on January 8, and testing begins on January 9.

## Prerequisites and invocation

Use Python 3 (standard library only) from a local repository checkout. No data download, model, credentials, cloud service, GPU, or physical device is used.

```bash
python3 7-TimeSeries/1-Introduction/applied-labs/r37-t017/example.py
python3 -m unittest discover -s 7-TimeSeries/1-Introduction/applied-labs/r37-t017 -p "test_*.py"
```

The first command prints the result below. The second executes the same ten-row fixture, checks sorting and 6/2/2 counts, covers small boundary sizes, rejects duplicate timestamps (including equal instants written with different UTC offsets), rejects mixed timezone modes, and verifies the command-line output in a fresh Python process.

## Fixture and result

`example.py` contains this local synthetic fixture. Each pair is `timestamp → value`; the rows are shown in their input order:

```text
Jan 06 → 60, Jan 02 → 20, Jan 10 → 100, Jan 01 → 10, Jan 07 → 70,
Jan 04 → 40, Jan 09 → 90, Jan 03 → 30, Jan 08 → 80, Jan 05 → 50
```

After sorting, the first six observations form training, the next two validation, and the final two test. The exact output is:

```json
{
  "train": [
    {"timestamp": "2024-01-01T00:00:00Z", "value": 10},
    {"timestamp": "2024-01-02T00:00:00Z", "value": 20},
    {"timestamp": "2024-01-03T00:00:00Z", "value": 30},
    {"timestamp": "2024-01-04T00:00:00Z", "value": 40},
    {"timestamp": "2024-01-05T00:00:00Z", "value": 50},
    {"timestamp": "2024-01-06T00:00:00Z", "value": 60}
  ],
  "validation": [
    {"timestamp": "2024-01-07T00:00:00Z", "value": 70},
    {"timestamp": "2024-01-08T00:00:00Z", "value": 80}
  ],
  "test": [
    {"timestamp": "2024-01-09T00:00:00Z", "value": 90},
    {"timestamp": "2024-01-10T00:00:00Z", "value": 100}
  ]
}
```

## Scope and limitations

This is a deterministic simulation of a local data split, not a mock of a service and not a forecasting model. ISO 8601 timestamps must consistently either include a timezone or omit one. The example does not resample irregular data, handle missing values, select forecast horizons, fit preprocessing, or assess forecast quality. In a real workflow, those choices depend on the data and forecast origin; any learned preprocessing must be fit using training data only.
