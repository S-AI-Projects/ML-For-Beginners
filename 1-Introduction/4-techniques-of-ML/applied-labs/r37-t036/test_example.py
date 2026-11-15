import copy
import unittest

from example import (
    SCENARIOS,
    check_scenario,
    check_scenario_baseline,
    find_structural_problems,
)


class TestRubric(unittest.TestCase):
    def test_complete_scenario_passes(self):
        r = check_scenario(SCENARIOS["complete"])
        self.assertEqual(r, {"status": "pass", "problems": [], "flags": []})

    def test_scenario_without_asset_fails(self):
        r = check_scenario(SCENARIOS["no_asset"])
        self.assertEqual(r["status"], "fail")
        self.assertIn("missing asset", r["problems"])

    def test_unrelated_control_is_flagged_for_review(self):
        r = check_scenario(SCENARIOS["unrelated_control"])
        self.assertEqual(r["status"], "review")
        self.assertEqual(r["problems"], [])
        self.assertEqual(len(r["flags"]), 1)

    def test_whitespace_only_field_counts_as_missing(self):
        s = copy.deepcopy(SCENARIOS["complete"])
        s["asset"] = "   "
        self.assertEqual(check_scenario(s)["status"], "fail")

    def test_invalid_risk_level_fails(self):
        s = copy.deepcopy(SCENARIOS["complete"])
        s["residual_risk"]["level"] = "severe"
        self.assertIn("invalid residual_risk.level", check_scenario(s)["problems"])

    def test_missing_whole_sections_fail(self):
        for key in ("threat", "control", "residual_risk"):
            s = copy.deepcopy(SCENARIOS["complete"])
            del s[key]
            r = check_scenario(s)
            self.assertEqual(r["status"], "fail")
            self.assertIn(f"missing {key}", r["problems"])

    def test_problem_beats_flag(self):
        s = copy.deepcopy(SCENARIOS["unrelated_control"])
        s["asset"] = ""
        r = check_scenario(s)
        self.assertEqual(r["status"], "fail")
        self.assertEqual(len(r["flags"]), 1)

    def test_non_dict_rejected(self):
        for bad in (None, "text", [1, 2], 5):
            with self.assertRaises(ValueError):
                check_scenario(bad)
            with self.assertRaises(ValueError):
                check_scenario_baseline(bad)

    def test_fixture_has_three_scenarios(self):
        self.assertEqual(len(SCENARIOS), 3)


class TestBeforeAfterEquivalence(unittest.TestCase):
    """The refactor keeps the same contract: identical output on identical input."""

    def test_equivalent_on_fixture(self):
        for name, s in SCENARIOS.items():
            self.assertEqual(check_scenario(s), check_scenario_baseline(s), name)

    def test_equivalent_when_each_field_is_removed_or_blanked(self):
        paths = [
            ("lesson_section",), ("asset",), ("threat",), ("control",), ("residual_risk",),
            ("threat", "id"), ("threat", "description"),
            ("control", "description"), ("control", "mitigates"),
            ("residual_risk", "level"), ("residual_risk", "note"),
        ]
        for base in SCENARIOS.values():
            for path in paths:
                for mode in ("delete", "blank"):
                    s = copy.deepcopy(base)
                    parent = s
                    for k in path[:-1]:
                        parent = parent[k]
                    if mode == "delete":
                        del parent[path[-1]]
                    else:
                        parent[path[-1]] = ""
                    self.assertEqual(
                        check_scenario(s), check_scenario_baseline(s), (path, mode)
                    )

    def test_equivalent_when_control_target_changes(self):
        for target in ("T1", "T2", "T3", "X", ""):
            s = copy.deepcopy(SCENARIOS["complete"])
            s["control"]["mitigates"] = target
            self.assertEqual(check_scenario(s), check_scenario_baseline(s), target)

    def test_extracted_function_is_what_produces_problems(self):
        for s in SCENARIOS.values():
            self.assertEqual(check_scenario(s)["problems"], find_structural_problems(s))

    def test_deliberate_wrong_result_is_detected(self):
        self.assertNotEqual(check_scenario(SCENARIOS["no_asset"])["status"], "pass")
        self.assertNotEqual(check_scenario(SCENARIOS["unrelated_control"])["status"], "pass")


if __name__ == "__main__":
    unittest.main()
