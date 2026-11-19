"""Unit tests for classification evaluation in example.py."""

import unittest

import example


class ClassificationEvaluationTests(unittest.TestCase):

    def test_headline_confusion_matrix(self):
        y_true = [1, 1, 0, 0]
        y_pred = [1, 0, 1, 0]
        tp, fn, fp, tn = example.confusion(y_true, y_pred)
        self.assertEqual((tp, fn, fp, tn), (1, 1, 1, 1))

    def test_headline_precision_and_recall(self):
        y_true = [1, 1, 0, 0]
        y_pred = [1, 0, 1, 0]
        self.assertAlmostEqual(example.precision(y_true, y_pred), 0.5)
        self.assertAlmostEqual(example.recall(y_true, y_pred), 0.5)

    def test_no_positive_predictions_precision_zero(self):
        y_true = [1, 1, 0, 0]
        y_pred = [0, 0, 0, 0]
        tp, fn, fp, tn = example.confusion(y_true, y_pred)
        self.assertEqual((tp, fn, fp, tn), (0, 2, 0, 2))
        self.assertEqual(example.precision(y_true, y_pred), 0.0)
        self.assertAlmostEqual(example.recall(y_true, y_pred), 0.0)

    def test_no_actual_positives_recall_zero(self):
        y_true = [0, 0, 0, 0]
        y_pred = [1, 0, 1, 0]
        self.assertEqual(example.recall(y_true, y_pred), 0.0)
        self.assertAlmostEqual(example.precision(y_true, y_pred), 0.0)

    def test_perfect_classification(self):
        y_true = [1, 0, 1, 0]
        y_pred = [1, 0, 1, 0]
        tp, fn, fp, tn = example.confusion(y_true, y_pred)
        self.assertEqual((tp, fn, fp, tn), (2, 0, 0, 2))
        self.assertEqual(example.precision(y_true, y_pred), 1.0)
        self.assertEqual(example.recall(y_true, y_pred), 1.0)

    def test_completely_wrong_classification(self):
        y_true = [1, 1, 0, 0]
        y_pred = [0, 0, 1, 1]
        tp, fn, fp, tn = example.confusion(y_true, y_pred)
        self.assertEqual((tp, fn, fp, tn), (0, 2, 2, 0))
        self.assertEqual(example.precision(y_true, y_pred), 0.0)
        self.assertEqual(example.recall(y_true, y_pred), 0.0)

    def test_mismatched_lengths_raises(self):
        with self.assertRaises(ValueError):
            example.confusion([1, 0], [1, 0, 1])

    def test_non_binary_label_raises(self):
        with self.assertRaises(ValueError):
            example.confusion([1, 2], [1, 0])
        with self.assertRaises(ValueError):
            example.confusion([1, 0], ["1", 0])

    def test_empty_input_raises(self):
        with self.assertRaises(ValueError):
            example.confusion([], [])

    def test_invalid_types_raise(self):
        with self.assertRaises(TypeError):
            example.confusion(123, [1, 0])


if __name__ == "__main__":
    unittest.main()
