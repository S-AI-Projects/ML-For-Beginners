"""Unit tests and worked-example regression checks in example.py."""

import unittest
import math

import example


class RegressionWorkedExampleTests(unittest.TestCase):

    def test_worked_example_regression_check(self):
        truth = [1, 2, 3]
        prediction = [1, 3, 2]
        mae = example.calculate_mae(truth, prediction)
        rmse = example.calculate_rmse(truth, prediction)
        # Exact values: MAE = 2/3, RMSE = sqrt(2/3)
        self.assertAlmostEqual(mae, 4.0 / 3.0)
        self.assertAlmostEqual(rmse, math.sqrt(2.0 / 3.0))

    def test_worked_table_row_details(self):
        truth = [1, 2, 3]
        prediction = [1, 3, 2]
        rows = example.generate_worked_table(truth, prediction)
        self.assertEqual(len(rows), 3)

        # Row 0: truth=1, pred=1 -> error=0, abs=0, sq=0
        self.assertEqual((rows[0]["error"], rows[0]["abs_error"], rows[0]["sq_error"]), (0, 0, 0))
        # Row 1: truth=2, pred=3 -> error=-1, abs=1, sq=1
        self.assertEqual((rows[1]["error"], rows[1]["abs_error"], rows[1]["sq_error"]), (-1, 1, 1))
        # Row 2: truth=3, pred=2 -> error=1, abs=1, sq=1
        self.assertEqual((rows[2]["error"], rows[2]["abs_error"], rows[2]["sq_error"]), (1, 1, 1))

    def test_identical_arrays_give_zero_errors(self):
        arr = [1, 2, 3]
        self.assertEqual(example.calculate_mae(arr, arr), 0.0)
        self.assertEqual(example.calculate_rmse(arr, arr), 0.0)

    def test_single_element_array(self):
        self.assertEqual(example.calculate_mae([5], [2]), 3.0)
        self.assertEqual(example.calculate_rmse([5], [2]), 3.0)

    def test_uniform_offset_errors(self):
        truth = [10, 20, 30]
        pred = [12, 22, 32]
        self.assertEqual(example.calculate_mae(truth, pred), 2.0)
        self.assertEqual(example.calculate_rmse(truth, pred), 2.0)

    def test_float_values(self):
        truth = [1.5, 2.5]
        pred = [2.0, 2.0]
        self.assertAlmostEqual(example.calculate_mae(truth, pred), 0.5)
        self.assertAlmostEqual(example.calculate_rmse(truth, pred), 0.5)

    def test_mismatched_lengths_raises(self):
        with self.assertRaises(ValueError):
            example.calculate_mae([1, 2], [1, 2, 3])

    def test_empty_truth_raises(self):
        with self.assertRaises(ValueError):
            example.calculate_mae([], [])

    def test_non_numeric_elements_raises(self):
        with self.assertRaises(TypeError):
            example.calculate_mae([1, "two"], [1, 2])
        with self.assertRaises(TypeError):
            example.calculate_mae([True, False], [1, 0])

    def test_invalid_container_type_raises(self):
        with self.assertRaises(TypeError):
            example.calculate_mae(123, [1, 2])


if __name__ == "__main__":
    unittest.main()
