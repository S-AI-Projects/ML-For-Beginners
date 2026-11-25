import unittest

from example import preflight


class PreflightTests(unittest.TestCase):
    def test_budget_three_reports_prefix_and_removed_token(self):
        result = preflight("one two three four", 3)
        self.assertEqual(result["report"], {
            "retained_tokens": ["one", "two", "three"],
            "removed_count": 1,
            "truncated": True,
        })

    def test_trace_states_match_final_output(self):
        result = preflight("one two three four", 3)
        token_state = result["trace"][1]["tokens"]
        budget_state = result["trace"][2]
        final = result["report"]
        self.assertEqual(budget_state["retained"], token_state[:3])
        self.assertEqual(budget_state["removed"], token_state[3:])
        self.assertEqual(final["retained_tokens"], budget_state["retained"])
        self.assertEqual(final["removed_count"], len(token_state) - len(final["retained_tokens"]))
        self.assertEqual(final["truncated"], final["removed_count"] > 0)

    def test_empty_input_retains_no_tokens(self):
        result = preflight("", 3)
        self.assertEqual(result["report"], {
            "retained_tokens": [], "removed_count": 0, "truncated": False
        })
        self.assertEqual(result["trace"][1]["tokens"], [])

    def test_negative_budget_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "budget must be zero or greater"):
            preflight("one two", -1)


if __name__ == "__main__":
    unittest.main()
