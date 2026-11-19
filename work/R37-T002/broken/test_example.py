"""Unit tests for lexical retrieval in example.py."""

import unittest

import example


class LexicalRetrieverTests(unittest.TestCase):

    def test_query_red_apple_ranks_a_before_b(self):
        results = example.retrieve("red apple")
        self.assertEqual(results, [("B", 2), ("A", 1)])
        # Check source attribution IDs
        doc_ids = [doc_id for doc_id, _ in results]
        self.assertEqual(doc_ids, ["A", "B"])

    def test_query_ocean_returns_no_match(self):
        results = example.retrieve("ocean")
        self.assertEqual(results, [])

    def test_smallest_valid_single_word_match(self):
        results = example.retrieve("sky")
        self.assertEqual(results, [("C", 1)])

    def test_tie_breaking_by_doc_id(self):
        # "apple" appears in A and B with score 1; tie broken by doc ID ascending
        results = example.retrieve("apple")
        self.assertEqual(results, [("A", 1), ("B", 1)])

    def test_case_insensitivity_boundary(self):
        results = example.retrieve("RED APPLE")
        self.assertEqual(results, [("B", 2), ("A", 1)])

    def test_repeated_query_words_set_boundary(self):
        # Word set ensures duplicates don't artificially increase score
        results = example.retrieve("apple apple apple")
        self.assertEqual(results, [("A", 1), ("B", 1)])

    def test_punctuation_and_whitespace_boundary(self):
        results = example.retrieve("  red!  apple?  ")
        self.assertEqual(results, [("B", 2), ("A", 1)])

    def test_empty_query_raises_value_error(self):
        with self.assertRaises(ValueError):
            example.retrieve("")
        with self.assertRaises(ValueError):
            example.retrieve("   ")

    def test_non_string_query_raises_type_error(self):
        with self.assertRaises(TypeError):
            example.retrieve(123)
        with self.assertRaises(TypeError):
            example.retrieve(None)

    def test_custom_corpus_retrieval(self):
        custom = {"Z": "yellow banana", "Y": "green banana"}
        results = example.retrieve("banana", documents=custom)
        # Tie break 'Y' before 'Z'
        self.assertEqual(results, [("Y", 1), ("Z", 1)])


if __name__ == "__main__":
    unittest.main()
