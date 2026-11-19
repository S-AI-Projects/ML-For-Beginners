# R37-T002: Retrieval with Source Attribution - Boundary-Case Lesson Extension

**Label:** lexical test double, not a production vector search.

## Prerequisites

Python 3 standard library and a local checkout. The local fixture is mandatory; any optional real-service extension needs separately supplied credentials/hardware and is not part of this task.

## What It Is

A small, deterministic lexical retriever over three local documents:
- Document A: `"red apple"`
- Document B: `"green apple"`
- Document C: `"blue sky"`

It scores query/document overlap on lowercase word sets and breaks ties by document ID in ascending alphabetical order. It returns document IDs with results.

## Invocation

From the repository root:

```bash
python3 7-TimeSeries/3-SVR/applied-labs/r37-t002/example.py
```

Run unit tests from the repository root:

```bash
python3 -m unittest discover -s 7-TimeSeries/3-SVR/applied-labs/r37-t002 -p "test_*.py"
```

## Fixture and Expected Output

Fixture documents:
- A: `"red apple"`
- B: `"green apple"`
- C: `"blue sky"`

Expected CLI output:

```text
lexical test double, not a production vector search
query 'red apple' -> [('A', 2), ('B', 1)]
query 'ocean' -> []
smallest valid query 'sky' -> [('C', 1)]
tie-break boundary query 'apple' -> [('A', 1), ('B', 1)]
```

## Boundary Decisions

- **Smallest valid case:** A single matching word (e.g., query `"sky"`) returns a single attributed match `[('C', 1)]`.
- **Zero-overlap boundary:** Words not present in any document (e.g., `"ocean"`) return an empty list `[]` rather than scores of 0 or dummy attributions.
- **Tie-breaking boundary:** When documents share equal overlap scores (e.g., query `"apple"` matches A and B with score 1), ties are strictly broken by document ID ascending (`'A'` before `'B'`).
- **Token normalization boundary:** Punctuation and casing are normalized (`"RED APPLE"` matches identically to `"red apple"`). Sets prevent repeated query words (`"apple apple"`) from inflating scores.
- **Invalid cases:** Empty queries or non-string inputs raise `ValueError` and `TypeError` respectively.

## Limitations

- Lexical word-overlap only; no semantic embeddings, cosine similarity, or vector indices.
- Fixed 3-document corpus; does not scale to large collections.
- Makes no claims about real hardware, cloud search services, or trained model performance.
