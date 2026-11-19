"""Unit tests for cosine similarity with state trace in example.py."""

import unittest

import example


class CosineSimilarityTests(unittest.TestCase):

    def test_identical_vectors_similarity_one(self):
        sim, trace = example.cosine_similarity_with_trace([1, 0], [1, 0])
        self.assertEqual(sim, 1.0)
        self.assertTrue(example.check_trace_invariant(trace))

    def test_orthogonal_vectors_similarity_zero(self):
        sim, trace = example.cosine_similarity_with_trace([1, 0], [0, 1])
        self.assertEqual(sim, 0.0)
        self.assertTrue(example.check_trace_invariant(trace))

    def test_zero_vector_returns_undefined_sentinel(self):
        sim, trace = example.cosine_similarity_with_trace([0, 0], [1, 0])
        self.assertIsNone(sim)
        self.assertTrue(trace["step5_zero_vector"])
        self.assertTrue(example.check_trace_invariant(trace))

    def test_both_zero_vectors_return_sentinel(self):
        sim, trace = example.cosine_similarity_with_trace([0, 0], [0, 0])
        self.assertIsNone(sim)
        self.assertTrue(example.check_trace_invariant(trace))

    def test_opposite_vectors_similarity_negative_one(self):
        sim, trace = example.cosine_similarity_with_trace([1, 0], [-1, 0])
        self.assertEqual(sim, -1.0)
        self.assertTrue(example.check_trace_invariant(trace))

    def test_intermediate_trace_steps_recorded(self):
        _, trace = example.cosine_similarity_with_trace([3, 4], [3, 4])
        self.assertIn("step1_dot", trace)
        self.assertIn("step2_norm_u", trace)
        self.assertIn("step3_norm_v", trace)
        self.assertIn("step4_norm_product", trace)
        self.assertIn("step5_zero_vector", trace)
        self.assertIn("step6_similarity", trace)
        self.assertEqual(trace["step1_dot"], 25)
        self.assertEqual(trace["step2_norm_u"], 5.0)
        self.assertEqual(trace["step3_norm_v"], 5.0)
        self.assertEqual(trace["step4_norm_product"], 25.0)

    def test_invariant_holds_arbitrary_vectors(self):
        sim, trace = example.cosine_similarity_with_trace([1, 2, 3], [4, 5, 6])
        self.assertTrue(example.check_trace_invariant(trace))
        self.assertGreater(sim, 0.0)

    def test_dimension_mismatch_raises(self):
        with self.assertRaises(ValueError):
            example.cosine_similarity_with_trace([1, 0], [1, 0, 0])

    def test_empty_vector_raises(self):
        with self.assertRaises(ValueError):
            example.cosine_similarity_with_trace([], [])

    def test_non_numeric_elements_raises(self):
        with self.assertRaises(TypeError):
            example.cosine_similarity_with_trace([1, "a"], [1, 0])
        with self.assertRaises(TypeError):
            example.cosine_similarity_with_trace([True, False], [1, 0])


if __name__ == "__main__":
    unittest.main()
