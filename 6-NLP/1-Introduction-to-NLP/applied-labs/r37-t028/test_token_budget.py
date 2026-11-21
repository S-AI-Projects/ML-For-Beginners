"""
Unit tests for r37-t028: token-budget preflight — failure and recovery example.

Run with:
    python3 -m unittest discover -s 6-NLP/1-Introduction-to-NLP/applied-labs/r37-t028 -p "test_*.py" -v
"""

import unittest

from example import (
    exercise_failure_and_recovery,
    preflight_token_budget,
    tokenize_approx,
)


class TestTokenBudgetPreflightContract(unittest.TestCase):
    """
    Contract requirements:
    - Budget 3 with "one two three four" retains ['one', 'two', 'three'] and reports 1 removed token
    - Empty input retains none (empty list [])
    - Reject a negative budget (ValueError)
    """

    def test_budget_3_retains_first_three_and_reports_one_removed(self):
        res = preflight_token_budget("one two three four", budget=3)
        self.assertEqual(res["retained_tokens"], ["one", "two", "three"])
        self.assertEqual(res["removed_token_count"], 1)
        self.assertEqual(res["original_token_count"], 4)
        self.assertTrue(res["is_truncated"])

    def test_empty_input_retains_none_and_reports_zero_removed(self):
        res = preflight_token_budget("", budget=3)
        self.assertEqual(res["retained_tokens"], [])
        self.assertEqual(res["removed_token_count"], 0)
        self.assertEqual(res["original_token_count"], 0)
        self.assertFalse(res["is_truncated"])

    def test_whitespace_only_input_retains_none(self):
        res = preflight_token_budget("   \t\n  ", budget=3)
        self.assertEqual(res["retained_tokens"], [])
        self.assertEqual(res["removed_token_count"], 0)

    def test_negative_budget_raises_value_error(self):
        with self.assertRaises(ValueError) as ctx:
            preflight_token_budget("one two", budget=-1)
        self.assertIn("Budget must be non-negative", str(ctx.exception))

    def test_missing_none_input_raises_value_error(self):
        with self.assertRaises(ValueError) as ctx:
            preflight_token_budget(None, budget=5)
        self.assertIn("text cannot be None", str(ctx.exception))


class TestFailureAndRecovery(unittest.TestCase):
    """
    Exercise documented invalid/missing-data case, explain the error,
    and demonstrate recovery on next valid input.
    """

    def test_failure_and_recovery_flow(self):
        flow = exercise_failure_and_recovery()
        # Step 1 should have caught expected negative budget error
        self.assertEqual(flow["step1_negative_budget"]["status"], "CAUGHT_EXPECTED_ERROR")
        self.assertEqual(flow["step1_negative_budget"]["error_type"], "ValueError")

        # Step 2 should have caught expected missing data error
        self.assertEqual(flow["step2_missing_data"]["status"], "CAUGHT_EXPECTED_ERROR")
        self.assertEqual(flow["step2_missing_data"]["error_type"], "ValueError")

        # Step 3 must recover cleanly on next valid input
        self.assertEqual(flow["step3_recovery"]["status"], "RECOVERED_SUCCESSFULLY")
        self.assertEqual(flow["step3_recovery"]["result"]["retained_tokens"], ["one", "two", "three"])
        self.assertEqual(flow["step3_recovery"]["result"]["removed_token_count"], 1)


class TestDeliberateFailure(unittest.TestCase):
    """
    Framework check: deliberate wrong expected result causes test to fail,
    demonstrating the framework exits non-zero on failure.
    """

    @unittest.skip("Deliberate failure demo: remove skip to verify non-zero exit")
    def test_deliberate_wrong_removed_count_DEMO_FAIL(self):
        res = preflight_token_budget("one two three four", budget=3)
        # Intentionally wrong expected removed count (99 instead of 1)
        self.assertEqual(res["removed_token_count"], 99, "DEMO: intentional failure")


if __name__ == "__main__":
    unittest.main()
