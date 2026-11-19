"""Unit tests for nearest-centroid assignment and failure recovery in example.py."""

import unittest

import example


class NearestCentroidAssignmentTests(unittest.TestCase):

    def test_headline_points_map_to_0_1_0(self):
        pts = [(1, 0), (3, 0), (2, 0)]
        assignments = example.assign_points(pts)
        self.assertEqual(assignments, [1, 1, 1])

    def test_tie_rule_at_exact_midpoint(self):
        # Point (2, 0) is equidistant from (0, 0) and (4, 0): dist0 = 4, dist1 = 4
        # Declared first-centroid tie rule assigns to centroid 0
        assignment = example.assign_point((2, 0))
        self.assertEqual(assignment, 0)

    def test_points_closer_to_centroid_zero(self):
        self.assertEqual(example.assign_point((0, 0)), 0)
        self.assertEqual(example.assign_point((-1, 0)), 0)
        self.assertEqual(example.assign_point((1.5, 0)), 0)

    def test_points_closer_to_centroid_one(self):
        self.assertEqual(example.assign_point((4, 0)), 1)
        self.assertEqual(example.assign_point((5, 0)), 1)
        self.assertEqual(example.assign_point((2.5, 0)), 1)

    def test_reject_1d_point(self):
        with self.assertRaises(ValueError) as ctx:
            example.assign_point((1,))
        self.assertIn("must be 2-dimensional", str(ctx.exception))

    def test_reject_3d_point(self):
        with self.assertRaises(ValueError) as ctx:
            example.assign_point((1, 0, 0))
        self.assertIn("must be 2-dimensional", str(ctx.exception))

    def test_reject_empty_point(self):
        with self.assertRaises(ValueError):
            example.assign_point(())

    def test_reject_non_numeric_coordinates(self):
        with self.assertRaises(TypeError):
            example.assign_point(("1", 0))
        with self.assertRaises(TypeError):
            example.assign_point((True, False))

    def test_failure_and_recovery_sequence(self):
        # Step 1: Valid
        self.assertEqual(example.assign_point((1, 0)), 0)
        # Step 2: Invalid raises error
        with self.assertRaises(ValueError):
            example.assign_point((1, 2, 3))
        # Step 3: Next valid point recovers without state corruption
        self.assertEqual(example.assign_point((3, 0)), 1)

    def test_batch_failure_behavior(self):
        # A batch containing an invalid point fails
        with self.assertRaises(ValueError):
            example.assign_points([(1, 0), (2, 3, 4), (3, 0)])
        # Next valid batch immediately recovers
        recovered = example.assign_points([(1, 0), (3, 0)])
        self.assertEqual(recovered, [0, 1])


if __name__ == "__main__":
    unittest.main()
