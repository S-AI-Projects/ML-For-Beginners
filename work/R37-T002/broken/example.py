"""Retrieval with source attribution on local documents.

Label: lexical test double, not a production vector search.

Prerequisites: Python 3 standard library and a local checkout. The local
fixture is mandatory; any optional real-service extension needs
separately supplied credentials/hardware and is not part of this task.

Contract:
- Documents: A="red apple", B="green apple", C="blue sky".
- Overlap score: number of shared lowercase words between query and document.
- Ranking: descending by score, tie-broken by document ID ascending.
- Boundary decision: documents with score 0 are excluded ("ocean" returns no match).
- Returns document IDs with results.
"""

DOCUMENTS = {
    "A": "red apple",
    "B": "green apple",
    "C": "blue sky"
}


def tokenize(text):
    """Normalize text to a lowercase set of alphanumeric word tokens."""
    if not isinstance(text, str):
        raise TypeError(f"text must be string, got {type(text).__name__}")
    cleaned = "".join(c.lower() if c.isalnum() else " " for c in text)
    tokens = set(cleaned.split())
    return tokens


def score_overlap(doc_text, query_text):
    """Compute count of overlapping unique words between doc and query."""
    doc_words = tokenize(doc_text)
    query_words = tokenize(query_text)
    return len(doc_words & query_words)


def retrieve(query, documents=None):
    """Retrieve matching documents ranked by overlap score, tie-broken by doc ID.

    Returns list of (doc_id, score) tuples for documents with score > 0.
    """
    if not isinstance(query, str):
        raise TypeError(f"query must be a string, got {type(query).__name__}")
    if len(query.strip()) == 0:
        raise ValueError("query cannot be empty or whitespace only")

    docs = DOCUMENTS if documents is None else documents
    if not isinstance(docs, dict) or len(docs) == 0:
        raise ValueError("documents corpus must be a non-empty dictionary")

    scored = []
    for doc_id, doc_text in docs.items():
        s = score_overlap(doc_text, query)
        if s > 0:
            scored.append((doc_id, s))

    # Sort: score descending (-score), then doc_id ascending
    scored.sort(key=lambda item: (-item[1], item[0]))
    return scored


def run_contract():
    """Run headline contract and boundary scenarios."""
    lines = []
    lines.append("lexical test double, not a production vector search")
    # 1. Query "red apple"
    res1 = retrieve("red apple")
    lines.append(f"query 'red apple' -> {res1}")

    # 2. Query "ocean"
    res2 = retrieve("ocean")
    lines.append(f"query 'ocean' -> {res2}")

    # 3. Smallest valid single-word match
    res3 = retrieve("sky")
    lines.append(f"smallest valid query 'sky' -> {res3}")

    # 4. Tie-breaking boundary "apple"
    res4 = retrieve("apple")
    lines.append(f"tie-break boundary query 'apple' -> {res4}")
    return "\n".join(lines)


if __name__ == "__main__":
    print(run_contract())
