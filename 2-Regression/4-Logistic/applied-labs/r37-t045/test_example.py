"""Tests for the offline confusion-matrix lab (example.py)."""

import unittest

from example import ZERO_DENOMINATOR_VALUE, evaluate, mock_adapter

INPUTS = ["a", "b", "c", "d"]


class RecordingAdapter:
    """Wrap a predict callable and record every input it receives."""

    def __init__(self, predict):
        self.predict = predict
        self.calls = []

    def __call__(self, x):
        self.calls.append(x)
        return self.predict(x)


class EvaluateTests(unittest.TestCase):

    def test_headline_contract(self):
        r = evaluate([1, 1, 0, 0], INPUTS, mock_adapter)
        self.assertEqual(r["y_pred"], [1, 0, 1, 0])
        self.assertEqual(
            (r["tp"], r["fn"], r["fp"], r["tn"]), (1, 1, 1, 1))
        self.assertEqual(r["precision"], 0.5)
        self.assertEqual(r["recall"], 0.5)

    def test_no_positive_predictions_gives_precision_zero(self):
        r = evaluate([1, 1, 0, 0], INPUTS, lambda x: 0)
        self.assertEqual(r["tp"] + r["fp"], 0)
        self.assertEqual(r["precision"], ZERO_DENOMINATOR_VALUE)
        self.assertEqual(r["precision"], 0.0)

    def test_no_actual_positives_gives_recall_zero(self):
        r = evaluate([0, 0, 0, 0], INPUTS, lambda x: 1)
        self.assertEqual(r["tp"] + r["fn"], 0)
        self.assertEqual(r["recall"], ZERO_DENOMINATOR_VALUE)
        self.assertEqual(r["recall"], 0.0)

    def test_empty_input_gives_zero_counts_and_scores(self):
        r = evaluate([], [], mock_adapter)
        self.assertEqual(
            (r["tp"], r["fn"], r["fp"], r["tn"]), (0, 0, 0, 0))
        self.assertEqual(r["precision"], 0.0)
        self.assertEqual(r["recall"], 0.0)

    def test_all_correct(self):
        r = evaluate([1, 0], ["a", "b"], mock_adapter)
        self.assertEqual(
            (r["tp"], r["fn"], r["fp"], r["tn"]), (1, 0, 0, 1))
        self.assertEqual(r["precision"], 1.0)
        self.assertEqual(r["recall"], 1.0)

    def test_all_wrong(self):
        r = evaluate([1, 0], ["b", "a"], mock_adapter)
        self.assertEqual(
            (r["tp"], r["fn"], r["fp"], r["tn"]), (0, 1, 1, 0))
        self.assertEqual(r["precision"], 0.0)
        self.assertEqual(r["recall"], 0.0)

    def test_length_mismatch_raises(self):
        with self.assertRaises(ValueError):
            evaluate([1, 0, 1], INPUTS, mock_adapter)

    def test_non_binary_label_raises(self):
        with self.assertRaises(ValueError):
            evaluate([1, 2, 0, 0], INPUTS, mock_adapter)

    def test_adapter_called_once_per_input_in_order(self):
        adapter = RecordingAdapter(mock_adapter)
        evaluate([1, 1, 0, 0], INPUTS, adapter)
        self.assertEqual(adapter.calls, INPUTS)

    def test_adapter_exception_is_not_swallowed(self):
        def broken(x):
            raise RuntimeError("adapter failed")

        with self.assertRaises(RuntimeError):
            evaluate([1], ["a"], broken)

    def test_adapter_non_binary_output_raises(self):
        with self.assertRaises(ValueError):
            evaluate([1], ["a"], lambda x: 2)

    def test_works_with_a_different_callable(self):
        # Proves the interface, not the lookup-table adapter, is used.
        r = evaluate([1, 0, 1], ["x", "y", "z"], lambda x: 1)
        self.assertEqual(r["y_pred"], [1, 1, 1])
        self.assertEqual((r["tp"], r["fp"]), (2, 1))
        self.assertEqual(r["precision"], 2 / 3)
        self.assertEqual(r["recall"], 1.0)

    def test_asymmetric_counts(self):
        # Distinguishes FP from FN and TP from TN, unlike the headline.
        preds = {"a": 1, "b": 0, "c": 0, "d": 1}
        r = evaluate([1, 1, 1, 0], INPUTS, lambda x: preds[x])
        self.assertEqual(r["y_pred"], [1, 0, 0, 1])
        self.assertEqual(
            (r["tp"], r["fn"], r["fp"], r["tn"]), (1, 2, 1, 0))
        self.assertAlmostEqual(r["precision"], 0.5)
        self.assertAlmostEqual(r["recall"], 1 / 3)


if __name__ == "__main__":
    unittest.main()
