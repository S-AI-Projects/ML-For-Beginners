import unittest

from example import preflight, whitespace_tokenizer


class PreflightTests(unittest.TestCase):
    def test_budget_truncates_and_reports_removed_count(self):
        actual = preflight("one two three four", 3)
        self.assertEqual(
            actual,
            {"retained_tokens": ["one", "two", "three"], "removed_count": 1, "truncated": True},
        )

    def test_empty_input_retains_no_tokens(self):
        self.assertEqual(
            preflight("", 3),
            {"retained_tokens": [], "removed_count": 0, "truncated": False},
        )

    def test_zero_budget_removes_every_token(self):
        self.assertEqual(
            preflight("one two", 0),
            {"retained_tokens": [], "removed_count": 2, "truncated": True},
        )

    def test_negative_budget_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "non-negative"):
            preflight("one", -1)

    def test_injected_callable_is_used(self):
        calls = []

        def fixture_tokenizer(text):
            calls.append(text)
            return ["mock-token", "second"]

        report = preflight("input text", 1, tokenizer=fixture_tokenizer)
        self.assertEqual(calls, ["input text"])
        self.assertEqual(report["retained_tokens"], ["mock-token"])
        self.assertEqual(report["removed_count"], 1)

    def test_whitespace_adapter_is_a_teaching_approximation(self):
        self.assertEqual(whitespace_tokenizer("one\t two\nthree"), ["one", "two", "three"])


if __name__ == "__main__":
    unittest.main()
