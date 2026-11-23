"""Unit tests for chronological evaluation split comparison (R37-T053)."""

import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(__file__))
from example import (
    chronological_split_direct,
    chronological_split_independent_calc,
    compare_split_approaches,
    validate_and_sort_observations,
    make_ten_sample_observations,
    MOCK_LIMITATIONS,
)


class TestChronologicalSplit(unittest.TestCase):
    def test_ten_ordered_observations_yield_six_two_two(self):
        # Ten ordered observations yield 6 train, 2 validation, 2 test
        obs = make_ten_sample_observations()
        res = chronological_split_direct(obs)

        self.assertEqual(len(res["train"]), 6)
        self.assertEqual(len(res["val"]), 2)
        self.assertEqual(len(res["test"]), 2)

        # Verify exact timestamps
        self.assertEqual([x["timestamp"] for x in res["train"]], [1, 2, 3, 4, 5, 6])
        self.assertEqual([x["timestamp"] for x in res["val"]], [7, 8])
        self.assertEqual([x["timestamp"] for x in res["test"]], [9, 10])

    def test_shuffled_input_is_sorted_first(self):
        # Shuffled inputs must be sorted prior to partition
        shuffled = [
            {"timestamp": 5, "v": "e"},
            {"timestamp": 1, "v": "a"},
            {"timestamp": 10, "v": "j"},
            {"timestamp": 3, "v": "c"},
            {"timestamp": 2, "v": "b"},
            {"timestamp": 8, "v": "h"},
            {"timestamp": 4, "v": "d"},
            {"timestamp": 6, "v": "f"},
            {"timestamp": 7, "v": "g"},
            {"timestamp": 9, "v": "i"},
        ]
        res = chronological_split_direct(shuffled)
        self.assertEqual([x["timestamp"] for x in res["train"]], [1, 2, 3, 4, 5, 6])
        self.assertEqual([x["timestamp"] for x in res["val"]], [7, 8])
        self.assertEqual([x["timestamp"] for x in res["test"]], [9, 10])

    def test_duplicate_timestamps_rejected(self):
        # Duplicate timestamps are rejected
        dup_input = [
            {"timestamp": 1, "v": 10},
            {"timestamp": 2, "v": 20},
            {"timestamp": 2, "v": 25},  # duplicate
            {"timestamp": 3, "v": 30},
        ]
        with self.assertRaises(ValueError) as ctx:
            chronological_split_direct(dup_input)
        self.assertIn("duplicate timestamp", str(ctx.exception).lower())

    def test_compare_two_approaches_identical_results(self):
        obs = make_ten_sample_observations()
        comp = compare_split_approaches(obs)
        self.assertTrue(comp["approaches_agree"])
        self.assertEqual(comp["approach_a_direct"]["train_len"], 6)
        self.assertEqual(comp["approach_b_independent"]["train_len"], 6)

    def test_empty_observations(self):
        res = chronological_split_direct([])
        self.assertEqual(res["train"], [])
        self.assertEqual(res["val"], [])
        self.assertEqual(res["test"], [])

    def test_future_leakage_prevented(self):
        # Max timestamp in train must be strictly less than min timestamp in val
        # Max timestamp in val must be strictly less than min timestamp in test
        obs = make_ten_sample_observations()
        res = chronological_split_direct(obs)
        max_train = max(x["timestamp"] for x in res["train"])
        min_val = min(x["timestamp"] for x in res["val"])
        max_val = max(x["timestamp"] for x in res["val"])
        min_test = min(x["timestamp"] for x in res["test"])

        self.assertLess(max_train, min_val)
        self.assertLess(max_val, min_test)

    def test_mock_limitations_documented(self):
        self.assertGreaterEqual(len(MOCK_LIMITATIONS), 3)

    @unittest.skip("Deliberate failure test: demonstrates framework exits non-zero on failure")
    def test_deliberate_wrong_result(self):
        obs = make_ten_sample_observations()
        res = chronological_split_direct(obs)
        self.assertEqual(len(res["train"]), 99)


if __name__ == "__main__":
    unittest.main()
