"""Offline token-budget preflight using an intentionally simple tokenizer."""

import argparse
import json
from typing import Callable, Dict, List


Tokenizer = Callable[[str], List[str]]


def whitespace_tokenizer(text: str) -> List[str]:
    """Teaching approximation: split on whitespace, not a model tokenizer."""
    return text.split()


def preflight(text: str, budget: int, tokenizer: Tokenizer = whitespace_tokenizer) -> Dict[str, object]:
    """Tokenize through a callable interface and report a deterministic budget check."""
    if budget < 0:
        raise ValueError("budget must be non-negative")

    tokens = tokenizer(text)
    retained = tokens[:budget]
    removed_count = len(tokens) - len(retained)
    return {
        "retained_tokens": retained,
        "removed_count": removed_count,
        "truncated": removed_count > 0,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Run a local whitespace-token budget simulation.")
    parser.add_argument("--text", required=True, help="input text for the local fixture")
    parser.add_argument("--budget", required=True, type=int, help="maximum retained token count")
    args = parser.parse_args()
    try:
        report = preflight(args.text, args.budget)
    except ValueError as error:
        parser.error(str(error))
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
