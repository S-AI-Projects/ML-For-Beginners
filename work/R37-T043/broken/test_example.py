"""Regression tests for the bounded memory fixture in example.py."""

import unittest

from example import BoundedMemory


class TestBoundedMemory(unittest.TestCase):

    def test_worked_example_add_a_to_d_then_mutate_copy(self):
        memory = BoundedMemory()
        for record in ["A", "B", "C", "D"]:
            memory.add(record)
        self.assertEqual(memory.records(), ["A", "B", "C"])
        returned = memory.records()
        returned.append("X")
        returned.remove("B")
        returned.clear()
        self.assertEqual(memory.records(), ["B", "C", "D"])

    def test_empty_memory_returns_empty_list(self):
        self.assertEqual(BoundedMemory().records(), [])

    def test_one_to_three_records_retained_in_order(self):
        memory = BoundedMemory()
        memory.add("A")
        self.assertEqual(memory.records(), ["A"])
        memory.add("B")
        self.assertEqual(memory.records(), ["A", "B"])
        memory.add("C")
        self.assertEqual(memory.records(), ["A", "B", "C"])

    def test_exactly_three_records_evicts_nothing(self):
        memory = BoundedMemory()
        for record in ["A", "B", "C"]:
            memory.add(record)
        self.assertEqual(memory.records(), ["A", "B", "C"])

    def test_fourth_record_evicts_only_the_oldest(self):
        memory = BoundedMemory()
        for record in ["A", "B", "C"]:
            memory.add(record)
        memory.add("D")
        self.assertEqual(memory.records(), ["B", "C", "D"])

    def test_longer_stream_keeps_last_three(self):
        memory = BoundedMemory()
        for record in ["A", "B", "C", "D", "E", "F", "G"]:
            memory.add(record)
        self.assertEqual(memory.records(), ["E", "F", "G"])

    def test_mutating_returned_list_does_not_alter_memory(self):
        memory = BoundedMemory()
        for record in ["A", "B", "C", "D"]:
            memory.add(record)

        appended = memory.records()
        appended.append("Z")
        self.assertEqual(memory.records(), ["B", "C", "D"])

        removed = memory.records()
        removed.remove("C")
        self.assertEqual(memory.records(), ["B", "C", "D"])

        cleared = memory.records()
        cleared.clear()
        self.assertEqual(memory.records(), ["B", "C", "D"])

    def test_two_calls_return_independent_copies(self):
        memory = BoundedMemory()
        memory.add("A")
        first = memory.records()
        second = memory.records()
        self.assertIsNot(first, second)
        first.append("X")
        self.assertEqual(second, ["A"])
        self.assertEqual(memory.records(), ["A"])

    def test_arrival_order_is_preserved(self):
        memory = BoundedMemory()
        for record in ["C", "A", "B"]:
            memory.add(record)
        self.assertEqual(memory.records(), ["C", "A", "B"])


if __name__ == "__main__":
    unittest.main()
