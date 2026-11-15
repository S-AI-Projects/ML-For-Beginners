import unittest

from example import BUDGETS, TEXT, compare_budgets, format_comparison, preflight


class TestContract(unittest.TestCase):
    def test_budget_3_example(self):
        r = preflight("one two three four", 3)
        self.assertEqual(r["retained"], ["one", "two", "three"])
        self.assertEqual(r["removed_count"], 1)
        self.assertTrue(r["truncated"])

    def test_empty_input_retains_none(self):
        r = preflight("", 3)
        self.assertEqual((r["retained"], r["removed_count"], r["truncated"]), ([], 0, False))
        self.assertEqual(r["coverage"], 1.0)  # nothing to lose
        self.assertEqual(r["budget_used"], 0.0)

    def test_negative_budget_rejected(self):
        with self.assertRaises(ValueError):
            preflight("one two", -1)

    def test_invalid_types_rejected(self):
        for text, budget in (("a b", 2.5), ("a b", "3"), ("a b", True), (None, 3), (5, 3)):
            with self.assertRaises(ValueError):
                preflight(text, budget)

    def test_budget_zero(self):
        r = preflight("one two", 0)
        self.assertEqual((r["retained"], r["removed_count"], r["coverage"], r["budget_used"]), ([], 2, 0.0, 0.0))

    def test_at_and_under_budget(self):
        self.assertFalse(preflight("one two three", 3)["truncated"])
        self.assertFalse(preflight("one two", 3)["truncated"])


class TestComparison(unittest.TestCase):
    def test_three_budgets_on_fixed_text(self):
        rows = compare_budgets(TEXT, BUDGETS)  # text has 6 tokens
        self.assertEqual([r["budget"] for r in rows], [2, 4, 8])
        self.assertEqual([len(r["retained"]) for r in rows], [2, 4, 6])
        self.assertEqual([r["removed_count"] for r in rows], [4, 2, 0])
        self.assertEqual([r["truncated"] for r in rows], [True, True, False])
        self.assertAlmostEqual(rows[0]["coverage"], 2 / 6)
        self.assertAlmostEqual(rows[1]["coverage"], 4 / 6)
        self.assertEqual(rows[2]["coverage"], 1.0)
        self.assertEqual([r["budget_used"] for r in rows], [1.0, 1.0, 0.75])

    def test_retained_is_always_a_prefix_in_order(self):
        tokens = TEXT.split()
        for r in compare_budgets(TEXT, BUDGETS):
            self.assertEqual(r["retained"], tokens[: len(r["retained"])])

    def test_invariant_retained_plus_removed_is_total(self):
        for b in range(0, 10):
            r = preflight(TEXT, b)
            self.assertEqual(len(r["retained"]) + r["removed_count"], r["total_tokens"])

    def test_observed_trade_off_is_monotonic(self):
        # Bigger budget: more tokens kept (more "cost"), never less coverage.
        rows = compare_budgets(TEXT, range(0, 10))
        for a, b in zip(rows, rows[1:]):
            self.assertLessEqual(len(a["retained"]), len(b["retained"]))
            self.assertLessEqual(a["coverage"], b["coverage"])
            self.assertGreaterEqual(a["removed_count"], b["removed_count"])

    def test_deterministic(self):
        self.assertEqual(format_comparison(TEXT, BUDGETS), format_comparison(TEXT, BUDGETS))

    def test_deliberate_wrong_result_is_detected(self):
        rows = compare_budgets(TEXT, BUDGETS)
        self.assertNotEqual([r["removed_count"] for r in rows], [4, 2, 2])
        self.assertNotEqual(rows[0]["coverage"], 1.0)


if __name__ == "__main__":
    unittest.main()
