import unittest

from example import assign_clusters

CENTROIDS = [(0, 0), (4, 0)]
POINTS = [(1, 0), (3, 0), (2, 0)]

# Explicit expected-result table, worked out by hand with identical inputs.
# point   d^2 to (0,0)   d^2 to (4,0)   label
# (1,0)        1              9           0
# (3,0)        9              1           1
# (2,0)        4              4           0   <- tie, first centroid wins
TABLE = {(1, 0): 0, (3, 0): 1, (2, 0): 0}


def independent_labels(points, centroids):
    """Simpler independent calculation: sort (distance, index) pairs and take
    the smallest. Ties sort by index, so the first centroid wins."""
    out = []
    for px, py in points:
        pairs = sorted(
            ((px - cx) ** 2 + (py - cy) ** 2, i) for i, (cx, cy) in enumerate(centroids)
        )
        out.append(pairs[0][1])
    return out


class TestAssign(unittest.TestCase):
    def test_contract_example(self):
        self.assertEqual(assign_clusters(POINTS, CENTROIDS), [0, 1, 0])

    def test_matches_expected_table(self):
        self.assertEqual(assign_clusters(POINTS, CENTROIDS), [TABLE[p] for p in POINTS])

    def test_matches_independent_calculation(self):
        self.assertEqual(assign_clusters(POINTS, CENTROIDS), independent_labels(POINTS, CENTROIDS))

    def test_matches_independent_on_more_points(self):
        pts = [(0, 0), (4, 0), (2, 5), (-1, -1), (2, -3), (3.5, 0.5)]
        self.assertEqual(assign_clusters(pts, CENTROIDS), independent_labels(pts, CENTROIDS))

    def test_tie_goes_to_first_centroid(self):
        self.assertEqual(assign_clusters([(2, 0)], CENTROIDS), [0])
        # reversing centroid order flips which index is "first"
        self.assertEqual(assign_clusters([(2, 0)], [(4, 0), (0, 0)]), [0])

    def test_single_centroid_and_no_points(self):
        self.assertEqual(assign_clusters([(9, 9)], [(0, 0)]), [0])
        self.assertEqual(assign_clusters([], CENTROIDS), [])

    def test_invalid_point_dimension(self):
        for bad in ([(1, 0, 0)], [(1,)], [()]):
            with self.assertRaises(ValueError):
                assign_clusters(bad, CENTROIDS)

    def test_invalid_centroid_dimension(self):
        with self.assertRaises(ValueError):
            assign_clusters(POINTS, [(0, 0), (4, 0, 1)])

    def test_invalid_values(self):
        for bad in ([("a", 0)], [(True, 0)], [(float("nan"), 0)], [5]):
            with self.assertRaises(ValueError):
                assign_clusters(bad, CENTROIDS)

    def test_no_centroids(self):
        with self.assertRaises(ValueError):
            assign_clusters(POINTS, [])

    def test_deliberate_wrong_result_is_detected(self):
        # A wrong expectation (ignoring the tie rule) must not equal the result.
        self.assertNotEqual(assign_clusters(POINTS, CENTROIDS), [0, 1, 1])


if __name__ == "__main__":
    unittest.main()
