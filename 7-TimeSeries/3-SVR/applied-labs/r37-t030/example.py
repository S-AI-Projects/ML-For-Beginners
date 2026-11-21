"""
r37-t030: Retrieval with Source Attribution — Scenario Assessment
=================================================================
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

Focus: Add three applied questions about the local example:
  1. Predict an output: Given query "green", predict exact ranking and score.
  2. Diagnose a failure: Explain why query "RED APPLE!" without case/punctuation normalization
     fails in a raw comparison, and demonstrate the normalization remedy.
  3. Choose a boundary policy: Evaluate tie-breaking policy options (doc_id ascending vs arbitrary order)
     and explain why deterministic tie-breaking is necessary for reproducible evaluation.
  Provide a rationale and executable check for each factual answer.

NOTE: This is a lexical test double, NOT a production vector search.
All behavior is simulated/mock using small local fixtures.
No model download, paid provider, GPU, or physical device is required.
"""

import re
from typing import Any, Dict, List, Tuple


DOCUMENTS: Dict[str, str] = {
    "A": "red apple",
    "B": "green apple",
    "C": "blue sky",
}


def tokenize(text: str) -> set:
    """Lowercase word tokenizer with punctuation stripping."""
    words = re.findall(r"\b\w+\b", text.lower())
    return set(words)


def retrieve(query: str, corpus: Dict[str, str] = None) -> List[Tuple[str, int]]:
    """
    Lexical retriever:
    Scores query/document overlap on lowercase word sets.
    Filters out score <= 0.
    Breaks ties by document ID ascending.
    """
    if corpus is None:
        corpus = DOCUMENTS

    q_tokens = tokenize(query)
    scored = []
    for doc_id, doc_text in corpus.items():
        d_tokens = tokenize(doc_text)
        score = len(q_tokens & d_tokens)
        if score > 0:
            scored.append((doc_id, score))

    # Sort descending by score, ascending by doc_id on ties
    scored.sort(key=lambda x: (-x[1], x[0]))
    return scored


# ---------------------------------------------------------------------------
# Applied Scenario Assessment Questions & Checks
# ---------------------------------------------------------------------------

SCENARIO_ASSESSMENT = {
    "question_1_predict_output": {
        "question": "Given query 'green', what is the exact output tuple list?",
        "expected_prediction": [("B", 1)],
        "rationale": "Only document B contains the token 'green' (overlap score 1). A and C have 0 overlap and are omitted.",
    },
    "question_2_diagnose_failure": {
        "question": "Why would query 'RED APPLE!' fail to match if normalization were omitted?",
        "diagnosis": "Case and punctuation mismatch: 'RED' != 'red' and 'APPLE!' != 'apple' under exact literal string comparison.",
        "remedy": "Lowercase normalization and punctuation stripping before token set intersection ensures robust matching.",
    },
    "question_3_boundary_policy": {
        "question": "When two documents have identical overlap scores, which tie-breaking policy should be chosen and why?",
        "chosen_policy": "doc_id_ascending",
        "rationale": "Arbitrary hash/insertion order leads to non-deterministic test outputs across different platforms. Sorting by doc_id ascending guarantees 100% deterministic, reproducible evaluation.",
    },
}


def check_question_1_prediction() -> bool:
    """Executable check for Question 1: predict output for 'green'."""
    actual = retrieve("green")
    expected = SCENARIO_ASSESSMENT["question_1_predict_output"]["expected_prediction"]
    return actual == expected


def check_question_2_diagnosis() -> bool:
    """Executable check for Question 2: normalize 'RED APPLE!' and verify match with A and B."""
    raw_query = "RED APPLE!"
    # With normalization, 'RED APPLE!' must match A (score 2) and B (score 1)
    normalized_results = retrieve(raw_query)
    return normalized_results == [("A", 2), ("B", 1)]


def check_question_3_boundary_policy() -> bool:
    """Executable check for Question 3: query 'apple' matches A and B with equal score 1; tie must be broken by doc_id."""
    results = retrieve("apple")
    # Both A and B have score 1; policy requires A before B
    return results == [("A", 1), ("B", 1)]


def run_demo():
    print("=== Retrieval with Source Attribution Demo ===")
    print("Query 'red apple':", retrieve("red apple"))
    print("Query 'ocean':", retrieve("ocean"))
    print("\n=== Scenario Assessment Checks ===")
    print("Check 1 (Predict output 'green'):", check_question_1_prediction())
    print("Check 2 (Diagnose failure & normalization):", check_question_2_diagnosis())
    print("Check 3 (Boundary tie-breaking policy):", check_question_3_boundary_policy())


if __name__ == "__main__":
    run_demo()
