"""
Unit tests for r37-t030: retrieval with source attribution — scenario assessment.

Run with:
    python3 -m unittest discover -s 7-TimeSeries/3-SVR/applied-labs/r37-t030 -p "test_*.py" -v
"""

import unittest

from example import (
    DOCUMENTS,
    SCENARIO_ASSESSMENT,
    check_question_1_prediction,
    check_question_2_diagnosis,
    check_question_3_boundary_policy,
    retrieve,
    tokenize,
)


class TestRetrievalContract(unittest.TestCase):
    """
    Contract requirements:
    - query "red apple" ranks A before B
    - query "ocean" returns no match (empty list)
    - Returns document IDs with results
    """

    def test_query_red_apple_ranks_a_before_b(self):
        results = retrieve("red apple")
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0], ("A", 2))
        self.assertEqual(results[1], ("B", 1))

    def test_query_ocean_returns_no_match(self):
        results = retrieve("ocean")
        self.assertEqual(results, [])

    def test_single_match_source_attribution(self):
        results = retrieve("blue")
        self.assertEqual(results, [("C", 1)])


class TestAppliedScenarioAssessment(unittest.TestCase):
    """
    Three applied questions:
    1. Predict output
    2. Diagnose failure & remedy
    3. Choose boundary policy
    """

    def test_q1_predict_output_executable_check(self):
        self.assertTrue(check_question_1_prediction())
        actual = retrieve("green")
        self.assertEqual(actual, [("B", 1)])
        self.assertIn("expected_prediction", SCENARIO_ASSESSMENT["question_1_predict_output"])

    def test_q2_diagnose_failure_executable_check(self):
        self.assertTrue(check_question_2_diagnosis())
        # Unnormalized comparison would fail without tokenize()
        self.assertEqual(tokenize("RED APPLE!"), {"red", "apple"})
        self.assertIn("remedy", SCENARIO_ASSESSMENT["question_2_diagnose_failure"])

    def test_q3_boundary_tie_breaking_policy_executable_check(self):
        self.assertTrue(check_question_3_boundary_policy())
        results = retrieve("apple")
        # Ties between A and B must rank A first
        self.assertEqual(results[0][0], "A")
        self.assertEqual(results[1][0], "B")
        self.assertEqual(SCENARIO_ASSESSMENT["question_3_boundary_policy"]["chosen_policy"], "doc_id_ascending")


class TestDeliberateFailure(unittest.TestCase):
    """
    Framework check: deliberate wrong expected result causes test to fail,
    demonstrating the framework exits non-zero on failure.
    """

    @unittest.skip("Deliberate failure demo: remove skip to verify non-zero exit")
    def test_deliberate_wrong_answer_DEMO_FAIL(self):
        results = retrieve("red apple")
        # Intentionally wrong expected order (B before A)
        self.assertEqual(results[0][0], "B", "DEMO: intentional failure")


if __name__ == "__main__":
    unittest.main()
