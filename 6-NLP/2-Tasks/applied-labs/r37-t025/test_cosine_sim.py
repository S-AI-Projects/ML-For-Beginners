"""
Unit tests for r37-t025: cosine-similarity lookup — offline service adapter.

Run with:
    python3 -m unittest discover -s 6-NLP/2-Tasks/applied-labs/r37-t025 -p "test_*.py" -v
"""

import math
import unittest

from example import (
    UNDEFINED_SENTINEL,
    LocalOfflineEmbeddingAdapter,
    compare_texts_via_adapter,
    cosine_similarity,
)


class TestCosineSimilarityContract(unittest.TestCase):
    """
    Contract requirements:
    - [1, 0] versus [1, 0] gives 1
    - [1, 0] versus [0, 1] gives 0
    - A zero vector returns the documented undefined-result sentinel (NaN)
    """

    def test_identical_vectors_yield_one(self):
        result = cosine_similarity([1.0, 0.0], [1.0, 0.0])
        self.assertAlmostEqual(result, 1.0, places=7)

    def test_orthogonal_vectors_yield_zero(self):
        result = cosine_similarity([1.0, 0.0], [0.0, 1.0])
        self.assertAlmostEqual(result, 0.0, places=7)

    def test_zero_vector_returns_undefined_sentinel(self):
        result = cosine_similarity([1.0, 0.0], [0.0, 0.0])
        self.assertTrue(math.isnan(result), "Expected NaN sentinel for zero vector")

    def test_both_zero_vectors_return_sentinel(self):
        result = cosine_similarity([0.0, 0.0], [0.0, 0.0])
        self.assertTrue(math.isnan(result))


class TestOfflineServiceAdapter(unittest.TestCase):
    """
    Test callable interface and deterministic offline adapter behavior.
    """

    def setUp(self):
        self.adapter = LocalOfflineEmbeddingAdapter()

    def test_adapter_callable_interface(self):
        # Must be callable
        self.assertTrue(callable(self.adapter))
        vec = self.adapter("base")
        self.assertEqual(vec, [1.0, 0.0])

    def test_adapter_lookup_same_texts(self):
        sim = compare_texts_via_adapter(self.adapter, "base", "same")
        self.assertAlmostEqual(sim, 1.0, places=7)

    def test_adapter_lookup_orthogonal_texts(self):
        sim = compare_texts_via_adapter(self.adapter, "base", "orthogonal")
        self.assertAlmostEqual(sim, 0.0, places=7)

    def test_adapter_zero_vector_sentinel(self):
        sim = compare_texts_via_adapter(self.adapter, "base", "empty_zero")
        self.assertTrue(math.isnan(sim))


class TestBoundaryAndInputValidation(unittest.TestCase):
    """
    Input validation: dimension mismatch and empty vectors.
    """

    def test_dimension_mismatch_raises(self):
        with self.assertRaises(ValueError) as ctx:
            cosine_similarity([1.0, 0.0], [1.0, 0.0, 0.0])
        self.assertIn("mismatch", str(ctx.exception))

    def test_empty_vectors_raise(self):
        with self.assertRaises(ValueError):
            cosine_similarity([], [])


class TestDeliberateFailure(unittest.TestCase):
    """
    Framework check: deliberate wrong expected result causes test to fail,
    demonstrating the framework exits non-zero on failure.
    """

    @unittest.skip("Deliberate failure demo: remove skip to verify non-zero exit")
    def test_deliberate_wrong_similarity_DEMO_FAIL(self):
        # [1, 0] vs [0, 1] is 0.0; asserting 0.99 must fail
        sim = cosine_similarity([1.0, 0.0], [0.0, 1.0])
        self.assertEqual(sim, 0.99, "DEMO: intentional failure")


if __name__ == "__main__":
    unittest.main()
