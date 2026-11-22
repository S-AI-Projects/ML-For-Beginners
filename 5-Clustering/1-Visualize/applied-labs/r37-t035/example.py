"""Assigning 2D points to centroids behind a callable interface (standard library only).

Idea: pretend the "which centroid is nearest?" decision is made by an EXTERNAL
service. Our code depends only on a callable with this signature:

    assigner(point, centroids) -> int      # index of the chosen centroid

`assign_points` does the work that must not depend on the service (input
validation, checking the service's answer). `local_nearest_assigner` is the
deterministic local adapter: squared Euclidean distance, and on a tie the
FIRST (lowest-index) centroid wins.

MOCK / SIMULATION: the local adapter is not a real service. It does NOT
establish any of the following about a real service:
  - network behaviour: latency, timeouts, retries, outages
  - authentication, quotas, rate limits or cost
  - the real service's distance metric or its tie-breaking rule
  - its response format or error codes
  - behaviour at scale (many points, many dimensions) or non-determinism
  - the quality of any trained model or real K-Means clustering
"""
import math


def _check_point(p, name):
    try:
        coords = list(p)
    except TypeError:
        raise ValueError(f"{name} must be a sequence of 2 numbers, got {p!r}")
    if len(coords) != 2:
        raise ValueError(f"{name} must have exactly 2 dimensions, got {len(coords)}: {p!r}")
    for v in coords:
        if isinstance(v, bool) or not isinstance(v, (int, float)) or not math.isfinite(v):
            raise ValueError(f"{name} has invalid coordinate {v!r}")
    return (coords[0], coords[1])


def local_nearest_assigner(point, centroids):
    """Deterministic local adapter: nearest centroid by squared Euclidean distance.
    Strict '<' means the first centroid wins a tie."""
    best, best_d = 0, (point[0] - centroids[0][0]) ** 2 + (point[1] - centroids[0][1]) ** 2
    for i in range(1, len(centroids)):
        d = (point[0] - centroids[i][0]) ** 2 + (point[1] - centroids[i][1]) ** 2
        if d < best_d:
            best, best_d = i, d
    return best


def assign_points(points, centroids, assigner=local_nearest_assigner):
    """Validate inputs, ask `assigner` for each point, and check its answers."""
    if not callable(assigner):
        raise ValueError("assigner must be callable")
    if len(centroids) == 0:
        raise ValueError("at least one centroid is required")
    cs = [_check_point(c, f"centroid {i}") for i, c in enumerate(centroids)]
    ps = [_check_point(p, f"point {i}") for i, p in enumerate(points)]  # all validated first
    labels = []
    for i, p in enumerate(ps):
        label = assigner(p, cs)
        if isinstance(label, bool) or not isinstance(label, int) or not 0 <= label < len(cs):
            raise ValueError(f"assigner returned invalid label {label!r} for point {i}")
        labels.append(label)
    return labels


if __name__ == "__main__":
    centroids = [(0, 0), (4, 0)]
    points = [(1, 0), (3, 0), (2, 0)]
    print(f"centroids={centroids} points={points} (local adapter, simulation)")
    print(f"labels={assign_points(points, centroids)}")
