import math
import unittest

from example import cosine_similarity


class CosineSimilarityTests(unittest.TestCase):
    def test_identical_smallest_valid_vectors(self):
        self.assertEqual(cosine_similarity([1, 0], [1, 0]), 1.0)

    def test_orthogonal_vectors(self):
        self.assertEqual(cosine_similarity([1, 0], [0, 1]), 0.0)

    def test_zero_vector_on_either_side_returns_undefined_sentinel(self):
        self.assertIsNone(cosine_similarity([0, 0], [1, 0]))
        self.assertIsNone(cosine_similarity([1, 0], [0, 0]))

    def test_exact_zero_boundary_does_not_use_epsilon_cutoff(self):
        self.assertEqual(cosine_similarity([1e-300, 0], [1, 0]), 1.0)

    def test_opposite_direction(self):
        self.assertEqual(cosine_similarity([1, 0], [-1, 0]), -1.0)

    def test_large_finite_vectors_do_not_overflow(self):
        self.assertTrue(math.isclose(cosine_similarity([1e308, 0], [1e308, 0]), 1.0))

    def test_empty_vector_is_invalid(self):
        with self.assertRaisesRegex(ValueError, "must not be empty"):
            cosine_similarity([], [])

    def test_dimensions_must_match(self):
        with self.assertRaisesRegex(ValueError, "same dimension"):
            cosine_similarity([1, 0], [1])

    def test_non_numeric_entry_is_invalid(self):
        with self.assertRaisesRegex(ValueError, "entries must be numbers"):
            cosine_similarity([1, "x"], [1, 0])

    def test_non_finite_entry_is_invalid(self):
        with self.assertRaisesRegex(ValueError, "entries must be finite"):
            cosine_similarity([math.inf], [1])


if __name__ == "__main__":
    unittest.main()
