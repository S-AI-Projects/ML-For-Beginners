"""Compare two supplied embedding vectors using cosine similarity."""
from __future__ import annotations

import argparse
import json
import math
from collections.abc import Iterable
from numbers import Real


def _vector(values: Iterable[Real], name: str) -> tuple[float, ...]:
    if isinstance(values, (str, bytes)):
        raise ValueError(f"{name} must be a non-empty sequence of finite numbers")
    try:
        result = tuple(values)
    except TypeError as error:
        raise ValueError(f"{name} must be a non-empty sequence of finite numbers") from error
    if not result:
        raise ValueError(f"{name} must not be empty")
    if any(isinstance(value, bool) or not isinstance(value, Real) for value in result):
        raise ValueError(f"{name} entries must be numbers")
    converted = tuple(float(value) for value in result)
    if not all(math.isfinite(value) for value in converted):
        raise ValueError(f"{name} entries must be finite")
    return converted


def cosine_similarity(vector_a: Iterable[Real], vector_b: Iterable[Real]) -> float | None:
    """Return cosine similarity, or None when either vector has exactly zero norm.

    The zero boundary is exact: a norm equal to 0 is undefined; every finite,
    nonzero vector, however small, is normalized and compared.
    """
    a = _vector(vector_a, "vector_a")
    b = _vector(vector_b, "vector_b")
    if len(a) != len(b):
        raise ValueError("vectors must have the same dimension")

    norm_a = math.hypot(*a)
    norm_b = math.hypot(*b)
    if norm_a == 0.0 or norm_b == 0.0:
        return None

    # Normalize before the dot product to avoid overflow for large finite inputs.
    score = sum((left / norm_a) * (right / norm_b) for left, right in zip(a, b))
    return max(-1.0, min(1.0, score))


def _parse_vector(text: str) -> list[float]:
    try:
        return [float(part.strip()) for part in text.split(",")]
    except ValueError as error:
        raise argparse.ArgumentTypeError("use comma-separated numbers, e.g. 1,0") from error


def main() -> None:
    parser = argparse.ArgumentParser(description="Compare two local embedding vectors.")
    parser.add_argument("vector_a", type=_parse_vector, help="comma-separated finite numbers")
    parser.add_argument("vector_b", type=_parse_vector, help="comma-separated finite numbers")
    args = parser.parse_args()
    try:
        score = cosine_similarity(args.vector_a, args.vector_b)
    except ValueError as error:
        parser.error(str(error))
    print(json.dumps({"vector_a": args.vector_a, "vector_b": args.vector_b,
                      "cosine_similarity": score}, allow_nan=False, sort_keys=True))


if __name__ == "__main__":
    main()
