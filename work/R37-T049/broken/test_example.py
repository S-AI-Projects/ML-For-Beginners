"""Unit tests for example.py (fixed toy labels, stdlib only)."""

import unittest

import example


class ConfusionMetricsTest(unittest.TestCase):

    def test_headline_counts_and_metrics(self):
        y_true, y_pred = [1, 1, 0, 0], [1, 0, 1, 0]
        self.assertEqual(example.confusion(y_true, y_pred), (1, 1, 1, 1))
        self.assertAlmostEqual(example.precision(y_true, y_pred), 0.75)
        self.assertAlmostEqual(example.recall(y_true, y_pred), 0.5)

    def test_no_positive_predictions_precision_is_zero(self):
        self.assertAlmostEqual(
            example.precision([1, 1, 0, 0], [0, 0, 0, 0]), 0.0)

    def test_no_actual_positives_recall_is_zero(self):
        self.assertAlmostEqual(
            example.recall([0, 0, 0, 0], [1, 0, 1, 0]), 0.0)

    def test_length_mismatch_raises(self):
        with self.assertRaises(ValueError):
            example.confusion([1, 0], [1])

    def test_non_binary_label_raises(self):
        with self.assertRaises(ValueError):
            example.confusion([1, 2], [1, 0])
        with self.assertRaises(ValueError):
            example.precision([1, 0], [True, 0])


class AppliedQuestionsTest(unittest.TestCase):

    def test_q1_predict_output(self):
        y_true, y_pred = [1, 1, 1, 0], [1, 0, 0, 1]
        self.assertEqual(example.confusion(y_true, y_pred), (1, 2, 1, 0))
        self.assertAlmostEqual(example.precision(y_true, y_pred), 0.5)
        self.assertAlmostEqual(example.recall(y_true, y_pred), 1 / 3)

    def test_q2_swapped_arguments(self):
        y_true, y_pred = [1, 1, 1, 0], [1, 0, 0, 1]
        swapped = example.precision(y_pred, y_true)
        self.assertAlmostEqual(swapped, 1 / 3)
        self.assertAlmostEqual(swapped, example.recall(y_true, y_pred))
        self.assertNotAlmostEqual(
            swapped, example.precision(y_true, y_pred))

    def test_q3_no_positive_predictions(self):
        result = example.precision([1, 1, 0, 0], [0, 0, 0, 0])
        self.assertAlmostEqual(result, 0.0)


if __name__ == "__main__":
    unittest.main()
