"""K-Means assignment step for 2D points (standard library only).

Contract:
    assign_clusters(points, centroids) -> list of centroid indices.
    Each point goes to the centroid with the smallest SQUARED Euclidean
    distance: (px - cx)**2 + (py - cy)**2. No square root is needed because
    squaring is monotonic, so the nearest centroid is the same.

Tie rule (declared): if two or more centroids are equally close, the point
goes to the FIRST (lowest-index) centroid.

Validation: every point and every centroid must be a sequence of exactly 2
finite numbers (bool is rejected), and at least one centroid is required.
Violations raise ValueError.

Simulation note: this is only the "assign points to centroids" step with
fixed, hand-chosen centroids. It does NOT move centroids, iterate, or train
a model, so it says nothing about real K-Means results or performance.
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
    return coords[0], coords[1]


def squared_distance(p, c):
    return (p[0] - c[0]) ** 2 + (p[1] - c[1]) ** 2


def assign_clusters(points, centroids):
    if len(centroids) == 0:
        raise ValueError("at least one centroid is required")
    cs = [_check_point(c, f"centroid {i}") for i, c in enumerate(centroids)]
    ps = [_check_point(p, f"point {i}") for i, p in enumerate(points)]
    labels = []
    for p in ps:
        best, best_d = 0, squared_distance(p, cs[0])
        for i in range(1, len(cs)):
            d = squared_distance(p, cs[i])
            if d < best_d:  # strict '<' keeps the first centroid on ties
                best, best_d = i, d
        labels.append(best)
    return labels


if __name__ == "__main__":
    centroids = [(0, 0), (4, 0)]
    points = [(1, 0), (3, 0), (2, 0)]
    print(f"centroids={centroids} points={points}")
    print(f"labels={assign_clusters(points, centroids)}")
