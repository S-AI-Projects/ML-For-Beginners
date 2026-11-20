import unittest
from pathlib import Path

from example import evaluate, load_fixtures


FIXTURES = Path(__file__).with_name("fixtures.json")


class ScenarioRubricTests(unittest.TestCase):
    def setUp(self):
        self.scenarios = load_fixtures(FIXTURES)

    def test_complete_scenario_passes(self):
        self.assertEqual(evaluate(self.scenarios[0])["status"], "PASS")

    def test_missing_asset_fails(self):
        result = evaluate(self.scenarios[1])
        self.assertEqual(result["status"], "FAIL")
        self.assertIn("asset", result["reason"])

    def test_unrelated_control_is_flagged_for_review(self):
        result = evaluate(self.scenarios[2])
        self.assertEqual(result["status"], "REVIEW")

    def test_other_required_fields_are_checked(self):
        for field in ("threat", "control", "residual_risk"):
            with self.subTest(field=field):
                scenario = dict(self.scenarios[0], **{field: "  "})
                self.assertEqual(evaluate(scenario)["status"], "FAIL")


if __name__ == "__main__":
    unittest.main()
