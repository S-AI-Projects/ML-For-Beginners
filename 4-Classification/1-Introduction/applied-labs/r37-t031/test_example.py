import unittest

from example import confusion_matrix, evaluate


class TestEvaluation(unittest.TestCase):
    def test_normal_case(self):
        r = evaluate([1, 1, 0, 0], [1, 0, 1, 0])
        self.assertEqual((r["TP"], r["FN"], r["FP"], r["TN"]), (1, 1, 1, 1))
        self.assertEqual(r["precision"], 0.5)
        self.assertEqual(r["recall"], 0.5)

    def test_no_positive_predictions_gives_zero_precision(self):
        r = evaluate([1, 1, 0, 0], [0, 0, 0, 0])
        self.assertEqual(r["precision"], 0.0)
        self.assertEqual(r["recall"], 0.0)

    def test_no_actual_positives_gives_zero_recall(self):
        r = evaluate([0, 0, 0], [1, 0, 0])
        self.assertEqual(r["recall"], 0.0)

    def test_perfect_classifier(self):
        r = evaluate([1, 0, 1, 0], [1, 0, 1, 0])
        self.assertEqual((r["precision"], r["recall"]), (1.0, 1.0))

    def test_length_mismatch_raises(self):
        with self.assertRaises(ValueError):
            confusion_matrix([1, 0], [1])

    def test_empty_raises(self):
        with self.assertRaises(ValueError):
            confusion_matrix([], [])

    def test_invalid_label_raises(self):
        with self.assertRaises(ValueError):
            confusion_matrix([1, 2], [1, 0])

    def test_argument_order_matters(self):
        a = confusion_matrix([1, 1, 1, 0], [1, 0, 0, 0])
        b = confusion_matrix([1, 0, 0, 0], [1, 1, 1, 0])
        self.assertEqual((a["FN"], a["FP"]), (2, 0))
        self.assertEqual((b["FN"], b["FP"]), (0, 2))


if __name__ == "__main__":
    unittest.main()