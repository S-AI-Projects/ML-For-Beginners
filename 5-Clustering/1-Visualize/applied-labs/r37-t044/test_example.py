"""Tests for the nearest-centroid teaching fixture in example.py."""

import unittest

from example import CENTROIDS, assign_with_trace

INVARIANT_SETS = [
    [(1, 0), (3, 0), (2, 0)],
    [(0, 0)],
    [(5, 5), (-1, 2), (2, 0), (4, 0)],
    [(-3, 1), (10, -2), (0.5, 0.5)],
    [],
]


class AssignWithTraceTests(unittest.TestCase):

    def test_headline_assignment(self):
        final, _ = assign_with_trace([(1, 0), (3, 0), (2, 0)])
        self.assertEqual(final, [0, 1, 0])

    def test_tie_goes_to_first_centroid(self):
        _, trace = assign_with_trace([(1, 0), (3, 0), (2, 0)])
        self.assertEqual(trace[2]["distances"], (4, 4))
        self.assertEqual(trace[2]["chosen"], 0)

    def test_squared_distances_not_square_roots(self):
        _, trace = assign_with_trace([(3, 0), (1, 2)])
        self.assertEqual(trace[0]["distances"], (9, 1))
        self.assertEqual(trace[1]["distances"], (5, 13))

    def test_point_equal_to_centroid(self):
        _, trace = assign_with_trace([(4, 0), (0, 0)])
        self.assertEqual(trace[0]["distances"], (16, 0))
        self.assertEqual(trace[0]["chosen"], 1)
        self.assertEqual(trace[1]["distances"], (0, 16))
        self.assertEqual(trace[1]["chosen"], 0)

    def test_invalid_points_rejected(self):
        for bad in [(), (1,), (1, 2, 3)]:
            with self.subTest(point=bad):
                with self.assertRaises(ValueError):
                    assign_with_trace([bad])

    def test_mixed_list_rejected_up_front(self):
        # Only the middle point is invalid; the call must raise and
        # return nothing, so no partial result or trace can leak out.
        with self.assertRaises(ValueError):
            assign_with_trace([(1, 0), (1,), (2, 0)])

    def test_empty_input(self):
        self.assertEqual(assign_with_trace([]), ([], []))

    def test_invariants_over_several_point_sets(self):
        for points in INVARIANT_SETS:
            with self.subTest(points=points):
                final, trace = assign_with_trace(points)
                self.assertEqual(len(trace), len(points))
                for k, entry in enumerate(trace):
                    self.assertEqual(entry["point"], points[k])
                    self.assertEqual(entry["assignments"], final[:k + 1])
                    d = entry["distances"]
                    c = entry["chosen"]
                    self.assertEqual(len(d), len(CENTROIDS))
                    self.assertEqual(d[c], min(d))
                    if d[0] == d[1]:
                        self.assertEqual(c, 0)
                if trace:
                    self.assertEqual(trace[-1]["assignments"], final)


if __name__ == "__main__":
    unittest.main()
