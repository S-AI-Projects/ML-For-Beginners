# R37-T034: Prompt-length preflight with a state trace

Standard-library Python only. No model, download, GPU or paid service.

**Teaching approximation:** tokens are the pieces of `str.split()`. This is
NOT the tokenizer of any real model; real tokenizers use sub-word pieces, so
real token counts differ.

## Run
```
python3 6-NLP/5-Hotel-Reviews-2/applied-labs/r37-t034/example.py
python3 -m unittest discover -s 6-NLP/5-Hotel-Reviews-2/applied-labs/r37-t034 -p "test_*.py"
```

## Fixture and expected output
Text `"one two three four"`, budget `3` ->
`retained=['one', 'two', 'three'] removed_count=1 truncated=True`

State recorded after each step:

| step | state |
|---|---|
| tokenize | `['one', 'two', 'three', 'four']` |
| measure | token_count=4, budget=3, over_budget=True |
| truncate | retained=`['one', 'two', 'three']`, removed_count=1 |

## Cases
| Input | Result |
|---|---|
| `""`, budget 3 | retains none, removes 0, not truncated |
| 2 tokens, budget 3 | all kept, not truncated |
| budget 0 | every token removed |
| negative budget | `ValueError` |
| non-int budget (float, str, bool) or non-str text | `ValueError` |

## Invariants (tested)
- I1: retained + removed == number of tokens
- I2: retained is the first `budget` tokens, in order
- I3: retained never exceeds the budget
- I4: truncated is true exactly when something was removed

## Limits (simulation)
Whitespace tokens, a fixed budget and no model. It only shows the idea of a
preflight length check; it says nothing about any real model's token counts,
limits or behaviour.
