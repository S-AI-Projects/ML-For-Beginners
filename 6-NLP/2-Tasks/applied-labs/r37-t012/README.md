# Local cosine similarity example

This deterministic **local calculation** compares vectors supplied directly by the caller; it does not create embeddings or call an NLP service. In the lesson's embedding concept, the vectors are the numeric representations and cosine similarity compares their direction.

Prerequisite: Python 3 standard library and a local repository checkout.

From the repository root, compare identical and orthogonal vectors:

```sh
python3 6-NLP/2-Tasks/applied-labs/r37-t012/example.py 1,0 1,0
python3 6-NLP/2-Tasks/applied-labs/r37-t012/example.py 1,0 0,1
```

Expected outputs:

```json
{"cosine_similarity": 1.0, "vector_a": [1.0, 0.0], "vector_b": [1.0, 0.0]}
{"cosine_similarity": 0.0, "vector_a": [1.0, 0.0], "vector_b": [0.0, 1.0]}
```

A zero norm has no defined cosine direction. This example returns Python `None` and serializes it as JSON `null`, without dividing by zero. The boundary decision is exact: only a computed norm equal to zero is undefined; every finite nonzero norm is normalized, even a very small one. Empty vectors, mismatched dimensions, non-numeric entries, and non-finite entries are rejected.

The fixture illustrates normalization and the normalized dot product only. It does not tokenize text, train or retrieve embeddings, establish semantic meaning, or model any cloud service, hardware, or trained-model performance.
