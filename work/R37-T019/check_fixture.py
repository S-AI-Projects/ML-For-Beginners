import json
import sys
from pathlib import Path

base = Path(__file__).parent
expected = json.loads((base / "expected.json").read_text())
actual_path = Path(sys.argv[1]) if len(sys.argv) > 1 else base / "actual.json"
actual = json.loads(actual_path.read_text())
assert actual["checked"] == 3, f"expected 3 checked rows, got {actual['checked']}"
statuses = [row["status"] for row in actual["outcomes"]]
assert statuses == expected["size_3"], f"expected {expected['size_3']}, got {statuses}"
print("fixture assertions passed")
