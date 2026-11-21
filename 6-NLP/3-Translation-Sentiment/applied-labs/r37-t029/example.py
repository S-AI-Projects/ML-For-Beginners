"""
r37-t029: Token-Budget Preflight — Runnable Concept Example
============================================================
Lesson context: 6-NLP/3-Translation-Sentiment/README.md
  "Translation and sentiment analysis with ML"

This module creates a deterministic local whitespace-token fixture that checks
prompt length against a configured budget; reports retained tokens and truncation explicitly.

Contract requirements:
- Budget 3 with "one two three four" retains ['one', 'two', 'three'] and reports 1 removed token.
- Empty input retains none (empty list []).
- Reject a negative budget (ValueError).
- Label the tokenizer as a teaching approximation, not the model's real tokenizer.
- Focus: Implement the minimal complete local example and connect each public
  input/output to the lesson concept.

Connection to Lesson Concepts:
1. `raw_text` (Input): Represents source natural language payload (e.g. translation/sentiment prompt).
2. `budget` (Input): Finite resource threshold representing maximum allowable context window.
3. `retained_tokens` (Output): The bounded token sequence safe to feed to downstream inference models.
4. `removed_token_count` (Output): Truncation metric reflecting information loss due to budget constraints.
5. `is_truncated` (Output): Boolean flag signaling to caller that input was clipped.

NOTE: Simulation/mock behavior using small local fixtures.
No model download, paid provider, GPU, or physical device is required.
"""

from typing import Any, Dict, List, Optional


def tokenize_approx(text: str) -> List[str]:
    """
    Teaching approximation tokenizer (whitespace splitting).
    NOTE: This is a simplified teaching approximation, NOT a production
    model tokenizer (which uses BPE/SentencePiece subword algorithms).
    """
    if not isinstance(text, str):
        raise TypeError(f"Expected text to be a string, got {type(text).__name__}")
    return text.strip().split() if text.strip() else []


def check_token_budget(text: str, budget: int) -> Dict[str, Any]:
    """
    Evaluates input text against a configured token budget.

    Validation:
    - budget < 0: raises ValueError (negative budget rejected).

    Returns a structured dictionary connecting inputs to lesson concepts:
    - original_token_count: number of tokens in raw text before truncation
    - budget: the enforced capacity limit
    - retained_tokens: tokens kept within budget
    - removed_token_count: number of tokens dropped
    - is_truncated: whether truncation occurred
    """
    if budget < 0:
        raise ValueError(f"Invalid negative budget: {budget}. Budget must be >= 0.")
    if text is None:
        raise ValueError("Text input must not be None.")

    tokens = tokenize_approx(text)
    total_tokens = len(tokens)

    if total_tokens <= budget:
        retained = list(tokens)
        removed = 0
        truncated = False
    else:
        retained = tokens[:budget]
        removed = total_tokens - budget
        truncated = True

    return {
        "original_token_count": total_tokens,
        "budget": budget,
        "retained_tokens": retained,
        "removed_token_count": removed,
        "is_truncated": truncated,
    }


def run_demo():
    print("=== Runnable Concept Example: Token-Budget Preflight ===")
    prompt = "one two three four"
    budget = 3
    res = check_token_budget(prompt, budget)
    print(f"Input: '{prompt}', Budget: {budget}")
    print(f"Retained: {res['retained_tokens']}")
    print(f"Removed count: {res['removed_token_count']}")
    print(f"Truncated: {res['is_truncated']}")

    empty_res = check_token_budget("", budget)
    print(f"\nEmpty Input: Retained={empty_res['retained_tokens']}, Removed={empty_res['removed_token_count']}")


if __name__ == "__main__":
    run_demo()
