import unittest

from example import preflight_tokens


class PreflightTokensTest(unittest.TestCase):
    def test_truncates_over_budget(self):
        r = preflight_tokens("one two three four", 3)
        self.assertEqual(r["retained"], ["one", "two", "three"])
        self.assertEqual(r["removed_count"], 1)
        self.assertTrue(r["truncated"])

    def test_empty_input(self):
        r = preflight_tokens("", 3)
        self.assertEqual(r["retained"], [])
        self.assertEqual(r["removed_count"], 0)
        self.assertFalse(r["truncated"])

    def test_negative_budget_raises(self):
        with self.assertRaises(ValueError):
            preflight_tokens("one two", -1)

    def test_exact_fit_not_truncated(self):
        r = preflight_tokens("one two three four", 4)
        self.assertEqual(r["retained"], ["one", "two", "three", "four"])
        self.assertEqual(r["removed_count"], 0)
        self.assertFalse(r["truncated"])

    def test_budget_zero_retains_none(self):
        r = preflight_tokens("one two", 0)
        self.assertEqual(r["retained"], [])
        self.assertEqual(r["removed_count"], 2)
        self.assertTrue(r["truncated"])


if __name__ == "__main__":
    unittest.main()
