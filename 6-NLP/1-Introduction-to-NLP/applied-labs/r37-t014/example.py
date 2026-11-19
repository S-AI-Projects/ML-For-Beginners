"""A local, whitespace-token preflight example for the NLP lesson.

Whitespace splitting is a teaching approximation. It is not a model tokenizer.
"""

import argparse
import json


def preflight(text: str, budget: int) -> dict:
    """Return a state trace and final report for a whitespace-token budget."""
    if budget < 0:
        raise ValueError("budget must be zero or greater")

    tokens = text.split()
    retained = tokens[:budget]
    removed = tokens[budget:]
    report = {
        "retained_tokens": retained,
        "removed_count": len(removed),
        "truncated": bool(removed),
    }
    return {
        "trace": [
            {"step": "input", "text": text, "budget": budget},
            {"step": "whitespace_tokenize", "tokens": tokens},
            {"step": "apply_budget", "retained": retained, "removed": removed},
            {"step": "report", **report},
        ],
        "report": report,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--text", required=True, help="local text fixture")
    parser.add_argument("--budget", required=True, type=int, help="maximum retained token count")
    args = parser.parse_args()
    try:
        result = preflight(args.text, args.budget)
    except ValueError as error:
        parser.error(str(error))
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
