# R37-T035: Point assignment behind a callable interface (offline adapter)

Standard-library Python only. No model, download, network, GPU or paid service.

## Idea
Pretend "which centroid is nearest?" is answered by an external service. The
code depends only on a callable `assigner(point, centroids) -> int`.
`local_nearest_assigner` is the deterministic local adapter (squared Euclidean
distance; ties go to the first centroid). `assign_points` validates input
and checks whatever the assigner returns.

## Run
```
python3 5-Clustering/1-Visualize/applied-labs/r37-t035/example.py
python3 -m unittest discover -s 5-Clustering/1-Visualize/applied-labs/r37-t035 -p "test_*.py"
```

## Fixture and expected output
Centroids `(0,0)`, `(4,0)`; points `(1,0)`, `(3,0)`, `(2,0)` -> `labels=[0, 1, 0]`

| point | d² to (0,0) | d² to (4,0) | label |
|---|---|---|---|
| (1,0) | 1 | 9 | 0 |
| (3,0) | 9 | 1 | 1 |
| (2,0) | 4 | 4 | 0 (tie: first centroid wins) |

## What the tests show
- Any callable can replace the adapter (a recording fake, a constant function).
- Invalid points (wrong dimension, non-numbers, NaN, booleans) are rejected
  before the assigner is ever called.
- Bad answers from the assigner (out of range, non-int) are rejected.
- A failing assigner's error propagates unchanged.

## What this mock does NOT establish about a real service
- Network behaviour: latency, timeouts, retries, outages (the "outage" test
  only raises a made-up error).
- Authentication, quotas, rate limits, cost.
- The real service's distance metric or tie-breaking rule.
- Its response format, error codes or versioning.
- Behaviour at scale, in more dimensions, or with non-deterministic answers.
- The quality of any trained model or real K-Means clustering.
