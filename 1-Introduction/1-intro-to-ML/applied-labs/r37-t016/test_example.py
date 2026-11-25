"""Tests for the local scenario rubric checker."""

import unittest

import example


# Frozen, deliberately small baseline from before extracting check_fields.
def baseline_evaluate_scenario(scenario):
    errors = []
    for field in example.REQUIRED_FIELDS:
        value = scenario.get(field)
        if not isinstance(value, str) or not value.strip():
            errors.append(f"missing or empty {field}")
    if errors:
        return {"id": str(scenario.get("id", "unknown")), "status": "fail", "detail": "; ".join(errors)}
    threat = scenario["threat"].strip().lower()
    control = scenario["control"].strip().lower()
    expected = example.CONTROL_THREATS.get(control)
    if expected is None or threat not in expected:
        return {"id": str(scenario.get("id", "unknown")), "status": "review", "detail": "control is not linked to the named threat in this local rubric"}
    return {"id": str(scenario.get("id", "unknown")), "status": "pass", "detail": "complete; stated control matches threat"}


class ScenarioCheckerTests(unittest.TestCase):
    def test_fixture_outcomes(self):
        results = example.evaluate(example.load_fixture())
        self.assertEqual(["pass", "fail", "review"], [row["status"] for row in results])
        self.assertIn("asset", results[1]["detail"])
        self.assertIn("control", results[2]["detail"])

    def test_extracted_responsibility_preserves_baseline_on_fixture(self):
        fixture = example.load_fixture()
        self.assertEqual([baseline_evaluate_scenario(item) for item in fixture], example.evaluate(fixture))

    def test_rationale_is_left_to_human_review(self):
        scenario = example.load_fixture()[0]
        original = example.evaluate_scenario(scenario)
        scenario["control_rationale"] = "Changed explanation for human review."
        self.assertEqual(original, example.evaluate_scenario(scenario))

    def test_boundary_values_are_incomplete(self):
        for value in (None, "", "   ", 0):
            with self.subTest(value=value):
                row = {"asset": value, "threat": "unauthorized record access", "control": "restrict record access", "residual_risk": "some risk"}
                self.assertEqual("fail", example.evaluate_scenario(row)["status"])

    def test_wrong_result_is_caught(self):
        expected = "pass"
        deliberately_wrong_actual = "fail"
        with self.assertRaises(AssertionError):
            self.assertEqual(expected, deliberately_wrong_actual)


if __name__ == "__main__":
    unittest.main()
