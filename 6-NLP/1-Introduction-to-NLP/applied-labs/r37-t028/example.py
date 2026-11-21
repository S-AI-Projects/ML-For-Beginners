"""
r37-t028: Token-Budget Preflight — Failure and Recovery Example
==============================================================
Lesson context: 6-NLP/1-Introduction-to-NLP/README.md
  "Introduction to natural language processing"

This module creates a deterministic local whitespace-token fixture that checks
prompt length against a configured budget; reports retained tokens and truncation explicitly.

Contract requirements:
- Budget 3 with "one two three four" retains ['one', 'two', 'three'] and reports 1 removed token.
- Empty input retains none (empty list []) with 0 removed tokens.
- Reject a negative budget by raising ValueError.
- Label the tokenizer as a teaching approximation, NOT the model's real tokenizer
  (real LLMs use Byte-Pair Encoding (BPE), SentencePiece, or WordPiece subwords).
- Focus: Exercise a documented invalid/missing-data case (None input or negative budget),
  explain the error, and demonstrate recovery on the next valid input.

NOTE: Simulation/mock behavior using small local fixtures.
No model download, paid provider, GPU, or physical device is required.
"""

from typing import Any, Dict, List, Optional


def tokenize_approx(text: str) -> List[str]:
    """
    Teaching approximation tokenizer (whitespace splitting).
    NOTE: This is a simplified teaching approximation, NOT a production
    model tokenizer (which uses BPE/WordPiece subword tokens).
    """
    if not isinstance(text, str):
        raise TypeError(f"Expected string input, received {type(text).__name__}")
    return text.strip().split() if text.strip() else []


def preflight_token_budget(text: Optional[str], budget: int) -> Dict[str, Any]:
    """
    Evaluates prompt length against a configured token budget.

    Validation:
    - budget < 0: raises ValueError (negative budget rejected).
    - text is None: raises ValueError (missing input data rejected).

    Returns:
    {
        "original_token_count": int,
        "budget": int,
        "retained_tokens": List[str],
        "removed_token_count": int,
        "is_truncated": bool
    }
    """
    if budget < 0:
        raise ValueError(f"Invalid budget: {budget}. Budget must be non-negative.")
    if text is None:
        raise ValueError("Invalid input: text cannot be None (missing data).")

    tokens = tokenize_approx(text)
    total_count = len(tokens)

    if total_count <= budget:
        retained = list(tokens)
        removed_count = 0
        truncated = False
    else:
        retained = tokens[:budget]
        removed_count = total_count - budget
        truncated = True

    return {
        "original_token_count": total_count,
        "budget": budget,
        "retained_tokens": retained,
        "removed_token_count": removed_count,
        "is_truncated": truncated,
    }


def exercise_failure_and_recovery() -> Dict[str, Any]:
    """
    Demonstrates failure on invalid/missing input, explains the error,
    and proves seamless recovery on the next valid input.
    """
    results = {}

    # Step 1: Failure case (negative budget)
    try:
        preflight_token_budget("one two three four", budget=-1)
        results["step1_negative_budget"] = "Unexpected success"
    except ValueError as e:
        results["step1_negative_budget"] = {
            "status": "CAUGHT_EXPECTED_ERROR",
            "error_type": type(e).__name__,
            "message": str(e),
            "explanation": "Negative resource budgets violate physical allocation bounds and fail fast before tokenizer execution.",
        }

    # Step 2: Failure case (None missing data)
    try:
        preflight_token_budget(None, budget=3)
        results["step2_missing_data"] = "Unexpected success"
    except ValueError as e:
        results["step2_missing_data"] = {
            "status": "CAUGHT_EXPECTED_ERROR",
            "error_type": type(e).__name__,
            "message": str(e),
            "explanation": "NoneType payload indicates missing or unpopulated request body; rejected at preflight.",
        }

    # Step 3: Recovery case (Valid next input)
    recovery_result = preflight_token_budget("one two three four", budget=3)
    results["step3_recovery"] = {
        "status": "RECOVERED_SUCCESSFULLY",
        "result": recovery_result,
        "explanation": "Valid payload and budget processed cleanly immediately following the failed invocations.",
    }

    return results


def run_demo():
    print("=== Token-Budget Preflight Demo ===")
    res1 = preflight_token_budget("one two three four", budget=3)
    print(f"Prompt: 'one two three four', Budget: 3")
    print(f"Retained: {res1['retained_tokens']}, Removed count: {res1['removed_token_count']}")

    res_empty = preflight_token_budget("", budget=3)
    print(f"\nEmpty Prompt, Budget: 3")
    print(f"Retained: {res_empty['retained_tokens']}, Removed count: {res_empty['removed_token_count']}")

    print("\n=== Failure & Recovery Demonstration ===")
    rec = exercise_failure_and_recovery()
    for step, info in rec.items():
        print(f"{step}: {info}")


if __name__ == "__main__":
    run_demo()
