# R37-T033: K-Means assignment step with a declared tie rule

Standard-library Python only. No model, download, GPU or paid service.

## Run
```
python3 5-Clustering/2-K-Means/applied-labs/r37-t033/example.py
python3 -m unittest discover -s 5-Clustering/2-K-Means/applied-labs/r37-t033 -p "test_*.py"
```

## Fixture and expected output
Centroids `(0,0)`, `(4,0)`; points `(1,0)`, `(3,0)`, `(2,0)` ->
`labels=[0, 1, 0]`

| point | d² to (0,0) | d² to (4,0) | label |
|---|---|---|---|
| (1,0) | 1 | 9 | 0 |
| (3,0) | 9 | 1 | 1 |
| (2,0) | 4 | 4 | 0 (tie: first centroid wins) |

## Two approaches, identical inputs
The tests compare `assign_clusters` (loop with a strict `<`) with (a) the
hand-written table above and (b) a separate calculation that sorts
`(distance, index)` pairs and takes the smallest. Both must agree.

## Decisions
- Squared Euclidean distance; no square root needed (same nearest centroid).
- Tie rule: lowest centroid index wins.
- Invalid input raises `ValueError`: points or centroids that are not exactly
  2 finite numbers (booleans rejected), or no centroids.

## Limits (simulation)
Centroids are fixed by hand. This is only the assignment step of K-Means: it
does not update centroids, iterate or train, so it says nothing about real
K-Means results, cluster quality or performance.

## Relation to the lesson

The lesson fits scikit-learn's KMeans and reads off cluster labels, without
showing how a point is matched to a centroid. This example shows that
assignment step by hand: squared Euclidean distance to each centroid, with
the nearest one winning. Ties go to the first centroid, a rule the lesson
does not state. Points must be 2-dimensional, matching the 2D data.

## Where the simplification stops

Centroids are fixed by hand, not learned. Real K-Means repeats the
assignment step and moves the centroids until they settle, uses many
more points and dimensions, and depends on how the starting centroids are
chosen. None of that is done here.
