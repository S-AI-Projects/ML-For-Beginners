"""Unit tests for security scenario rubric checker in example.py."""

import unittest

import example


class SecurityScenarioRubricTests(unittest.TestCase):

    def test_complete_scenario_passes(self):
        res = example.check_scenario(example.SCENARIOS["scenario_1_pass"])
        self.assertEqual(res["status"], "pass")
        self.assertIn("meets all structural rubric", res["reason"])

    def test_scenario_without_asset_fails(self):
        res = example.check_scenario(example.SCENARIOS["scenario_2_fail"])
        self.assertEqual(res["status"], "fail")
        self.assertIn("asset", res["reason"])

    def test_unrelated_control_flagged_for_review(self):
        res = example.check_scenario(example.SCENARIOS["scenario_3_review"])
        self.assertEqual(res["status"], "review")
        self.assertIn("unrelated", res["reason"])

    def test_missing_threat_fails(self):
        s = {
            "asset": "Historical ML dataset",
            "control": "Encryption",
            "residual_risk": "Key loss"
        }
        res = example.check_scenario(s)
        self.assertEqual(res["status"], "fail")
        self.assertIn("threat", res["reason"])

    def test_missing_control_fails(self):
        s = {
            "asset": "Historical ML dataset",
            "threat": "unauthorized modification",
            "residual_risk": "Key loss"
        }
        res = example.check_scenario(s)
        self.assertEqual(res["status"], "fail")
        self.assertIn("control", res["reason"])

    def test_missing_residual_risk_fails(self):
        s = {
            "asset": "Historical ML dataset",
            "threat": "unauthorized modification",
            "control": "Encryption"
        }
        res = example.check_scenario(s)
        self.assertEqual(res["status"], "fail")
        self.assertIn("residual_risk", res["reason"])

    def test_whitespace_only_field_fails(self):
        s = {
            "asset": "   ",
            "threat": "threat",
            "control": "control",
            "residual_risk": "risk"
        }
        res = example.check_scenario(s)
        self.assertEqual(res["status"], "fail")
        self.assertIn("asset", res["reason"])

    def test_invalid_type_raises(self):
        with self.assertRaises(TypeError):
            example.check_scenario(["not", "a", "dict"])

    def test_experiment_runs_three_configurations(self):
        metrics = example.run_experiment()
        self.assertIn("config_1_single", metrics)
        self.assertIn("config_2_standard_three", metrics)
        self.assertIn("config_3_extended_five", metrics)
        self.assertEqual(metrics["config_1_single"]["total"], 1)
        self.assertEqual(metrics["config_2_standard_three"]["total"], 3)
        self.assertEqual(metrics["config_3_extended_five"]["total"], 5)

    def test_experiment_metrics_and_tradeoff(self):
        metrics = example.run_experiment()
        # In config 2: 1 pass, 1 fail, 1 review -> review rate = 1/3
        c2 = metrics["config_2_standard_three"]
        self.assertEqual(c2["counts"], {"pass": 1, "fail": 1, "review": 1})
        self.assertAlmostEqual(c2["review_rate"], 1.0 / 3.0)
        self.assertAlmostEqual(c2["automated_rate"], 2.0 / 3.0)


if __name__ == "__main__":
    unittest.main()
