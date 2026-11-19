"""Unit tests for offline regression service adapter in example.py."""

import unittest
import math

import example


class RegressionAdapterTests(unittest.TestCase):

    def test_headline_mae_and_rmse(self):
        truth = [1, 2, 3]
        prediction = [1, 3, 2]
        res = example.evaluate(truth, prediction)
        self.assertAlmostEqual(res["mae"], 2.0 / 3.0)
        self.assertAlmostEqual(res["rmse"], math.sqrt(2.0 / 3.0))

    def test_identical_arrays_zero_errors(self):
        truth = [1, 2, 3]
        prediction = [1, 2, 3]
        res = example.evaluate(truth, prediction)
        self.assertEqual(res["mae"], 0.0)
        self.assertEqual(res["rmse"], 0.0)

    def test_adapter_callable_interface(self):
        adapter = example.LocalRegressionEvaluatorAdapter()
        self.assertTrue(callable(adapter))
        res = adapter([1, 2], [2, 3])
        self.assertEqual(res["mae"], 1.0)
        self.assertEqual(res["rmse"], 1.0)

    def test_client_with_injected_adapter(self):
        adapter = example.LocalRegressionEvaluatorAdapter()
        client = example.RegressionEvaluationClient(service_adapter=adapter)
        res = client.evaluate([1, 2, 3], [1, 3, 2])
        self.assertAlmostEqual(res["mae"], 2.0 / 3.0)

    def test_mismatched_lengths_raises(self):
        with self.assertRaises(ValueError):
            example.evaluate([1, 2], [1, 2, 3])

    def test_empty_input_raises(self):
        with self.assertRaises(ValueError):
            example.evaluate([], [])

    def test_non_numeric_elements_raises(self):
        with self.assertRaises(TypeError):
            example.evaluate([1, "two"], [1, 2])
        with self.assertRaises(TypeError):
            example.evaluate([True, False], [1, 0])

    def test_single_element_evaluation(self):
        res = example.evaluate([10], [6])
        self.assertEqual(res["mae"], 4.0)
        self.assertEqual(res["rmse"], 4.0)

    def test_floating_point_numbers(self):
        truth = [1.5, 2.5]
        pred = [1.0, 3.0]
        res = example.evaluate(truth, pred)
        self.assertAlmostEqual(res["mae"], 0.5)
        self.assertAlmostEqual(res["rmse"], 0.5)

    def test_large_uniform_offset(self):
        truth = [10, 20, 30]
        pred = [12, 22, 32]
        res = example.evaluate(truth, pred)
        self.assertEqual(res["mae"], 2.0)
        self.assertEqual(res["rmse"], 2.0)


if __name__ == "__main__":
    unittest.main()
