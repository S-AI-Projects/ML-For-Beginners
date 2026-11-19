# R37-T004: Cosine-Similarity Lookup - Invariant and State Trace

**Label:** local vector test double, not an NLP embedding service.

## Prerequisites

Python 3 standard library and a local checkout. The local fixture is mandatory; any optional real-service extension needs separately supplied credentials/hardware and is not part of this task.

## What It Is

A small, deterministic module for comparing local vector embeddings using cosine similarity. It records the complete intermediate calculation trace at each step:
1. `step1_dot`: Dot product `u · v`.
2. `step2_norm_u`: Euclidean norm `||u||`.
3. `step3_norm_v`: Euclidean norm `||v||`.
4. `step4_norm_product`: Product `||u|| * ||v||`.
5. `step5_zero_vector`: Boolean flag for zero-magnitude input vectors.
6. `step6_similarity`: Cosine similarity `(u · v) / (||u|| * ||v||)`, or sentinel `None` if zero vector.

## Mathematical Invariants

The state trace is explicitly linked to the output through two verified invariants:
- **Cauchy-Schwarz Invariant:** For non-zero vectors, similarity is bounded in `[-1.0, 1.0]`.
- **Reconstruction Invariant:** `similarity * norm_product == dot_product` within numerical tolerance (`1e-9`).
- **Sentinel Invariant:** If `is_zero == True`, `similarity is None`.

## Invocation

From the repository root:

```bash
python3 6-NLP/2-Tasks/applied-labs/r37-t004/example.py
```

Run unit tests from the repository root:

```bash
python3 -m unittest discover -s 6-NLP/2-Tasks/applied-labs/r37-t004 -p "test_*.py"
```

## Fixture and Expected Output

Fixture comparisons:
- `[1, 0]` vs `[1, 0]` -> `1.0000`
- `[1, 0]` vs `[0, 1]` -> `0.0000`
- `[0, 0]` vs `[1, 0]` -> `None` (documented undefined-result sentinel)

Expected CLI output:

```text
local vector test double, not an NLP embedding service
[1, 0] vs [1, 0] -> similarity=1.0000, invariant=True
[1, 0] vs [0, 1] -> similarity=0.0000, invariant=True
[0, 0] vs [1, 0] -> similarity=None (undefined sentinel), invariant=True
```

## Limitations

- Computes cosine similarity on caller-provided numeric vectors only; does not generate token embeddings or download language models.
- Does not infer semantic linguistic properties or quality.
- Makes no claims about real hardware, cloud API services, or trained-model performance.
