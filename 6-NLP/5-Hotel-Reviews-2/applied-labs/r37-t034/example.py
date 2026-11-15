"""Prompt-length preflight check with a whitespace tokenizer (standard library only).

TEACHING APPROXIMATION: tokens here are just the pieces of str.split().
This is NOT the tokenizer of any real model; real tokenizers split text into
sub-word pieces, so real token counts differ.

Contract:
    preflight(text, budget) -> dict with the state recorded after each step
    and the final output.

Steps recorded in result["trace"]:
    1. tokenize  : text -> tokens (whitespace split)
    2. measure   : count tokens and compare with the budget
    3. truncate  : keep the first `budget` tokens, drop the rest

Final fields: retained (list), removed_count (int), truncated (bool).

Invariants (checked by the tests, and by check_invariants):
    I1. len(retained) + removed_count == len(tokens)
    I2. retained == tokens[:budget]       (order preserved, prefix kept)
    I3. len(retained) <= budget
    I4. truncated == (removed_count > 0)

Validation: budget must be an int >= 0 (bool rejected); text must be a str.
Budget 0 is allowed and removes every token. A negative budget raises
ValueError.
"""


def preflight(text, budget):
    if not isinstance(text, str):
        raise ValueError(f"text must be a str, got {type(text).__name__}")
    if isinstance(budget, bool) or not isinstance(budget, int):
        raise ValueError(f"budget must be an int, got {budget!r}")
    if budget < 0:
        raise ValueError(f"budget must be >= 0, got {budget}")

    trace = []

    tokens = text.split()
    trace.append({"step": "tokenize", "tokens": list(tokens)})

    count = len(tokens)
    over = count > budget
    trace.append({"step": "measure", "token_count": count, "budget": budget, "over_budget": over})

    retained = tokens[:budget]
    removed_count = count - len(retained)
    trace.append({"step": "truncate", "retained": list(retained), "removed_count": removed_count})

    return {
        "tokens": tokens,
        "budget": budget,
        "retained": retained,
        "removed_count": removed_count,
        "truncated": removed_count > 0,
        "trace": trace,
    }


def check_invariants(result):
    """Raise AssertionError if the recorded state and final output disagree."""
    tokens, retained = result["tokens"], result["retained"]
    assert len(retained) + result["removed_count"] == len(tokens), "I1 violated"
    assert retained == tokens[: result["budget"]], "I2 violated"
    assert len(retained) <= result["budget"], "I3 violated"
    assert result["truncated"] == (result["removed_count"] > 0), "I4 violated"


if __name__ == "__main__":
    r = preflight("one two three four", 3)
    check_invariants(r)
    print('text="one two three four" budget=3  (whitespace tokens: teaching approximation)')
    for s in r["trace"]:
        print(s)
    print(f"retained={r['retained']} removed_count={r['removed_count']} truncated={r['truncated']}")
