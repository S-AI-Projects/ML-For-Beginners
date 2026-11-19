"""Nearest-centroid assignment with failure and recovery demonstration.

Label: nearest-centroid test fixture, not a K-means training algorithm.

Prerequisites: Python 3 standard library and a local checkout. The local
fixture is mandatory; any optional real-service extension needs
separately supplied credentials/hardware and is not part of this task.

Contract:
- Centroids: C0 = (0, 0), C1 = (4, 0).
- Squared Euclidean distance: (x - cx)^2 + (y - cy)^2.
- Tie-break rule: if d0 <= d1 assign to centroid 0, else 1 (declared first-centroid rule).
- Headline points: (1, 0), (3, 0), (2, 0) map to 0, 1, 0.
- Rejects invalid-dimensional points (e.g. 1D or 3D or empty points).
- Focus: Exercise a documented invalid/missing-data case, explain the error,
  and demonstrate recovery on the next valid input.
"""

CENTROIDS = ((0, 0), (4, 0))


def validate_point_2d(point):
    """Validate that point is a 2-dimensional numeric sequence."""
    if not isinstance(point, (list, tuple)):
        raise TypeError(f"point must be a list or tuple, got {type(point).__name__}")
    if len(point) != 2:
        raise ValueError(f"point must be 2-dimensional, got length {len(point)}: {point!r}")
    for coord in point:
        if type(coord) is bool or not isinstance(coord, (int, float)):
            raise TypeError(f"coordinates must be numeric, got {coord!r}")


def squared_distance(p1, p2):
    """Compute squared Euclidean distance between two 2D points."""
    return (p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2


def assign_point(point):
    """Assign a single 2D point to nearest centroid (0 or 1) with first-centroid tie rule."""
    validate_point_2d(point)
    d0 = squared_distance(point, CENTROIDS[0])
    d1 = squared_distance(point, CENTROIDS[1])
    # Declared first-centroid tie rule: if d0 <= d1, pick centroid 0
    return 0 if d0 <= d1 else 1


def assign_points(points):
    """Assign a sequence of 2D points to centroids."""
    if not isinstance(points, (list, tuple)):
        raise TypeError("points must be a list or tuple")
    return [assign_point(p) for p in points]


def run_failure_and_recovery():
    """Exercise invalid data, explain the error, and demonstrate recovery on the next valid input."""
    log = []
    # Step 1: Valid initial call
    p1 = (1, 0)
    c1 = assign_point(p1)
    log.append(f"step 1 valid input {p1} -> assigned to centroid {c1}")

    # Step 2: Invalid call (3-dimensional point)
    p2 = (1, 0, 0)
    error_caught = None
    try:
        assign_point(p2)
    except ValueError as e:
        error_caught = str(e)
    log.append(f"step 2 invalid input {p2} -> rejected with ValueError: {error_caught}")

    # Step 3: Immediate recovery on next valid input
    p3 = (3, 0)
    c3 = assign_point(p3)
    log.append(f"step 3 recovery input {p3} -> assigned to centroid {c3}")
    return log


def run_contract():
    """Run headline contract cases and failure/recovery demonstration."""
    lines = []
    lines.append("nearest-centroid test fixture, not a K-means training algorithm")

    pts = [(1, 0), (3, 0), (2, 0)]
    assignments = assign_points(pts)
    lines.append(f"headline points {pts} -> {assignments}")
    lines.append("  (1,0) d0=1, d1=9 -> 0")
    lines.append("  (3,0) d0=9, d1=1 -> 1")
    lines.append("  (2,0) d0=4, d1=4 -> 0 (tie broken to first centroid)")

    lines.append("failure and recovery demonstration:")
    for entry in run_failure_and_recovery():
        lines.append(f"  {entry}")
    return "\n".join(lines)


if __name__ == "__main__":
    print(run_contract())
