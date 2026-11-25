import json
from pathlib import Path

base = Path(__file__).parent
expected = json.loads((base / "expected.json").read_text())
for size in (1, 2, 3):
    path = base / (f"size_{size}.json" if size < 3 else "actual.json")
    actual = json.loads(path.read_text())
    statuses = [row["status"] for row in actual["outcomes"]]
    wanted = expected[f"size_{size}"]
    assert actual["checked"] == size, (size, actual["checked"])
    assert statuses == wanted, (size, wanted, statuses)
print("all three input-size assertions passed")
