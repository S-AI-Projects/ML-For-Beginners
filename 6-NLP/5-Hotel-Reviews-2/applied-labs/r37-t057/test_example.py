"""Unit tests for token budget preflight worked example with checks (R37-T057)."""

import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(__file__))
from example import (
    check_token_budget_worked_example,
    get_canonical_worked_example,
    MOCK_LIMITATIONS,
)


class TestTokenBudgetWorkedExample(unittest.TestCase):
    def test_canonical_worked_example_regression(self):
        # Executes the exact canonical worked example as a regression test
        canonical = get_canonical_worked_example()
        res = canonical["actual_result"]

        self.assertEqual(res["retained_tokens"], ["one", "two", "three"])
        self.assertEqual(res["removed_count"], 1)
        self.assertTrue(res["truncated"])
        self.assertEqual(res["total_tokens"], 4)
        self.assertEqual(res["retained_count"], 3)

    def test_empty_input_retains_none(self):
        # Empty input retains none
        res = check_token_budget_worked_example("", 3)
        self.assertEqual(res["retained_tokens"], [])
        self.assertEqual(res["removed_count"], 0)
        self.assertFalse(res["truncated"])

    def test_negative_budget_rejected(self):
        # Reject a negative budget
        with self.assertRaises(ValueError) as ctx:
            check_token_budget_worked_example("one two three four", -1)
        self.assertIn("negative budget", str(ctx.exception).lower())

    def test_boundary_zero_budget(self):
        res = check_token_budget_worked_example("hotel review text", 0)
        self.assertEqual(res["retained_tokens"], [])
        self.assertEqual(res["removed_count"], 3)
        self.assertTrue(res["truncated"])

    def test_exact_budget_match(self):
        res = check_token_budget_worked_example("alpha beta gamma", 3)
        self.assertEqual(res["retained_tokens"], ["alpha", "beta", "gamma"])
        self.assertEqual(res["removed_count"], 0)
        self.assertFalse(res["truncated"])

    def test_mock_limitations_stated(self):
        self.assertGreaterEqual(len(MOCK_LIMITATIONS), 3)

    @unittest.skip("Deliberate failure test: demonstrates framework exits non-zero on failure")
    def test_deliberate_wrong_result(self):
        res = check_token_budget_worked_example("one two three four", 3)
        self.assertEqual(res["removed_count"], 999)


if __name__ == "__main__":
    unittest.main()
