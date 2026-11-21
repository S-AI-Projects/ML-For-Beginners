"""
r37-t024: Retrieval with Source Attribution — Refactor the Teaching Example
===========================================================================
Lesson context: 7-TimeSeries/3-SVR/README.md
  "Time Series Forecasting with Support Vector Regressor"

This module builds a tiny lexical retriever over three local documents, scoring
query/document overlap on lowercase word sets and breaking ties by document ID.
Returns document IDs with results.

Fixtures:
  Documents:
    A = "red apple"
    B = "green apple"
    C = "blue sky"

Behaviors:
  - query "red apple" ranks A before B (A has score 2, B has score 1, C has score 0).
  - query "ocean" returns no match (empty result list []).
  - Ties in overlap score are broken lexicographically by document ID.

Focus:
  Implement a correct baseline (`retrieve_baseline`), then extract one named
  responsibility (`score_overlap` / query-document scorer), creating `retrieve_refactored`.
  Prove before/after equivalence on all fixtures.

NOTE: This is a lexical test double, NOT a production vector search.
All behavior is simulated/mock using small local fixtures.
No model download, paid provider, GPU, or physical device is required.
"""

from typing import Dict, List, Tuple


# Standard test corpus
DOCUMENTS: Dict[str, str] = {
    "A": "red apple",
    "B": "green apple",
    "C": "blue sky",
}


def _tokenize(text: str) -> set:
    """Helper: lowercase whitespace word tokenizer."""
    return set(text.lower().split())


# ---------------------------------------------------------------------------
# Baseline implementation (monolithic)
# ---------------------------------------------------------------------------

def retrieve_baseline(query: str, corpus: Dict[str, str] = None) -> List[Tuple[str, int]]:
    """
    Baseline implementation: performs normalization, overlap calculation,
    filtering (>0 matches), and tie-breaking by doc_id all in one function.
    """
    if corpus is None:
        corpus = DOCUMENTS

    q_words = set(query.lower().split())
    scored = []
    for doc_id, text in corpus.items():
        doc_words = set(text.lower().split())
        score = len(q_words & doc_words)
        if score > 0:
            scored.append((doc_id, score))

    # Sort descending by score, ascending by doc_id on ties
    scored.sort(key=lambda item: (-item[1], item[0]))
    return scored


# ---------------------------------------------------------------------------
# Refactored implementation: Extracted Named Responsibility
# Responsibility: Lexical Overlap Scoring (`score_overlap`)
# ---------------------------------------------------------------------------

def score_overlap(query_tokens: set, doc_tokens: set) -> int:
    """
    Extracted named responsibility:
    Computes lexical set overlap between tokenized query and document.
    """
    return len(query_tokens & doc_tokens)


def retrieve_refactored(query: str, corpus: Dict[str, str] = None) -> List[Tuple[str, int]]:
    """
    Refactored retriever: delegates token overlap calculation to the
    extracted `score_overlap` responsibility while preserving the exact
    ranking, tie-breaking, and return contract.
    """
    if corpus is None:
        corpus = DOCUMENTS

    q_tokens = _tokenize(query)
    results = []
    for doc_id, doc_text in corpus.items():
        d_tokens = _tokenize(doc_text)
        score = score_overlap(q_tokens, d_tokens)
        if score > 0:
            results.append((doc_id, score))

    # Sort descending by score, breaking ties by document ID ascending
    results.sort(key=lambda x: (-x[1], x[0]))
    return results


def run_demo():
    print("=== Baseline vs Refactored Equivalence Demo ===")
    queries = ["red apple", "ocean", "apple"]
    for q in queries:
        res_base = retrieve_baseline(q)
        res_refact = retrieve_refactored(q)
        print(f"Query: '{q}'")
        print(f"  Baseline   : {res_base}")
        print(f"  Refactored : {res_refact}")
        assert res_base == res_refact, f"Mismatch for query {q}"
        print(f"  Equivalence: PROVEN ✓\n")


if __name__ == "__main__":
    run_demo()
