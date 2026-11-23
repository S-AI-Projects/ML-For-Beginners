"""Unit tests for token-budget preflight boundary-case extension (R37-T052)."""

import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(__file__))
from example import check_token_budget, tokenize_whitespace, MOCK_LIMITATIONS


class TestTokenBudgetPreflight(unittest.TestCase):
    def test_normal_budget_truncation(self):
        # Budget 3 with "one two three four" retains [one,two,three] and reports one removed token
        res = check_token_budget("one two three four", 3)
        self.assertEqual(res["retained_tokens"], ["one", "two", "three"])
        self.assertEqual(res["removed_count"], 1)
        self.assertTrue(res["truncated"])
        self.assertEqual(res["total_tokens"], 4)
        self.assertEqual(res["retained_count"], 3)

    def test_empty_input_retains_none(self):
        res = check_token_budget("", 3)
        self.assertEqual(res["retained_tokens"], [])
        self.assertEqual(res["removed_count"], 0)
        self.assertFalse(res["truncated"])
        self.assertEqual(res["retained_count"], 0)

    def test_negative_budget_rejected(self):
        with self.assertRaises(ValueError) as ctx:
            check_token_budget("one two three four", -1)
        self.assertIn("negative budget", str(ctx.exception).lower())

    def test_zero_budget_boundary(self):
        res = check_token_budget("one two three", 0)
        self.assertEqual(res["retained_tokens"], [])
        self.assertEqual(res["removed_count"], 3)
        self.assertTrue(res["truncated"])

    def test_exact_budget_boundary(self):
        res = check_token_budget("one two three", 3)
        self.assertEqual(res["retained_tokens"], ["one", "two", "three"])
        self.assertEqual(res["removed_count"], 0)
        self.assertFalse(res["truncated"])

    def test_mock_limitations_stated(self):
        self.assertGreaterEqual(len(MOCK_LIMITATIONS), 3)

    @unittest.skip("Deliberate failure test: demonstrates framework exits non-zero on failure")
    def test_deliberate_wrong_result(self):
        res = check_token_budget("one two three four", 3)
        self.assertEqual(res["removed_count"], 999)


if __name__ == "__main__":
    unittest.main()
