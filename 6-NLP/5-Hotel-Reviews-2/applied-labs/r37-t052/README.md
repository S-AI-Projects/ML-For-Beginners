# Applied Lab R37-T052: Token-Budget Preflight — Boundary-Case Lesson Extension

## Overview

This lab extends [Sentiment analysis with hotel reviews](../../README.md) by introducing token budget preflight checks. In real-world NLP and Large Language Model systems, input prompts have fixed context windows and token constraints. Exceeding token budgets leads to runtime model rejection or silent truncation.

This lab demonstrates:
- Preflight validation of prompt length against a configured integer token budget.
- Explicit tracking of retained tokens and removed token counts.
- Smallest valid cases, boundary conditions (zero budget, exact budget, empty input), and invalid inputs (negative budgets).
- Clear labeling of the local whitespace tokenizer as a teaching approximation rather than a production BPE/WordPiece tokenizer.

## Boundary Decision Matrix

| Scenario | Input Prompt | Budget | Retained Tokens | Removed Count | Truncated Flag |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Truncation** | `"one two three four"` | `3` | `["one", "two", "three"]` | `1` | `True` |
| **Exact Match** | `"one two three"` | `3` | `["one", "two", "three"]` | `0` | `False` |
| **Under Budget** | `"one two"` | `3` | `["one", "two"]` | `0` | `False` |
| **Empty Input** | `""` | `3` | `[]` | `0` | `False` |
| **Zero Budget** | `"one two"` | `0` | `[]` | `2` | `True` |
| **Negative Budget** | `"one two"` | `-1` | *Rejected (`ValueError`)* | - | - |

## Mock Limitations

1. **Teaching Approximation**: Uses whitespace-based tokenization; does not use byte-pair encoding (BPE) or subword tokenizers.
2. **No Model Vocab**: Does not translate tokens into vocabulary IDs or vector embeddings.
3. **No Special Tokens**: Does not inject `[CLS]`, `[SEP]`, or padding tokens.

## Running Tests

```bash
python3 -m unittest discover -s 6-NLP/5-Hotel-Reviews-2/applied-labs/r37-t052 -p "test_*.py" -v
```
