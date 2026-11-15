"""Bounded conversation memory: worked example with checks.

Label: local teaching fixture, not a real chat-model memory implementation

Prerequisites: Python 3 standard library and a local checkout. The local
fixture is mandatory; any optional real-service extension needs separately
supplied credentials/hardware and is not part of this task.

Run from this directory:

    python3 example.py

This module is not ARIMA and does no forecasting. It keeps at most three
string records, oldest first, and returns a shallow copy to callers.
"""

CAPACITY = 3


class BoundedMemory:
    """Store at most CAPACITY records in arrival order (oldest first)."""

    def __init__(self):
        self._records = []

    def add(self, record):
        """Append a record and evict the oldest one if over capacity."""
        self._records.append(record)
        if len(self._records) > CAPACITY:
            del self._records[0]

    def records(self):
        """Return a shallow copy of the stored records."""
        return list(self._records)


def format_list(items):
    """Render a list as [A,B,C] with no spaces, matching the lab README."""
    return "[" + ",".join(items) + "]"


def main():
    memory = BoundedMemory()
    for record in ["A", "B", "C", "D"]:
        memory.add(record)
        print("add {} -> {}".format(record, format_list(memory.records())))

    returned = memory.records()
    returned.append("X")
    returned.remove("B")
    returned.clear()
    print("mutate returned list -> copy {}".format(format_list(returned)))
    print("stored memory -> {}".format(format_list(memory.records())))


if __name__ == "__main__":
    main()
