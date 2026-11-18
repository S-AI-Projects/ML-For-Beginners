"""Tests for the MAE/RMSE toy comparison in example.py.

Scope: controlled toy configurations, not a measure of real-world model
accuracy.

Prerequisites: Python 3 standard library and a local checkout. The local
fixture is mandatory; any optional real-service extension needs separately
supplied credentials/hardware and is not part of this task.
"""
import math
import unittest

from example import CONFIGS, TRUTH, compare, mae, rmse

EXPECTED = {
    "A": (1.0, 1.0),
    "B": (1.0, 2.0),
    "C": (0.5, 0.5),
}


class HeadlineTests(unittest.TestCase):
    def test_headline_mae_and_rmse(self):
        self.assertAlmostEqual(mae([1, 2, 3], [1, 3, 2]), 2 / 3)
        self.assertAlmostEqual(rmse([1, 2, 3], [1, 3, 2]),
                               math.sqrt(2 / 3))

    def test_identical_lists_give_zero(self):
        self.assertAlmostEqual(mae([1, 2, 3], [1, 2, 3]), 0.0)
        self.assertAlmostEqual(rmse([1, 2, 3], [1, 2, 3]), 0.0)

    def test_single_element_pair(self):
        self.assertAlmostEqual(mae([5], [3]), 2.0)
        self.assertAlmostEqual(rmse([5], [3]), 2.0)

    def test_negative_and_float_values(self):
        truth = [-1.5, 2.0]
        prediction = [1.0, -1.0]
        self.assertAlmostEqual(mae(truth, prediction), 2.75)
        self.assertAlmostEqual(rmse(truth, prediction),
                               math.sqrt(7.625))


class InputValidationTests(unittest.TestCase):
    def test_mismatched_lengths_raise(self):
        with self.assertRaises(ValueError):
            mae([1, 2, 3], [1, 2])
        with self.assertRaises(ValueError):
            rmse([1, 2, 3], [1, 2])

    def test_both_empty_raise(self):
        with self.assertRaises(ValueError):
            mae([], [])
        with self.assertRaises(ValueError):
            rmse([], [])

    def test_one_empty_raises(self):
        with self.assertRaises(ValueError):
            mae([], [1])
        with self.assertRaises(ValueError):
            rmse([1], [])


class ConfigurationTests(unittest.TestCase):
    def test_truth_is_fixed_list(self):
        self.assertEqual(TRUTH, [1, 2, 3, 4])

    def test_each_config_matches_expected(self):
        rows = {key: (m, r) for key, _, m, r in compare()}
        self.assertEqual(sorted(rows), sorted(EXPECTED))
        for key, (exp_mae, exp_rmse) in EXPECTED.items():
            with self.subTest(config=key):
                self.assertAlmostEqual(rows[key][0], exp_mae)
                self.assertAlmostEqual(rows[key][1], exp_rmse)

    def test_configs_are_defined_in_order(self):
        self.assertEqual([key for key, _, _ in CONFIGS], ["A", "B", "C"])

    def test_tradeoff_same_mae_larger_rmse_for_outlier(self):
        rows = {key: (m, r) for key, _, m, r in compare()}
        self.assertAlmostEqual(rows["A"][0], rows["B"][0])
        self.assertGreater(rows["B"][1], rows["A"][1])

    def test_rmse_at_least_mae_with_equality_for_a_and_c(self):
        rows = {key: (m, r) for key, _, m, r in compare()}
        for key, (m, r) in rows.items():
            with self.subTest(config=key):
                self.assertGreaterEqual(r + 1e-12, m)
        for key in ("A", "C"):
            with self.subTest(config=key):
                self.assertAlmostEqual(rows[key][0], rows[key][1])
        self.assertGreater(rows["B"][1], rows["B"][0])


if __name__ == "__main__":
    unittest.main()
