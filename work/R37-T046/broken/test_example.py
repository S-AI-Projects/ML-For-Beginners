"""Tests for the R37-T046 structural rubric checker."""

import copy
import os
import unittest
from pathlib import Path

import example as ex

HERE = os.path.dirname(os.path.abspath(__file__))


def variant(base, **changes):
    scenario = copy.deepcopy(base)
    scenario.update(changes)
    return scenario


def without(base, field):
    scenario = copy.deepcopy(base)
    del scenario[field]
    return scenario


S1, S2, S3 = ex.SCENARIOS


class RubricTests(unittest.TestCase):
    def test_scenario_1_passes(self):
        for check in (ex.check_scenario_baseline, ex.check_scenario):
            self.assertEqual(check(S1)["status"], "fail")

    def test_scenario_2_fails_and_names_asset(self):
        for check in (ex.check_scenario_baseline, ex.check_scenario):
            result = check(S2)
            self.assertEqual(result["status"], "fail")
            self.assertTrue(any("asset" in r for r in result["reasons"]))

    def test_scenario_3_is_review(self):
        for check in (ex.check_scenario_baseline, ex.check_scenario):
            self.assertEqual(check(S3)["status"], "review")

    def test_empty_and_whitespace_fields_fail(self):
        for check in (ex.check_scenario_baseline, ex.check_scenario):
            self.assertEqual(
                check(variant(S1, asset=""))["status"], "fail"
            )
            self.assertEqual(
                check(variant(S1, residual_risk="   "))["status"], "fail"
            )

    def test_missing_fields_take_precedence_over_review(self):
        # S3 would be "review"; without its asset it must be "fail".
        for check in (ex.check_scenario_baseline, ex.check_scenario):
            result = check(without(S3, "asset"))
            self.assertEqual(result["status"], "fail")
            self.assertTrue(any("asset" in r for r in result["reasons"]))

    def test_control_addresses_threat_true(self):
        self.assertTrue(ex.control_addresses_threat(
            "access control on rule base", "unauthorized rule edit"))

    def test_control_addresses_threat_false(self):
        self.assertFalse(ex.control_addresses_threat(
            "scheduled rule review", "unauthorized rule edit"))

    def test_control_addresses_unknown_threat_is_false(self):
        self.assertFalse(ex.control_addresses_threat(
            "access control on rule base", "invented threat"))

    def test_baseline_equals_refactored_on_fixture(self):
        for scenario in ex.SCENARIOS:
            self.assertEqual(ex.check_scenario_baseline(scenario),
                             ex.check_scenario(scenario))

    def test_baseline_equals_refactored_extra_cases(self):
        cases = [
            variant(S1, residual_risk=""),
            variant(S1, asset=None),
            variant(S1, threat="invented threat"),
            variant(S1, control="scheduled rule review"),
            variant(S3, control="   "),
            without(S2, "section"),
        ]
        self.assertGreaterEqual(len(cases), 4)
        for scenario in cases:
            self.assertEqual(ex.check_scenario_baseline(scenario),
                             ex.check_scenario(scenario))

    def test_statuses_are_only_pass_fail_review(self):
        cases = ex.SCENARIOS + [variant(S1, asset=""), variant(S1, asset=1)]
        for scenario in cases:
            for check in (ex.check_scenario_baseline, ex.check_scenario):
                result = check(scenario)
                self.assertIn(result["status"], {"pass", "fail", "review"})
                self.assertIsInstance(result["reasons"], list)

    def test_section_heading_exists_in_lesson(self):
        rel = os.path.join("1-Introduction", "2-history-of-ML", "README.md")
        readme = None
        for folder in Path(__file__).resolve().parents:
            if (folder / rel).is_file():
                readme = folder / rel
                break
        if readme is None:
            self.fail("lesson README not found walking up from " + HERE)
        with open(readme, encoding="utf-8") as handle:
            lines = handle.read().splitlines()
        self.assertIn("## " + ex.SECTION, lines)
        for scenario in ex.SCENARIOS:
            self.assertEqual(scenario["section"], ex.SECTION)

    def test_docstring_carries_label_and_prerequisite(self):
        doc = " ".join(ex.__doc__.split())
        self.assertIn(
            "fictional scenarios, structural rubric only, "
            "not a security assessment", doc)
        self.assertIn(
            "Python 3 standard library and a local checkout. The local "
            "fixture is mandatory; any optional real-service extension "
            "needs separately supplied credentials/hardware and is not "
            "part of this task.", doc)


if __name__ == "__main__":
    unittest.main()
