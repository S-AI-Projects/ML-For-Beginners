"""
Unit tests for r37-t021: classification evaluation boundary-case extension.

Run with:
    python3 -m unittest discover -s 4-Classification/4-Applied/applied-labs/r37-t021 -p "test_*.py"

The test suite covers:
  1. Normal case  – balanced 2×2 fixture with precision = recall = 0.5
  2. Boundary case – no positive predictions → precision = 0.0
  3. Failure demonstration – a deliberately wrong expected value that
     causes the test to fail (shows the suite exits non-zero on failure)
  4. Invalid input – length mismatch raises ValueError
"""

import sys
import unittest

from example import (
    confusion_matrix_binary,
    precision_binary,
    recall_binary,
)


class TestNormalCase(unittest.TestCase):
    """
    Smallest valid fixture:
      y_true=[1,1,0,0], y_pred=[1,0,1,0]
      → TP=1, FN=1, FP=1, TN=1, precision=0.5, recall=0.5
    """

    def setUp(self):
        self.y_true = [1, 1, 0, 0]
        self.y_pred = [1, 0, 1, 0]
        self.TP, self.FN, self.FP, self.TN = confusion_matrix_binary(
            self.y_true, self.y_pred
        )

    def test_tp(self):
        self.assertEqual(self.TP, 1)

    def test_fn(self):
        self.assertEqual(self.FN, 1)

    def test_fp(self):
        self.assertEqual(self.FP, 1)

    def test_tn(self):
        self.assertEqual(self.TN, 1)

    def test_precision_is_half(self):
        prec = precision_binary(self.TP, self.FP)
        self.assertAlmostEqual(prec, 0.5)

    def test_recall_is_half(self):
        rec = recall_binary(self.TP, self.FN)
        self.assertAlmostEqual(rec, 0.5)


class TestBoundaryNoPredictedPositives(unittest.TestCase):
    """
    Boundary case: classifier predicts all zeros.
      y_true=[1,0], y_pred=[0,0]
      → TP=0, FP=0, precision=0.0 (zero-denominator policy)
    """

    def setUp(self):
        self.y_true = [1, 0]
        self.y_pred = [0, 0]
        self.TP, self.FN, self.FP, self.TN = confusion_matrix_binary(
            self.y_true, self.y_pred
        )

    def test_no_tp(self):
        self.assertEqual(self.TP, 0)

    def test_no_fp(self):
        self.assertEqual(self.FP, 0)

    def test_precision_zero_denominator_policy(self):
        """precision must return 0.0 — not raise — when TP+FP==0."""
        prec = precision_binary(self.TP, self.FP)
        self.assertEqual(prec, 0.0)

    def test_recall_nonzero_because_fn_exists(self):
        """recall = TP/(TP+FN) = 0/(0+1) = 0.0"""
        rec = recall_binary(self.TP, self.FN)
        self.assertEqual(rec, 0.0)


class TestBoundaryAllPredictedPositive(unittest.TestCase):
    """
    Boundary case: classifier predicts all ones.
      y_true=[1,0], y_pred=[1,1]
      → TP=1, FP=1, TN=0, FN=0
      → precision=0.5, recall=1.0
    """

    def setUp(self):
        self.TP, self.FN, self.FP, self.TN = confusion_matrix_binary(
            [1, 0], [1, 1]
        )

    def test_values(self):
        self.assertEqual((self.TP, self.FN, self.FP, self.TN), (1, 0, 1, 0))

    def test_precision(self):
        self.assertAlmostEqual(precision_binary(self.TP, self.FP), 0.5)

    def test_recall(self):
        self.assertAlmostEqual(recall_binary(self.TP, self.FN), 1.0)


class TestInvalidInput(unittest.TestCase):
    """Invalid inputs must raise ValueError, not silently produce wrong numbers."""

    def test_length_mismatch_raises(self):
        with self.assertRaises(ValueError):
            confusion_matrix_binary([1, 0], [1])

    def test_empty_lists_give_all_zeros(self):
        TP, FN, FP, TN = confusion_matrix_binary([], [])
        self.assertEqual((TP, FN, FP, TN), (0, 0, 0, 0))


class TestDeliberateFailure(unittest.TestCase):
    """
    This test is intentionally designed to FAIL when run in isolation to
    demonstrate that the test framework exits non-zero on assertion failure.

    To verify framework behaviour, run:
        python3 -m unittest \
            4-Classification/4-Applied/applied-labs/r37-t021/test_classification_eval.py \
            TestDeliberateFailure.test_wrong_precision_expectation_DEMO_FAIL

    Expected output: FAIL (1 test)  exit code 1
    """

    @unittest.skip(
        "Deliberate-failure demo: remove the @skip decorator to confirm "
        "the suite exits non-zero when an assertion fails."
    )
    def test_wrong_precision_expectation_DEMO_FAIL(self):
        """
        Uses the normal fixture but asserts precision == 0.9 (wrong).
        Without @skip this WILL fail — proving the suite catches mistakes.
        """
        y_true = [1, 1, 0, 0]
        y_pred = [1, 0, 1, 0]
        TP, FN, FP, TN = confusion_matrix_binary(y_true, y_pred)
        prec = precision_binary(TP, FP)
        # Deliberately wrong expected value: 0.9 ≠ 0.5
        self.assertAlmostEqual(
            prec,
            0.9,
            msg=(
                "DEMO: This failure is intentional. "
                "Precision should be 0.5, not 0.9."
            ),
        )


if __name__ == "__main__":
    unittest.main()
