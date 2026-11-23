"""Unit tests for refactored classification evaluation (R37-T056)."""

import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(__file__))
from example import (
    BinaryMetricsCalculator,
    MetricsPresenter,
    evaluate_binary_classification,
    MOCK_LIMITATIONS,
)


class TestClassificationEvaluationRefactored(unittest.TestCase):
    def setUp(self):
        self.calc = BinaryMetricsCalculator(zero_division=0.0)

    def test_standard_fixture(self):
        # y_true=[1,1,0,0], y_pred=[1,0,1,0] gives TP=1,FN=1,FP=1,TN=1, precision=recall=0.5
        y_true = [1, 1, 0, 0]
        y_pred = [1, 0, 1, 0]
        res = self.calc.evaluate(y_true, y_pred)
        cm = res["confusion_matrix"]

        self.assertEqual(cm["tp"], 1)
        self.assertEqual(cm["fn"], 1)
        self.assertEqual(cm["fp"], 1)
        self.assertEqual(cm["tn"], 1)
        self.assertEqual(res["precision"], 0.5)
        self.assertEqual(res["recall"], 0.5)
        self.assertEqual(res["accuracy"], 0.5)

    def test_no_positive_predictions_gives_precision_zero(self):
        # No positive predictions gives precision=0 under the documented policy
        y_true = [1, 1, 0, 0]
        y_pred = [0, 0, 0, 0]
        res = self.calc.evaluate(y_true, y_pred)
        cm = res["confusion_matrix"]

        self.assertEqual(cm["tp"], 0)
        self.assertEqual(cm["fp"], 0)
        self.assertEqual(cm["fn"], 2)
        self.assertEqual(cm["tn"], 2)
        self.assertEqual(res["precision"], 0.0)
        self.assertEqual(res["recall"], 0.0)

    def test_all_positive_predictions(self):
        y_true = [1, 0]
        y_pred = [1, 1]
        res = self.calc.evaluate(y_true, y_pred)
        self.assertEqual(res["confusion_matrix"]["tp"], 1)
        self.assertEqual(res["confusion_matrix"]["fp"], 1)
        self.assertEqual(res["precision"], 0.5)
        self.assertEqual(res["recall"], 1.0)

    def test_length_mismatch_raises_value_error(self):
        with self.assertRaises(ValueError) as ctx:
            self.calc.evaluate([1, 0], [1])
        self.assertIn("length mismatch", str(ctx.exception).lower())

    def test_invalid_label_value_raises_value_error(self):
        with self.assertRaises(ValueError) as ctx:
            self.calc.evaluate([1, 2], [1, 0])
        self.assertIn("binary labels must be 0 or 1", str(ctx.exception).lower())

    def test_presentation_layer_formatting(self):
        res = self.calc.evaluate([1, 1, 0, 0], [1, 0, 1, 0])
        formatted = MetricsPresenter.format_summary(res)
        self.assertIn("TP=1, FN=1, FP=1, TN=1", formatted)
        self.assertIn("Precision=0.500", formatted)

    def test_mock_limitations_documented(self):
        self.assertGreaterEqual(len(MOCK_LIMITATIONS), 3)

    @unittest.skip("Deliberate failure test: demonstrates framework exits non-zero on failure")
    def test_deliberate_wrong_result(self):
        res = self.calc.evaluate([1, 1, 0, 0], [1, 0, 1, 0])
        self.assertEqual(res["precision"], 0.999)


if __name__ == "__main__":
    unittest.main()
