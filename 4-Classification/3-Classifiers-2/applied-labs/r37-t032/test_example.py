import unittest

from example import confusion_matrix, precision_recall


class TestConfusionMatrix(unittest.TestCase):
    def test_smallest_valid_case(self):
        self.assertEqual(confusion_matrix([1, 1, 0, 0], [1, 0, 1, 0]), (2, 0, 0, 2))
        self.assertEqual(precision_recall([1, 1, 0, 0], [1, 0, 1, 0]), (0.5, 0.5))

    def test_single_sample(self):
        self.assertEqual(confusion_matrix([1], [1]), (1, 0, 0, 0))

    def test_boundary_no_positive_predictions(self):
        # TP + FP == 0 -> precision defined as 0.0 by policy
        p, r = precision_recall([1, 1, 0, 0], [0, 0, 0, 0])
        self.assertEqual(p, 0.0)
        self.assertEqual(r, 0.0)

    def test_boundary_no_actual_positives(self):
        # TP + FN == 0 -> recall defined as 0.0 by policy
        p, r = precision_recall([0, 0], [1, 0])
        self.assertEqual(r, 0.0)
        self.assertEqual(p, 0.0)

    def test_argument_order_matters(self):
        # swapping (y_true, y_pred) swaps FN and FP
        self.assertEqual(confusion_matrix([1, 1, 1], [1, 0, 0]), (1, 2, 0, 0))
        self.assertEqual(confusion_matrix([1, 0, 0], [1, 1, 1]), (1, 0, 2, 0))

    def test_invalid_length_mismatch(self):
        with self.assertRaises(ValueError):
            confusion_matrix([1, 0], [1])

    def test_invalid_empty(self):
        with self.assertRaises(ValueError):
            confusion_matrix([], [])

    def test_invalid_label_value(self):
        with self.assertRaises(ValueError):
            confusion_matrix([1, 2], [1, 0])
        with self.assertRaises(ValueError):
            confusion_matrix([1, 0], [True, 0])

    def test_deliberate_wrong_result_is_detected(self):
        # Proves the check can fail: a wrong expectation must NOT equal the result.
        self.assertNotEqual(confusion_matrix([1, 1, 0, 0], [1, 0, 1, 0]), (2, 0, 0, 2))


if __name__ == "__main__":
    unittest.main()
