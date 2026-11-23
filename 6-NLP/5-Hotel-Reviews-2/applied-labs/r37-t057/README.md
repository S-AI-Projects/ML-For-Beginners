# Applied Lab R37-T057: Token-Budget Preflight — Worked Example with Checks

## Overview

This lab extends [Sentiment analysis with hotel reviews](../../README.md) by publishing a fully documented worked example and regression test harness for token-budget preflight checks.

When interacting with NLP review classifiers and LLM backends, long reviews must be checked prior to model ingestion. This lab walks through input parsing, budget comparison, token slicing, and explicit truncation telemetry.

## Canonical Worked Example Walkthrough

- **Input Prompt**: `"one two three four"`
- **Configured Token Budget**: `3`
- **Step 1 (Tokenize)**: Whitespace segmentation yields 4 tokens: `["one", "two", "three", "four"]`.
- **Step 2 (Compare)**: `len(tokens) = 4 > budget = 3`. Truncation is required (`truncated = True`).
- **Step 3 (Slice)**: Retained tokens = `tokens[:3] = ["one", "two", "three"]`.
- **Step 4 (Report)**: Removed tokens count = `4 - 3 = 1`.
- **Final Output**:
  ```json
  {
    "budget": 3,
    "total_tokens": 4,
    "retained_tokens": ["one", "two", "three"],
    "retained_count": 3,
    "removed_count": 1,
    "truncated": true,
    "retained_text": "one two three"
  }
  ```

## Boundary Policies

- **Empty Input (`""`)**: Retains `[]` and reports `0` removed tokens.
- **Negative Budget (`-1`)**: Rejected with `ValueError`.
- **Teaching Approximation**: Labels the whitespace tokenizer as a didactic approximation rather than a production subword tokenizer.

## Running Tests

```bash
python3 -m unittest discover -s 6-NLP/5-Hotel-Reviews-2/applied-labs/r37-t057 -p "test_*.py" -v
```
