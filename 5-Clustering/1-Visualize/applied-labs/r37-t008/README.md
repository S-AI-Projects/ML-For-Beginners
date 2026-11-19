# R37-T008: Nearest-Centroid Assignment - Failure and Recovery Example

**Label:** nearest-centroid test fixture, not a K-means training algorithm.

## Prerequisites

Python 3 standard library and a local checkout. The local fixture is mandatory; any optional real-service extension needs separately supplied credentials/hardware and is not part of this task.

## What It Is

A deterministic nearest-centroid assigner for 2D points against two fixed centroids:
- Centroid 0: `(0, 0)`
- Centroid 1: `(4, 0)`

Metric: Squared Euclidean distance $(x - c_x)^2 + (y - c_y)^2$ without square roots.
Tie Rule: When distances to both centroids are equal, points are assigned to Centroid 0 (declared first-centroid tie rule).

## Distance Calculations for Headline Points

- Point `(1, 0)`:
  - $d_0 = (1 - 0)^2 + 0 = 1$
  - $d_1 = (1 - 4)^2 + 0 = 9$
  - Assigned to **0**
- Point `(3, 0)`:
  - $d_0 = (3 - 0)^2 + 0 = 9$
  - $d_1 = (3 - 4)^2 + 0 = 1$
  - Assigned to **1**
- Point `(2, 0)`:
  - $d_0 = (2 - 0)^2 + 0 = 4$
  - $d_1 = (2 - 4)^2 + 0 = 4$
  - Tie broken to **0** by declared first-centroid rule

Result: `[(1, 0), (3, 0), (2, 0)]` maps to `[0, 1, 0]`.

## Failure and Recovery Demonstration

The assigner is completely stateless and validates dimensionality before computation:
1. **Valid call:** `assign_point((1, 0))` succeeds and returns `0`.
2. **Invalid call:** `assign_point((1, 0, 0))` rejects the 3D point and raises `ValueError("point must be 2-dimensional")`.
3. **Recovery:** The error leaves no mutated internal state; the very next call `assign_point((3, 0))` executes cleanly and returns `1`.

## Invocation

From the repository root:

```bash
python3 5-Clustering/1-Visualize/applied-labs/r37-t008/example.py
```

Run unit tests from the repository root:

```bash
python3 -m unittest discover -s 5-Clustering/1-Visualize/applied-labs/r37-t008 -p "test_*.py"
```

## Fixture and Expected Output

Expected CLI output:

```text
nearest-centroid test fixture, not a K-means training algorithm
headline points [(1, 0), (3, 0), (2, 0)] -> [0, 1, 0]
  (1,0) d0=1, d1=9 -> 0
  (3,0) d0=9, d1=1 -> 1
  (2,0) d0=4, d1=4 -> 0 (tie broken to first centroid)
failure and recovery demonstration:
  step 1 valid input (1, 0) -> assigned to centroid 0
  step 2 invalid input (1, 0, 0) -> rejected with ValueError: point must be 2-dimensional, got length 3: (1, 0, 0)
  step 3 recovery input (3, 0) -> assigned to centroid 1
```

## Limitations

- Fixed 2D centroids only; does not perform iterative K-means clustering or centroid recalculation.
- No dataset loading or visualization plotting libraries.
- Makes no claims about real hardware, cloud service behavior, or trained model performance.
