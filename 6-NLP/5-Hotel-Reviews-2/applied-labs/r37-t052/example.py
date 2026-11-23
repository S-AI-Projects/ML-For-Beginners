"""Token-budget preflight — boundary-case lesson extension for 6-NLP/5-Hotel-Reviews-2."""

import re
from typing import Dict, List, Any

MOCK_LIMITATIONS = [
    "Teaching approximation: splits on whitespace and punctuation only; does not implement BPE, WordPiece, or SentencePiece.",
    "Does not use real vocabulary IDs or subword merge tables.",
    "Does not account for model-specific special tokens ([CLS], [SEP], <bos>, <eos>).",
    "Does not establish GPU memory bounds or sequence packing.",
]


def tokenize_whitespace(text: str) -> List[str]:
    """Teaching approximation tokenizer splitting on whitespace and basic punctuation."""
    if not text:
        return []
    # Tokenize words/tokens preserving sequence
    return [t for t in re.findall(r'\S+', text)]


def check_token_budget(prompt: str, budget: int) -> Dict[str, Any]:
    """Checks prompt length against a configured token budget with boundary validation.
    
    Budget must be non-negative (rejects negative budget).
    Returns retained tokens, count of removed tokens, and truncation flag.
    """
    if budget < 0:
        raise ValueError(f"Invalid negative budget: {budget}. Budget must be non-negative (>= 0).")

    tokens = tokenize_whitespace(prompt)
    total_tokens = len(tokens)

    if total_tokens <= budget:
        retained = tokens
        removed_count = 0
        truncated = False
    else:
        retained = tokens[:budget]
        removed_count = total_tokens - budget
        truncated = True

    return {
        "budget": budget,
        "total_tokens": total_tokens,
        "retained_tokens": retained,
        "retained_count": len(retained),
        "removed_count": removed_count,
        "truncated": truncated,
        "retained_text": " ".join(retained),
    }


def run_demo() -> Dict[str, Any]:
    return {
        "normal_truncation": check_token_budget("one two three four", 3),
        "exact_budget": check_token_budget("one two three", 3),
        "under_budget": check_token_budget("one two", 3),
        "empty_input": check_token_budget("", 3),
        "zero_budget": check_token_budget("one two", 0),
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run_demo(), indent=2))
