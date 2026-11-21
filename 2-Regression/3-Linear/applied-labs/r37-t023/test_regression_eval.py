"""
Unit tests for r37-t023: regression evaluation – invariant and state trace.

Run with:
    python3 -m unittest discover -s 2-Regression/3-Linear/applied-labs/r37-t023 -p "test_*.py" -v
"""

import math
import unittest

from example import evaluate_regression


class TestRegressionEvaluationNormalFixture(unittest.TestCase):
    """
    Contract requirement:
    truth=[1,2,3], prediction=[1,3,2] gives MAE=2/3 and RMSE=sqrt(2/3).
    """

    def setUp(self):
        self.truth = [1, 2, 3]
        self.prediction = [1, 3, 2]
        self.result = evaluate_regression(self.truth, self.prediction)

    def test_mae_exact_fraction(self):
        expected_mae = 2.0 / 3.0
        self.assertAlmostEqual(self.result["metrics"]["mae"], expected_mae, places=7)

    def test_rmse_exact_sqrt(self):
        expected_rmse = math.sqrt(2.0 / 3.0)
        self.assertAlmostEqual(self.result["metrics"]["rmse"], expected_rmse, places=7)

    def test_intermediate_residuals(self):
        expected_residuals = [0, 1, -1]
        self.assertEqual(self.result["trace"]["residuals"], expected_residuals)

    def test_intermediate_absolute_errors(self):
        expected_abs = [0, 1, 1]
        self.assertEqual(self.result["trace"]["absolute_errors"], expected_abs)
        self.assertEqual(self.result["trace"]["sum_absolute_errors"], 2)

    def test_intermediate_squared_errors(self):
        expected_sq = [0, 1, 1]
        self.assertEqual(self.result["trace"]["squared_errors"], expected_sq)
        self.assertEqual(self.result["trace"]["sum_squared_errors"], 2)

    def test_state_invariants(self):
        invs = self.result["invariants"]
        self.assertTrue(invs["non_negative"])
        self.assertTrue(invs["mae_le_rmse"])
        self.assertTrue(invs["sum_abs_reconciled"])
        self.assertTrue(invs["sum_sq_reconciled"])


class TestRegressionIdenticalArrays(unittest.TestCase):
    """
    Contract requirement: identical arrays give both errors 0.
    """

    def test_identical_integer_arrays(self):
        arr = [4, 5, 6, 7]
        result = evaluate_regression(arr, arr)
        self.assertEqual(result["metrics"]["mae"], 0.0)
        self.assertEqual(result["metrics"]["rmse"], 0.0)
        self.assertEqual(result["trace"]["sum_absolute_errors"], 0.0)
        self.assertEqual(result["trace"]["sum_squared_errors"], 0.0)

    def test_identical_float_arrays(self):
        arr = [1.25, 3.5, 7.75]
        result = evaluate_regression(arr, arr)
        self.assertEqual(result["metrics"]["mae"], 0.0)
        self.assertEqual(result["metrics"]["rmse"], 0.0)


class TestInputValidationAndBoundary(unittest.TestCase):
    """
    Rejection of mismatched lengths and empty inputs.
    """

    def test_mismatched_lengths_raises_value_error(self):
        with self.assertRaises(ValueError) as ctx:
            evaluate_regression([1, 2, 3], [1, 2])
        self.assertIn("Mismatched lengths", str(ctx.exception))

    def test_empty_truth_raises_value_error(self):
        with self.assertRaises(ValueError) as ctx:
            evaluate_regression([], [1, 2])
        self.assertIn("empty", str(ctx.exception))

    def test_empty_prediction_raises_value_error(self):
        with self.assertRaises(ValueError) as ctx:
            evaluate_regression([1, 2], [])
        self.assertIn("empty", str(ctx.exception))

    def test_both_empty_raises_value_error(self):
        with self.assertRaises(ValueError) as ctx:
            evaluate_regression([], [])
        self.assertIn("empty", str(ctx.exception))

    def test_single_element_array(self):
        result = evaluate_regression([5.0], [8.0])
        self.assertAlmostEqual(result["metrics"]["mae"], 3.0)
        self.assertAlmostEqual(result["metrics"]["rmse"], 3.0)
        self.assertEqual(result["trace"]["residuals"], [3.0])


class TestDeliberateFailure(unittest.TestCase):
    """
    Framework check: deliberate wrong expected result causes test to fail,
    demonstrating the framework exits non-zero on failure.
    """

    @unittest.skip("Deliberate failure demo: remove skip to verify non-zero exit")
    def test_deliberate_wrong_mae_DEMO_FAIL(self):
        result = evaluate_regression([1, 2, 3], [1, 3, 2])
        # Intentional error: 0.999 instead of 2/3 (0.6666...)
        self.assertEqual(result["metrics"]["mae"], 0.999, "DEMO: intentional failure")


if __name__ == "__main__":
    unittest.main()
