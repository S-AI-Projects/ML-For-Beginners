"""
Unit tests for r37-t024: retrieval with source attribution — refactor teaching example.

Run with:
    python3 -m unittest discover -s 7-TimeSeries/3-SVR/applied-labs/r37-t024 -p "test_*.py" -v
"""

import unittest

from example import (
    DOCUMENTS,
    retrieve_baseline,
    retrieve_refactored,
    score_overlap,
)


class TestRetrievalContract(unittest.TestCase):
    """
    Contract requirements:
    - query "red apple" ranks A before B
    - query "ocean" returns no match (empty list)
    - Returns document IDs with results
    """

    def test_query_red_apple_ranks_a_before_b(self):
        results = retrieve_refactored("red apple")
        # Expected: A score 2, B score 1. C has 0 so excluded.
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0], ("A", 2))
        self.assertEqual(results[1], ("B", 1))

    def test_query_ocean_returns_empty_list(self):
        results = retrieve_refactored("ocean")
        self.assertEqual(results, [])

    def test_source_attribution_doc_ids_returned(self):
        results = retrieve_refactored("sky")
        self.assertEqual(results, [("C", 1)])


class TestTieBreaking(unittest.TestCase):
    """
    Breaking ties by document ID ascending.
    """

    def test_tie_breaking_by_doc_id(self):
        # query "apple" matches A and B with score 1 each
        results = retrieve_refactored("apple")
        self.assertEqual(len(results), 2)
        # Should be ordered A, then B because 'A' < 'B'
        self.assertEqual(results, [("A", 1), ("B", 1)])


class TestBeforeAfterEquivalence(unittest.TestCase):
    """
    Prove before (baseline) and after (refactored) equivalence on all fixtures.
    """

    def test_equivalence_red_apple(self):
        q = "red apple"
        self.assertEqual(retrieve_baseline(q), retrieve_refactored(q))

    def test_equivalence_ocean(self):
        q = "ocean"
        self.assertEqual(retrieve_baseline(q), retrieve_refactored(q))

    def test_equivalence_tie_case(self):
        q = "apple"
        self.assertEqual(retrieve_baseline(q), retrieve_refactored(q))

    def test_equivalence_custom_corpus(self):
        corpus = {"X": "quick brown fox", "Y": "lazy dog", "Z": "brown dog"}
        q = "brown dog"
        self.assertEqual(retrieve_baseline(q, corpus), retrieve_refactored(q, corpus))


class TestExtractedResponsibility(unittest.TestCase):
    """
    Unit test specifically for the extracted responsibility: score_overlap.
    """

    def test_score_overlap_exact_match(self):
        self.assertEqual(score_overlap({"apple", "red"}, {"apple", "red"}), 2)

    def test_score_overlap_partial_match(self):
        self.assertEqual(score_overlap({"red", "apple"}, {"green", "apple"}), 1)

    def test_score_overlap_no_match(self):
        self.assertEqual(score_overlap({"ocean"}, {"blue", "sky"}), 0)


class TestDeliberateFailure(unittest.TestCase):
    """
    Framework check: deliberate wrong expected result causes test to fail,
    demonstrating the framework exits non-zero on failure.
    """

    @unittest.skip("Deliberate failure demo: remove skip to verify non-zero exit")
    def test_deliberate_wrong_ranking_DEMO_FAIL(self):
        results = retrieve_refactored("red apple")
        # Intentionally wrong expected order (B before A)
        self.assertEqual(results[0][0], "B", "DEMO: intentional failure")


if __name__ == "__main__":
    unittest.main()
