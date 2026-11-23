"""Unit tests for security scenario rubric checker with state trace (R37-T054)."""

import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(__file__))
from example import (
    check_security_rubric_with_state_trace,
    FICTIONAL_SCENARIOS,
    MOCK_LIMITATIONS,
)


class TestSecurityScenarioRubric(unittest.TestCase):
    def test_complete_scenario_passes(self):
        # One complete scenario passes
        res = check_security_rubric_with_state_trace(FICTIONAL_SCENARIOS[0])
        self.assertEqual(res["status"], "passed")
        self.assertTrue(res["passed"])
        self.assertFalse(res["review_flagged"])
        self.assertTrue(res["invariant_holds"])
        self.assertEqual(len(res["state_trace"]), 4)

    def test_scenario_without_asset_fails(self):
        # A scenario without an asset fails
        scenario = dict(FICTIONAL_SCENARIOS[0])
        scenario["asset"] = ""
        res = check_security_rubric_with_state_trace(scenario)
        self.assertEqual(res["status"], "failed")
        self.assertFalse(res["passed"])
        self.assertIn("asset", res["reason"])
        self.assertTrue(res["invariant_holds"])

    def test_missing_asset_key_fails(self):
        scenario = dict(FICTIONAL_SCENARIOS[0])
        del scenario["asset"]
        res = check_security_rubric_with_state_trace(scenario)
        self.assertEqual(res["status"], "failed")
        self.assertFalse(res["passed"])

    def test_unrelated_control_flagged_for_review(self):
        # A control unrelated to named threat is flagged for review
        scenario = dict(FICTIONAL_SCENARIOS[0])
        scenario["control"] = "Paint the server chassis yellow and change room lightbulbs."
        res = check_security_rubric_with_state_trace(scenario)
        self.assertEqual(res["status"], "flagged_for_review")
        self.assertFalse(res["passed"])
        self.assertTrue(res["review_flagged"])
        self.assertTrue(res["invariant_holds"])

    def test_all_predefined_scenarios_pass(self):
        for s in FICTIONAL_SCENARIOS:
            res = check_security_rubric_with_state_trace(s)
            self.assertEqual(res["status"], "passed")
            self.assertTrue(res["invariant_holds"])

    def test_state_trace_recorded(self):
        res = check_security_rubric_with_state_trace(FICTIONAL_SCENARIOS[1])
        steps = [s["step"] for s in res["state_trace"]]
        self.assertEqual(steps, [1, 2, 3, 4])

    def test_mock_limitations_documented(self):
        self.assertGreaterEqual(len(MOCK_LIMITATIONS), 3)

    @unittest.skip("Deliberate failure test: demonstrates framework exits non-zero on failure")
    def test_deliberate_wrong_result(self):
        res = check_security_rubric_with_state_trace(FICTIONAL_SCENARIOS[0])
        self.assertEqual(res["status"], "unexpected_status")


if __name__ == "__main__":
    unittest.main()
