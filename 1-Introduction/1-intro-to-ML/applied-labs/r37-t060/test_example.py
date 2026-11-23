"""
Unit tests for R37-T060: Security-Scenario Rubric Checker
"""

import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(__file__))

from example import SecurityRubricChecker, FICTIONAL_SCENARIOS


class TestSecurityRubricChecker(unittest.TestCase):

    def test_complete_scenario_passes(self):
        """A complete scenario with aligned asset, threat, and control passes."""
        scenario = FICTIONAL_SCENARIOS["complete_valid_scenario"]
        result = SecurityRubricChecker.evaluate(scenario)
        self.assertEqual(result["status"], "pass")
        self.assertTrue(result["details"]["asset_defined"])
        self.assertTrue(result["details"]["control_aligned"])

    def test_missing_asset_fails(self):
        """A scenario without an asset fails the structural rubric."""
        scenario = FICTIONAL_SCENARIOS["missing_asset_scenario"]
        result = SecurityRubricChecker.evaluate(scenario)
        self.assertEqual(result["status"], "fail")
        self.assertIn("asset", result["reason"])

    def test_unrelated_control_flagged_for_review(self):
        """A control unrelated to the named threat is flagged for review."""
        scenario = FICTIONAL_SCENARIOS["unrelated_control_scenario"]
        result = SecurityRubricChecker.evaluate(scenario)
        self.assertEqual(result["status"], "flagged_for_review")
        self.assertIn("unrelated", result["reason"])

    def test_missing_residual_risk_fails(self):
        """A scenario missing residual_risk fails."""
        scenario = {
            "asset": "Credit Scoring Model Weights",
            "threat": "Model extraction attacks",
            "control": "Query rate limiting and differential privacy noise",
            # "residual_risk" omitted
        }
        result = SecurityRubricChecker.evaluate(scenario)
        self.assertEqual(result["status"], "fail")
        self.assertIn("residual_risk", result["reason"])

    def test_batch_evaluation(self):
        """Batch evaluation processes all three scenarios with expected statuses."""
        results = SecurityRubricChecker.evaluate_all(FICTIONAL_SCENARIOS)
        self.assertEqual(results["complete_valid_scenario"]["status"], "pass")
        self.assertEqual(results["missing_asset_scenario"]["status"], "fail")
        self.assertEqual(results["unrelated_control_scenario"]["status"], "flagged_for_review")

    def test_deliberate_failure_detection(self):
        """Demonstrates that asserting wrong outcome fails the test suite."""
        result = SecurityRubricChecker.evaluate(FICTIONAL_SCENARIOS["complete_valid_scenario"])
        with self.assertRaises(AssertionError):
            self.assertEqual(result["status"], "fail", "Valid scenario must not be marked fail")


if __name__ == "__main__":
    unittest.main()
