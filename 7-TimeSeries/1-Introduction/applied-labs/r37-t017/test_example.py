import json
from pathlib import Path
import subprocess
import sys
import unittest

from example import FIXTURE, split_observations


class SplitObservationsTests(unittest.TestCase):
    def test_shuffled_ten_rows_are_sorted_before_60_20_20_split(self):
        result = split_observations(FIXTURE)
        self.assertEqual([len(result[key]) for key in ("train", "validation", "test")], [6, 2, 2])
        timestamps = [
            row["timestamp"]
            for key in ("train", "validation", "test")
            for row in result[key]
        ]
        self.assertEqual(timestamps, [
            "2024-01-01T00:00:00Z", "2024-01-02T00:00:00Z",
            "2024-01-03T00:00:00Z", "2024-01-04T00:00:00Z",
            "2024-01-05T00:00:00Z", "2024-01-06T00:00:00Z",
            "2024-01-07T00:00:00Z", "2024-01-08T00:00:00Z",
            "2024-01-09T00:00:00Z", "2024-01-10T00:00:00Z",
        ])

    def test_small_boundary_sizes_keep_every_row_in_order(self):
        rows = [
            {"timestamp": f"2024-02-{day:02d}T00:00:00", "value": day}
            for day in range(1, 6)
        ]
        for size in range(1, len(rows) + 1):
            with self.subTest(size=size):
                result = split_observations(rows[:size])
                combined = result["train"] + result["validation"] + result["test"]
                self.assertEqual(combined, rows[:size])
                self.assertEqual(sum(map(len, result.values())), size)

    def test_duplicate_timestamp_is_rejected_even_if_timezone_spelling_differs(self):
        rows = [
            {"timestamp": "2024-01-01T00:00:00Z", "value": 1},
            {"timestamp": "2023-12-31T19:00:00-05:00", "value": 2},
        ]
        with self.assertRaisesRegex(ValueError, "timestamps must be unique"):
            split_observations(rows)

    def test_mixed_timezone_modes_are_rejected(self):
        rows = [
            {"timestamp": "2024-01-01T00:00:00Z", "value": 1},
            {"timestamp": "2024-01-02T00:00:00", "value": 2},
        ]
        with self.assertRaisesRegex(ValueError, "consistently include a timezone"):
            split_observations(rows)

    def test_command_line_example_matches_fixture_output(self):
        script = Path(__file__).with_name("example.py")
        completed = subprocess.run(
            [sys.executable, str(script)], capture_output=True, text=True, check=True
        )
        expected = split_observations(FIXTURE)
        self.assertEqual(json.loads(completed.stdout), expected)


if __name__ == "__main__":
    unittest.main()
