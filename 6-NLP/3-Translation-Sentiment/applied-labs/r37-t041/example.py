"""Token-budget preflight for a teaching lab (R37-T041).

Teaching approximation: this splits text on whitespace. It is NOT the tokenizer
of any real model, so counts will differ from a production model's tokens.

Python 3 standard library and a local checkout. The local fixture is mandatory;
any optional real-service extension needs separately supplied
credentials/hardware and is not part of this task.

Boundary decision: the first `budget` tokens are kept and the rest are removed.
An exact fit (len(tokens) == budget) is not truncated; budget 0 keeps nothing.
"""

import sys


def preflight_tokens(text, budget):
    """Keep the first `budget` whitespace tokens of `text` and report what
    was removed."""
    if budget < 0:
        raise ValueError("budget must be >= 0")
    tokens = text.split()
    retained = tokens[:budget]
    removed_count = len(tokens) - len(retained)
    return {
        "retained": retained,
        "removed_count": removed_count,
        "truncated": removed_count > 0,
    }


def main():
    text = "one two three four"
    budget = 3
    result = preflight_tokens(text, budget)
    print("tokenizer: whitespace split "
          "(teaching approximation, not a model tokenizer)")
    print(f"input: {text!r}")
    print(f"budget: {budget}")
    print(f"retained: {result['retained']}")
    print(f"removed_count: {result['removed_count']}")
    print(f"truncated: {result['truncated']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
