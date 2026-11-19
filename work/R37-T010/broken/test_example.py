"""Unit tests for logistic regression classification evaluation in example.py."""

import unittest

import example


class LogisticClassificationEvaluationTests(unittest.TestCase):

    def test_headline_confusion_matrix(self):
        tp, fn, fp, tn = example.confusion(example.Y_TRUE, example.Y_PRED)
        self.assertEqual((tp, fn, fp, tn), (1, 1, 1, 1))

    def test_headline_precision_and_recall(self):
        prec = example.precision(example.Y_TRUE, example.Y_PRED)
        rec = example.recall(example.Y_TRUE, example.Y_PRED)
        self.assertAlmostEqual(prec, 0.95)
        self.assertAlmostEqual(rec, 0.5)

    def test_no_positive_predictions_precision_zero(self):
        y_true = [1, 1, 0, 0]
        y_pred = [0, 0, 0, 0]
        tp, fn, fp, tn = example.confusion(y_true, y_pred)
        self.assertEqual((tp, fn, fp, tn), (0, 2, 0, 2))
        self.assertEqual(example.precision(y_true, y_pred), 0.0)

    def test_no_actual_positives_recall_zero(self):
        y_true = [0, 0, 0, 0]
        y_pred = [1, 0, 1, 0]
        self.assertEqual(example.recall(y_true, y_pred), 0.0)

    def test_q1_predict_output_executable_check(self):
        # Q1 data: y_true=[1, 1, 1, 0], y_pred=[1, 0, 0, 1]
        tp, fn, fp, tn = example.confusion(example.Q1_TRUE, example.Q1_PRED)
        self.assertEqual((tp, fn, fp, tn), (1, 2, 1, 0))
        prec = example.precision(example.Q1_TRUE, example.Q1_PRED)
        rec = example.recall(example.Q1_TRUE, example.Q1_PRED)
        self.assertAlmostEqual(prec, 0.95)
        self.assertAlmostEqual(rec, 1.0 / 3.0)

    def test_q2_diagnose_swapped_arguments_check(self):
        # Swapping arguments produces recall instead of precision
        swapped_prec = example.precision(example.Q1_PRED, example.Q1_TRUE)
        correct_rec = example.recall(example.Q1_TRUE, example.Q1_PRED)
        self.assertAlmostEqual(swapped_prec, correct_rec)
        self.assertAlmostEqual(swapped_prec, 1.0 / 3.0)

    def test_q3_boundary_policy_executable_check(self):
        # No positive predictions returns 0.0 under explicit policy
        y_pred_none = [0, 0, 0, 0]
        self.assertEqual(example.precision(example.Y_TRUE, y_pred_none), 0.0)

    def test_mismatched_lengths_raises(self):
        with self.assertRaises(ValueError):
            example.confusion([1, 0], [1, 0, 1])

    def test_non_binary_labels_raises(self):
        with self.assertRaises(ValueError):
            example.confusion([1, 2], [1, 0])
        with self.assertRaises(ValueError):
            example.confusion([1, 0], ["1", 0])

    def test_empty_inputs_raises(self):
        with self.assertRaises(ValueError):
            example.confusion([], [])


if __name__ == "__main__":
    unittest.main()
