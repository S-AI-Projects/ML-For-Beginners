"""Tests for the chronological split. Run from the lab directory."""

import unittest

from example import chronological_split


def ordered(count):
    return [(t, t * 1.5) for t in range(1, count + 1)]


class ChronologicalSplitTests(unittest.TestCase):

    def test_ten_ordered_observations_split_six_two_two(self):
        train, validation, test = chronological_split(ordered(10))
        self.assertEqual([t for t, _ in train], [1, 2, 3, 4, 5, 6])
        self.assertEqual([t for t, _ in validation], [7, 8])
        self.assertEqual([t for t, _ in test], [9, 10])

    def test_shuffled_input_gives_identical_split(self):
        shuffled = [ordered(10)[i] for i in (6, 0, 9, 3, 1, 8, 4, 2, 7, 5)]
        self.assertEqual(
            chronological_split(shuffled),
            chronological_split(ordered(10)),
        )

    def test_caller_list_is_not_mutated(self):
        shuffled = [ordered(10)[i] for i in (6, 0, 9, 3, 1, 8, 4, 2, 7, 5)]
        before = list(shuffled)
        chronological_split(shuffled)
        self.assertEqual(shuffled, before)

    def test_no_future_leakage(self):
        train, validation, test = chronological_split(ordered(20))
        self.assertLess(max(t for t, _ in train),
                        min(t for t, _ in validation))
        self.assertLess(max(t for t, _ in validation),
                        min(t for t, _ in test))

    def test_duplicate_timestamp_is_named(self):
        batch = ordered(10) + [(4, 9.0)]
        with self.assertRaisesRegex(ValueError, "duplicate timestamp 4"):
            chronological_split(batch)

    def test_missing_value_is_named(self):
        batch = [(t, None if t == 4 else t * 1.5) for t in range(1, 11)]
        with self.assertRaisesRegex(ValueError,
                                    "missing value at timestamp 4"):
            chronological_split(batch)

    def test_fewer_than_five_observations_rejected(self):
        with self.assertRaisesRegex(ValueError, "at least 5"):
            chronological_split(ordered(4))

    def test_exactly_five_gives_three_one_one(self):
        train, validation, test = chronological_split(ordered(5))
        self.assertEqual(len(train), 3)
        self.assertEqual(len(validation), 1)
        self.assertEqual(len(test), 1)

    def test_twenty_gives_twelve_four_four(self):
        train, validation, test = chronological_split(ordered(20))
        self.assertEqual(len(train), 12)
        self.assertEqual(len(validation), 4)
        self.assertEqual(len(test), 4)

    def test_recovery_after_invalid_batch(self):
        broken = [(t, None if t == 4 else t * 1.5) for t in range(1, 11)]
        with self.assertRaises(ValueError):
            chronological_split(broken)
        next_batch = [(t, t * 1.5) for t in range(11, 21)]
        train, validation, test = chronological_split(next_batch)
        self.assertEqual([t for t, _ in train], list(range(11, 17)))
        self.assertEqual([t for t, _ in validation], [17, 18])
        self.assertEqual([t for t, _ in test], [19, 20])


if __name__ == "__main__":
    unittest.main()
