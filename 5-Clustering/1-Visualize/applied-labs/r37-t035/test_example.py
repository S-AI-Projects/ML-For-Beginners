import unittest

from example import assign_points, local_nearest_assigner

CENTROIDS = [(0, 0), (4, 0)]
POINTS = [(1, 0), (3, 0), (2, 0)]


class RecordingAssigner:
    """A fake service: records every call and delegates to the local adapter."""

    def __init__(self):
        self.calls = []

    def __call__(self, point, centroids):
        self.calls.append((point, list(centroids)))
        return local_nearest_assigner(point, centroids)


class TestAdapter(unittest.TestCase):
    def test_contract_example(self):
        self.assertEqual(assign_points(POINTS, CENTROIDS), [0, 1, 0])

    def test_tie_goes_to_first_centroid(self):
        self.assertEqual(assign_points([(2, 0)], CENTROIDS), [0])
        self.assertEqual(assign_points([(2, 0)], [(4, 0), (0, 0)]), [0])

    def test_dependency_is_called_through_the_interface(self):
        rec = RecordingAssigner()
        self.assertEqual(assign_points(POINTS, CENTROIDS, assigner=rec), [0, 1, 0])
        self.assertEqual([c[0] for c in rec.calls], POINTS)  # one call per point, in order

    def test_any_callable_can_replace_the_adapter(self):
        always_last = lambda point, centroids: len(centroids) - 1
        self.assertEqual(assign_points(POINTS, CENTROIDS, assigner=always_last), [1, 1, 1])

    def test_invalid_points_rejected_before_service_is_called(self):
        rec = RecordingAssigner()
        for bad in ([(1, 0), (1, 0, 0)], [(1,)], [()], [("a", 0)], [(True, 0)], [(float("nan"), 0)]):
            with self.assertRaises(ValueError):
                assign_points(bad, CENTROIDS, assigner=rec)
        self.assertEqual(rec.calls, [])  # the dependency was never reached

    def test_invalid_centroids_rejected(self):
        with self.assertRaises(ValueError):
            assign_points(POINTS, [(0, 0), (4, 0, 1)])
        with self.assertRaises(ValueError):
            assign_points(POINTS, [])

    def test_bad_service_answers_are_rejected(self):
        for bad_answer in (5, -1, 1.0, "0", None, True):
            with self.assertRaises(ValueError):
                assign_points(POINTS, CENTROIDS, assigner=lambda p, c, a=bad_answer: a)

    def test_non_callable_assigner_rejected(self):
        with self.assertRaises(ValueError):
            assign_points(POINTS, CENTROIDS, assigner="nearest")

    def test_service_errors_propagate(self):
        def failing(point, centroids):
            raise TimeoutError("simulated outage")
        with self.assertRaises(TimeoutError):
            assign_points(POINTS, CENTROIDS, assigner=failing)

    def test_no_points(self):
        self.assertEqual(assign_points([], CENTROIDS), [])

    def test_deliberate_wrong_result_is_detected(self):
        self.assertNotEqual(assign_points(POINTS, CENTROIDS), [0, 1, 1])


if __name__ == "__main__":
    unittest.main()
