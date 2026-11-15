# R37-T044: nearest-centroid assignment, invariant and state trace

**Label:** local teaching fixture, not a K-means training implementation. It
assigns 2D points to two fixed centroids by squared Euclidean distance,
records the intermediate state after each step, and tests the invariant
that links that trace to the final output. It is linked from the
[Introduction to clustering lesson](../../README.md).

## Prerequisites

Python 3 standard library and a local checkout. The local fixture is
mandatory; any optional real-service extension needs separately
supplied credentials/hardware and is not part of this task.

## Run

From the repository root:

```bash
python3 5-Clustering/1-Visualize/applied-labs/r37-t044/example.py
```

Run the tests (a nonzero test count; the exit code is nonzero on any
failed assertion):

```bash
python3 -m unittest discover -s 5-Clustering/1-Visualize/applied-labs/r37-t044 -p "test_*.py"
```

## Fixture

- Centroids are fixed at `(0, 0)` and `(4, 0)`.
- Distance is the squared Euclidean distance, with no square root.
- Input points are `(1, 0)`, `(3, 0)`, `(2, 0)`.

## Worked trace and expected output

| Step | Point  | d² to (0, 0) | d² to (4, 0) | Chosen | Assignments so far |
| ---- | ------ | ------------ | ------------ | ------ | ------------------ |
| 1    | (1, 0) | 1            | 9            | 0      | [0]                |
| 2    | (3, 0) | 9            | 1            | 1      | [0, 1]             |
| 3    | (2, 0) | 4            | 4            | 0      | [0, 1, 0]          |

The CLI prints exactly this output:

```output
step 1: point=(1, 0) distances=(1, 9) chosen=0 assignments=[0]
step 2: point=(3, 0) distances=(9, 1) chosen=1 assignments=[0, 1]
step 3: point=(2, 0) distances=(4, 4) chosen=0 assignments=[0, 1, 0]
final assignments: [0, 1, 0]
invariant check (length and last entry): ok
```

## Tie rule

The point `(2, 0)` is equidistant from both centroids (4 and 4). The
tie goes to the first centroid, index 0. The code takes
`distances.index(min(distances))`, and `index` returns the first
occurrence. `test_example.py` asserts this explicitly.

## Up-front validation

Every point is checked before any work is done. A point that is not
2-dimensional, such as `()`, `(1,)` or `(1, 2, 3)`, raises `ValueError`.
A list with one invalid point raises as well, and nothing is returned,
so no partial result or trace can leak out. Empty input returns `[]`
with an empty trace.

## Invariant

For any input, the trace links the state to the final output:

- The trace has one entry per point.
- Entry `k` holds the assignments so far, which equal `final[:k+1]`.
- The last entry's assignments equal the final output.
- Each chosen centroid minimises the squared distance, and ties go to
  the first centroid.

`test_example.py` checks these over several point sets, including an
empty one.

## How it illustrates the lesson

The lesson describes Euclidean ("flat") distance, centroid clustering
where the centre is the mean of the cluster, and the idea that "the
squared distance from the cluster is minimized". This fixture shows
the assignment step of that idea: each point goes to its nearest
centroid, and the trace makes each decision visible. It also shows
why ties need a declared rule.

## Limitations

- **Not K-means training.** The centroids are fixed and never updated,
  so there is no centroid recomputation, no convergence and no learning.
  The lesson's K-means discussion is about that update loop, which this
  fixture does not implement.
- **No choice of k.** There are two centroids, chosen by hand.
- **Shape validation is a teaching guard.** The 2-dimensional check is
  an addition for this exercise; the lesson does not cover it.
- **No model or performance claim.** The output is a text trace. It
  makes no claim about trained models, real hardware or cloud services.
