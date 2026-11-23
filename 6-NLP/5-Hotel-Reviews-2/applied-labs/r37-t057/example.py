"""Token-budget preflight — worked example with checks for 6-NLP/5-Hotel-Reviews-2."""

import re
from typing import Any, Dict, List

MOCK_LIMITATIONS = [
    "Teaching approximation: splits on whitespace and punctuation only; does not implement BPE, WordPiece, or SentencePiece.",
    "Does not use real vocabulary IDs or subword merge tables.",
    "Does not account for model-specific special tokens ([CLS], [SEP], <bos>, <eos>).",
    "Does not establish GPU memory bounds or sequence packing.",
]


def tokenize_whitespace(text: str) -> List[str]:
    """Teaching approximation tokenizer splitting on whitespace."""
    if not text:
        return []
    return [t for t in re.findall(r'\S+', text)]


def check_token_budget_worked_example(prompt: str, budget: int) -> Dict[str, Any]:
    """Worked example function evaluating token budget preflight.
    
    Budget must be non-negative.
    Reports retained tokens and removed tokens explicitly.
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


def get_canonical_worked_example() -> Dict[str, Any]:
    """Returns the canonical worked example with input, step-by-step logic, and output."""
    prompt = "one two three four"
    budget = 3
    result = check_token_budget_worked_example(prompt, budget)
    return {
        "input_prompt": prompt,
        "input_budget": budget,
        "tokenized_steps": ["one", "two", "three", "four"],
        "budget_limit": 3,
        "slice_operation": "tokens[:3]",
        "expected_retained": ["one", "two", "three"],
        "expected_removed_count": 1,
        "actual_result": result,
    }


if __name__ == "__main__":
    import json
    canonical = get_canonical_worked_example()
    print("Canonical Worked Example:")
    print(json.dumps(canonical, indent=2))
