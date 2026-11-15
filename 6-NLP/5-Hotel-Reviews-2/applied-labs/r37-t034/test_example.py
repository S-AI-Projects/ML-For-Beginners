import unittest

from example import check_invariants, preflight


class TestPreflight(unittest.TestCase):
    def test_contract_example(self):
        r = preflight("one two three four", 3)
        self.assertEqual(r["retained"], ["one", "two", "three"])
        self.assertEqual(r["removed_count"], 1)
        self.assertTrue(r["truncated"])

    def test_trace_records_each_step_in_order(self):
        r = preflight("one two three four", 3)
        self.assertEqual([s["step"] for s in r["trace"]], ["tokenize", "measure", "truncate"])
        self.assertEqual(r["trace"][0]["tokens"], ["one", "two", "three", "four"])
        self.assertEqual(
            r["trace"][1],
            {"step": "measure", "token_count": 4, "budget": 3, "over_budget": True},
        )
        self.assertEqual(
            r["trace"][2],
            {"step": "truncate", "retained": ["one", "two", "three"], "removed_count": 1},
        )

    def test_trace_state_links_to_final_output(self):
        # The intermediate state must agree with the final output.
        r = preflight("a b c d e", 2)
        tokenize, measure, truncate = r["trace"]
        self.assertEqual(truncate["retained"], r["retained"])
        self.assertEqual(truncate["removed_count"], r["removed_count"])
        self.assertEqual(measure["token_count"], len(tokenize["tokens"]))
        self.assertEqual(measure["token_count"], len(r["retained"]) + r["removed_count"])

    def test_empty_input_retains_none(self):
        r = preflight("", 3)
        self.assertEqual(r["retained"], [])
        self.assertEqual(r["removed_count"], 0)
        self.assertFalse(r["truncated"])

    def test_whitespace_only_input(self):
        r = preflight("  \t\n ", 3)
        self.assertEqual(r["retained"], [])

    def test_under_and_exactly_at_budget(self):
        r = preflight("one two", 3)
        self.assertEqual((r["retained"], r["removed_count"], r["truncated"]), (["one", "two"], 0, False))
        r = preflight("one two three", 3)
        self.assertEqual((r["retained"], r["removed_count"], r["truncated"]), (["one", "two", "three"], 0, False))

    def test_budget_zero_removes_everything(self):
        r = preflight("one two", 0)
        self.assertEqual((r["retained"], r["removed_count"]), ([], 2))

    def test_extra_whitespace_is_not_a_token(self):
        r = preflight("  one   two  ", 5)
        self.assertEqual(r["tokens"], ["one", "two"])

    def test_negative_budget_rejected(self):
        with self.assertRaises(ValueError):
            preflight("one two", -1)

    def test_invalid_types_rejected(self):
        for text, budget in (("a b", 2.5), ("a b", "3"), ("a b", True), (None, 3), (5, 3)):
            with self.assertRaises(ValueError):
                preflight(text, budget)

    def test_invariants_hold_over_many_inputs(self):
        for text in ("", "a", "a b", "a b c d e f g", "  x  y "):
            for budget in range(0, 9):
                check_invariants(preflight(text, budget))

    def test_invariant_check_detects_corrupted_state(self):
        r = preflight("one two three four", 3)
        r["removed_count"] = 0  # corrupt the state
        with self.assertRaises(AssertionError):
            check_invariants(r)

    def test_deliberate_wrong_result_is_detected(self):
        r = preflight("one two three four", 3)
        self.assertNotEqual(r["retained"], ["one", "two", "three", "four"])
        self.assertNotEqual(r["removed_count"], 0)


if __name__ == "__main__":
    unittest.main()
