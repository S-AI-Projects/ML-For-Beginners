"""Tests compare the checker to a small independent expected-result table."""

import copy
import json
import subprocess
import sys
import unittest
from pathlib import Path

import example


EXPECTED = [
    {"id": "prepared-data", "result": "PASS", "issues": []},
    {"id": "model-evaluation", "result": "FAIL", "issues": ["missing or empty: asset"]},
    {
        "id": "new-prediction",
        "result": "REVIEW",
        "issues": ["control tag validation is not listed for threat prediction-misuse; review needed"],
    },
]


class RubricCheckerTests(unittest.TestCase):
    def test_fixtures_match_independent_expected_table(self):
        # Both approaches receive the exact same fixture list; EXPECTED is a
        # literal oracle, independent of the checker's categorization code.
        actual = [example.check_scenario(row) for row in copy.deepcopy(example.FIXTURES)]
        self.assertEqual(actual, EXPECTED)

    def test_complete_scenario_passes(self):
        self.assertEqual(example.check_scenario(example.FIXTURES[0]), EXPECTED[0])

    def test_missing_asset_fails(self):
        result = example.check_scenario(example.FIXTURES[1])
        self.assertEqual(result["result"], "FAIL")
        self.assertIn("asset", result["issues"][0])

    def test_unrelated_control_is_flagged_for_review(self):
        result = example.check_scenario(example.FIXTURES[2])
        self.assertEqual(result["result"], "REVIEW")
        self.assertIn("review needed", result["issues"][0])

    def test_unknown_tags_and_blank_content_are_review_or_failure(self):
        unknown = dict(example.FIXTURES[0], threat="[novel-risk] Something could happen.")
        self.assertEqual(example.check_scenario(unknown)["result"], "REVIEW")
        blank = dict(example.FIXTURES[0], residual_risk="  ")
        self.assertEqual(example.check_scenario(blank)["result"], "FAIL")

    def test_cli_in_fresh_process_matches_expected_table(self):
        completed = subprocess.run(
            [sys.executable, str(Path(__file__).with_name("example.py"))],
            check=True,
            capture_output=True,
            text=True,
        )
        self.assertEqual(json.loads(completed.stdout), EXPECTED)


if __name__ == "__main__":
    unittest.main()
