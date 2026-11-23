"""Unit tests for classification evaluation failure and recovery (R37-T058)."""

import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(__file__))
from example import (
    BinaryEvaluationSession,
    run_failure_and_recovery_demonstration,
    MOCK_LIMITATIONS,
)


class TestClassificationFailureAndRecovery(unittest.TestCase):
    def setUp(self):
        self.session = BinaryEvaluationSession(zero_division=0.0)

    def test_standard_fixture_accuracy_and_confusion_matrix(self):
        # y_true=[1,1,0,0], y_pred=[1,0,1,0] gives TP=1,FN=1,FP=1,TN=1, precision=recall=0.5
        res = self.session.evaluate([1, 1, 0, 0], [1, 0, 1, 0])
        self.assertEqual(res["status"], "success")
        self.assertIsNone(res["error"])

        cm = res["metrics"]["confusion_matrix"]
        self.assertEqual(cm["tp"], 1)
        self.assertEqual(cm["fn"], 1)
        self.assertEqual(cm["fp"], 1)
        self.assertEqual(cm["tn"], 1)
        self.assertEqual(res["metrics"]["precision"], 0.5)
        self.assertEqual(res["metrics"]["recall"], 0.5)
        self.assertEqual(res["metrics"]["accuracy"], 0.5)

    def test_no_positive_predictions_gives_precision_zero(self):
        # No positive predictions gives precision=0 under the documented policy
        res = self.session.evaluate([1, 1, 0, 0], [0, 0, 0, 0])
        self.assertEqual(res["status"], "success")
        self.assertEqual(res["metrics"]["precision"], 0.0)
        self.assertEqual(res["metrics"]["recall"], 0.0)
        self.assertEqual(res["metrics"]["confusion_matrix"]["tp"], 0)
        self.assertEqual(res["metrics"]["confusion_matrix"]["fp"], 0)

    def test_failure_on_length_mismatch(self):
        # Failure case with clear diagnostic explanation
        res = self.session.evaluate([1, 1, 0, 0], [1, 0])
        self.assertEqual(res["status"], "error")
        self.assertIsNotNone(res["error"])
        self.assertEqual(res["error"]["error_type"], "LengthMismatchError")
        self.assertIn("length mismatch", res["error"]["message"].lower())
        self.assertIn("same number of observations", res["error"]["recovery_guidance"].lower())

    def test_failure_on_invalid_label(self):
        res = self.session.evaluate([1, 2], [1, 0])
        self.assertEqual(res["status"], "error")
        self.assertEqual(res["error"]["error_type"], "InvalidLabelError")

    def test_seamless_recovery_after_failure(self):
        # 1. Trigger failure
        res_fail = self.session.evaluate([1, 0], [1])
        self.assertEqual(res_fail["status"], "error")
        self.assertIsNotNone(self.session.last_error)

        # 2. Immediate recovery on next valid input
        res_recover = self.session.evaluate([1, 1, 0, 0], [1, 0, 1, 0])
        self.assertEqual(res_recover["status"], "success")
        self.assertIsNone(self.session.last_error)
        self.assertEqual(res_recover["metrics"]["precision"], 0.5)

    def test_demo_pipeline_demonstrates_recovery(self):
        demo = run_failure_and_recovery_demonstration()
        self.assertTrue(demo["recovered_successfully"])
        self.assertEqual(demo["step_2_failure"]["status"], "error")
        self.assertEqual(demo["step_3_recovery"]["status"], "success")

    def test_mock_limitations_documented(self):
        self.assertGreaterEqual(len(MOCK_LIMITATIONS), 3)

    @unittest.skip("Deliberate failure test: demonstrates framework exits non-zero on failure")
    def test_deliberate_wrong_result(self):
        res = self.session.evaluate([1, 1, 0, 0], [1, 0, 1, 0])
        self.assertEqual(res["metrics"]["precision"], 0.999)


if __name__ == "__main__":
    unittest.main()
