"""Nearest-centroid assignment with a per-step state trace.

local teaching fixture, not a K-means training implementation

Python 3 standard library and a local checkout. The local fixture is
mandatory; any optional real-service extension needs separately
supplied credentials/hardware and is not part of this task.
"""

CENTROIDS = ((0, 0), (4, 0))


def _check_point(point):
    """Raise ValueError unless the point is 2-dimensional."""
    if len(point) != 2:
        raise ValueError(f"point is not 2-dimensional: {point!r}")


def _squared_distance(a, b):
    """Squared Euclidean distance (no square root)."""
    return (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2


def assign_with_trace(points):
    """Assign each point to its nearest fixed centroid.

    Returns (assignments, trace). The trace has one entry per point:
    the point, its two squared distances, the chosen centroid and the
    assignments so far. Ties go to the first centroid (index 0).
    All points are validated first, so an invalid point raises
    ValueError and nothing is returned.
    """
    for point in points:
        _check_point(point)
    assignments = []
    trace = []
    for point in points:
        distances = tuple(_squared_distance(point, c) for c in CENTROIDS)
        chosen = distances.index(min(distances))
        assignments.append(chosen)
        trace.append({
            "point": point,
            "distances": distances,
            "chosen": chosen,
            "assignments": list(assignments),
        })
    return assignments, trace


def main():
    points = [(1, 0), (3, 0), (2, 0)]
    final, trace = assign_with_trace(points)
    for k, step in enumerate(trace, start=1):
        print(f"step {k}: point={step['point']} "
              f"distances={step['distances']} chosen={step['chosen']} "
              f"assignments={step['assignments']}")
    print(f"final assignments: {final}")
    ok = len(trace) == len(points) and trace[-1]["assignments"] == final
    print(f"invariant check (length and last entry): {'ok' if ok else 'FAIL'}")


if __name__ == "__main__":
    main()
