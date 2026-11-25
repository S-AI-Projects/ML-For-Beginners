"""Assert the checked-in example matches the recorded expected statuses."""
import json
from pathlib import Path
import sys

repo = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(repo / "1-Introduction/1-intro-to-ML/applied-labs/r37-t016"))
import example

expected = json.loads((Path(__file__).parent / "expected.json").read_text())
actual = example.evaluate(example.load_fixture())
assert actual == expected, f"expected {expected!r}; got {actual!r}"
print("fixture matches expected output")
