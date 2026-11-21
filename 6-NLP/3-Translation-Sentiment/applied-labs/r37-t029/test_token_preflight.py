"""
Unit tests for r37-t029: token-budget preflight — runnable concept example.

Run with:
    python3 -m unittest discover -s 6-NLP/3-Translation-Sentiment/applied-labs/r37-t029 -p "test_*.py" -v
"""

import unittest

from example import (
    check_token_budget,
    tokenize_approx,
)


class TestTokenBudgetConceptContract(unittest.TestCase):
    """
    Contract requirements:
    - Budget 3 with "one two three four" retains ['one', 'two', 'three'] and reports 1 removed token
    - Empty input retains none (empty list [])
    - Reject a negative budget (ValueError)
    """

    def test_budget_3_truncation(self):
        res = check_token_budget("one two three four", budget=3)
        self.assertEqual(res["retained_tokens"], ["one", "two", "three"])
        self.assertEqual(res["removed_token_count"], 1)
        self.assertEqual(res["original_token_count"], 4)
        self.assertTrue(res["is_truncated"])

    def test_empty_input_retains_none(self):
        res = check_token_budget("", budget=3)
        self.assertEqual(res["retained_tokens"], [])
        self.assertEqual(res["removed_token_count"], 0)
        self.assertEqual(res["original_token_count"], 0)
        self.assertFalse(res["is_truncated"])

    def test_whitespace_only_retains_none(self):
        res = check_token_budget("   \t  \n", budget=3)
        self.assertEqual(res["retained_tokens"], [])
        self.assertEqual(res["removed_token_count"], 0)

    def test_negative_budget_raises_value_error(self):
        with self.assertRaises(ValueError) as ctx:
            check_token_budget("hello world", budget=-5)
        self.assertIn("Budget must be >= 0", str(ctx.exception))

    def test_exact_budget_no_truncation(self):
        res = check_token_budget("one two three", budget=3)
        self.assertEqual(res["retained_tokens"], ["one", "two", "three"])
        self.assertEqual(res["removed_token_count"], 0)
        self.assertFalse(res["is_truncated"])


class TestDeliberateFailure(unittest.TestCase):
    """
    Framework check: deliberate wrong expected result causes test to fail,
    demonstrating the framework exits non-zero on failure.
    """

    @unittest.skip("Deliberate failure demo: remove skip to verify non-zero exit")
    def test_deliberate_wrong_tokens_DEMO_FAIL(self):
        res = check_token_budget("one two three four", budget=3)
        # Intentionally wrong expected retained tokens
        self.assertEqual(res["retained_tokens"], ["wrong", "tokens"], "DEMO: intentional failure")


if __name__ == "__main__":
    unittest.main()
