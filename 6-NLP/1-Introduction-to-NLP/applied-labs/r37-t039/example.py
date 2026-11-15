"""Prompt-length budget check with a three-budget comparison (standard library only).

TEACHING APPROXIMATION: a token here is a piece of str.split(). This is NOT
the tokenizer of any real model; real tokenizers use sub-word pieces, so real
token counts differ.

preflight(text, budget) keeps the first `budget` tokens and reports what was
retained and removed. Negative budgets raise ValueError; budget 0 is allowed.

Metrics used to compare budgets on the SAME text:
    retained_count - tokens kept (a stand-in "cost": more tokens kept = more to process)
    removed_count  - tokens dropped
    coverage       - retained_count / total_tokens   (how much of the text survives)
                     policy: 1.0 when the text has no tokens (nothing was lost)
    budget_used    - retained_count / budget          (how full the budget is)
                     policy: 0.0 when budget is 0
Observed trade-off: a smaller budget keeps fewer tokens (less to process) but
lowers coverage. This says nothing about real model cost, speed or accuracy.

Simulation: fixed hand-written text, no model.
"""


def preflight(text, budget):
    if not isinstance(text, str):
        raise ValueError(f"text must be a str, got {type(text).__name__}")
    if isinstance(budget, bool) or not isinstance(budget, int):
        raise ValueError(f"budget must be an int, got {budget!r}")
    if budget < 0:
        raise ValueError(f"budget must be >= 0, got {budget}")
    tokens = text.split()
    retained = tokens[:budget]
    removed_count = len(tokens) - len(retained)
    total = len(tokens)
    return {
        "budget": budget,
        "total_tokens": total,
        "retained": retained,
        "removed_count": removed_count,
        "truncated": removed_count > 0,
        "coverage": (len(retained) / total) if total > 0 else 1.0,
        "budget_used": (len(retained) / budget) if budget > 0 else 0.0,
    }


def compare_budgets(text, budgets):
    """Run preflight on the same text with each budget; return the rows in order."""
    return [preflight(text, b) for b in budgets]


def format_comparison(text, budgets):
    lines = [f"text={text!r} (whitespace tokens: teaching approximation)",
             "budget retained removed coverage budget_used"]
    for r in compare_budgets(text, budgets):
        lines.append(
            f"{r['budget']} {len(r['retained'])} {r['removed_count']} "
            f"{r['coverage']:.3f} {r['budget_used']:.3f}"
        )
    return "\n".join(lines)


TEXT = "the room was clean and quiet"
BUDGETS = [2, 4, 8]

if __name__ == "__main__":
    r = preflight("one two three four", 3)
    print(f"contract: retained={r['retained']} removed_count={r['removed_count']} truncated={r['truncated']}")
    print(format_comparison(TEXT, BUDGETS))
