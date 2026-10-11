"""Big-O of each operation per structure. This table is how Select Puzzles get
their Reference Solution (ADR 0001): the answer is computed, never typed in.

A scenario weights how often each operation happens. The best structure has the
lowest weighted cost. Ties go to the structure with fewer capabilities, because
the most restrictive structure that still does the job states intent best
(a stack says "LIFO only" where an array says "anything goes").
"""
from __future__ import annotations

OPERATIONS = {
    "access_index": "read the item at a position",
    "search": "find a value",
    "add_front": "add at the front",
    "add_back": "add at the back",
    "remove_front": "remove from the front",
    "remove_back": "remove from the back",
}

# Stack's "back" is its top. Queue adds at the back and removes from the front.
TABLE: dict[str, dict[str, str]] = {
    "array": {"access_index": "O(1)", "search": "O(n)", "add_front": "O(n)", "add_back": "O(1)",
              "remove_front": "O(n)", "remove_back": "O(1)"},
    "linked_list": {"access_index": "O(n)", "search": "O(n)", "add_front": "O(1)", "add_back": "O(1)",
                    "remove_front": "O(1)", "remove_back": "O(n)"},
    "stack": {"add_back": "O(1)", "remove_back": "O(1)"},
    "queue": {"add_back": "O(1)", "remove_front": "O(1)"},
}

RANK = {"O(1)": 1, "O(log n)": 2, "O(n)": 3, "O(n log n)": 4}


def cost(structure: str, scenario: dict[str, int]) -> float:
    row = TABLE[structure]
    total = 0.0
    for op, weight in scenario.items():
        if weight <= 0:
            continue
        if op not in row:
            return float("inf")
        total += weight * RANK[row[op]]
    return total


def ranking(choices: list[str], scenario: dict[str, int]) -> list[str]:
    return sorted(choices, key=lambda s: (cost(s, scenario), len(TABLE[s])))


def best(choices: list[str], scenario: dict[str, int]) -> str:
    """The single best structure. Raises if the scenario can't separate the top two."""
    ranked = ranking(choices, scenario)
    a, b = ranked[0], ranked[1]
    if (cost(a, scenario), len(TABLE[a])) == (cost(b, scenario), len(TABLE[b])):
        raise ValueError(f"scenario ties {a} and {b}; adjust the weights")
    if cost(a, scenario) == float("inf"):
        raise ValueError("no choice supports every operation in the scenario")
    return a


def explain(chosen: str, correct: str, scenario: dict[str, int]) -> str:
    """Why `chosen` loses to `correct`, naming the most damning operation."""
    from . import DISPLAY_NAMES as names

    row_c, row_k = TABLE[chosen], TABLE[correct]
    used = [op for op, w in sorted(scenario.items(), key=lambda kv: -kv[1]) if w > 0]
    for op in used:
        if op not in row_c:
            return f"A {names[chosen]} can't {OPERATIONS[op]} at all."
    for op in used:
        if RANK[row_c[op]] > RANK[row_k[op]]:
            return (f"To {OPERATIONS[op]}, a {names[chosen]} takes {row_c[op]} "
                    f"but a {names[correct]} takes {row_k[op]}.")
    return (f"A {names[chosen]} works, but a {names[correct]} does the same job with fewer "
            f"operations to misuse.")
