import copy
import unittest

from example import QUESTIONS, SCENARIOS, check_scenario


class TestRubric(unittest.TestCase):
    def test_complete_scenario_passes(self):
        self.assertEqual(check_scenario(SCENARIOS["complete"]), {"status": "pass", "problems": [], "flags": []})

    def test_scenario_without_asset_fails(self):
        r = check_scenario(SCENARIOS["no_asset"])
        self.assertEqual(r["status"], "fail")
        self.assertIn("missing asset", r["problems"])

    def test_unrelated_control_is_flagged_for_review(self):
        r = check_scenario(SCENARIOS["unrelated_control"])
        self.assertEqual((r["status"], r["problems"]), ("review", []))
        self.assertEqual(len(r["flags"]), 1)

    def test_blank_and_invalid_fields(self):
        s = copy.deepcopy(SCENARIOS["complete"])
        s["asset"] = "   "
        self.assertEqual(check_scenario(s)["status"], "fail")
        s = copy.deepcopy(SCENARIOS["complete"])
        s["residual_risk"]["level"] = "severe"
        self.assertIn("invalid residual_risk.level", check_scenario(s)["problems"])

    def test_missing_sections_fail(self):
        for key in ("threat", "control", "residual_risk"):
            s = copy.deepcopy(SCENARIOS["complete"])
            del s[key]
            self.assertIn(f"missing {key}", check_scenario(s)["problems"])

    def test_non_dict_rejected(self):
        for bad in (None, "text", [1], 5):
            with self.assertRaises(ValueError):
                check_scenario(bad)

    def test_three_scenarios(self):
        self.assertEqual(len(SCENARIOS), 3)


class TestAppliedQuestions(unittest.TestCase):
    def test_three_questions_of_the_required_kinds(self):
        self.assertEqual(
            [q["kind"] for q in QUESTIONS],
            ["predict an output", "diagnose a failure", "choose a boundary policy"],
        )

    def test_each_question_has_answer_rationale_and_check(self):
        for q in QUESTIONS:
            self.assertTrue(q["answer"].strip(), q["id"])
            self.assertTrue(q["rationale"].strip(), q["id"])
            self.assertTrue(callable(q["check"]), q["id"])

    def test_each_answer_check_passes(self):
        for q in QUESTIONS:
            self.assertTrue(q["check"](), f"{q['id']} check failed")

    def test_q1_prediction_is_exactly_review(self):
        self.assertEqual(QUESTIONS[0]["answer"], check_scenario(SCENARIOS["unrelated_control"])["status"])

    def test_deliberate_wrong_answers_are_detected(self):
        # Wrong claims must not match what the code really does.
        self.assertNotEqual(check_scenario(SCENARIOS["unrelated_control"])["status"], "pass")
        self.assertNotEqual(check_scenario(SCENARIOS["unrelated_control"])["status"], "fail")
        s = copy.deepcopy(SCENARIOS["unrelated_control"])
        s["asset"] = ""
        self.assertNotEqual(check_scenario(s)["status"], "review")


if __name__ == "__main__":
    unittest.main()
