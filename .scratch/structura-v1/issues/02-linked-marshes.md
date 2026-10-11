# 02: The Linked Marshes

**What to build:** A playable Zone teaching singly linked lists. Students see nodes joined by arrows from a head pointer. They trace by clicking nodes from the head, insert at the head or after a node by clicking a slot (using the Tray value), and delete by selecting a node and pressing Delete. Arrows visibly re-route on insert and delete, and a "cur" marker walks the list during traversal Steps. The Zone has a Lesson, Guided and Challenge Puzzles (traverse, insert at head, mend a missing node, cut a corrupted node, search, reassemble without swaps) and the Marsh Hydra Boss, whose Disruption spawns a rotten node.

**Blocked by:** 01 (Shared renderer contract and play-through helper)

**Status:** ready-for-human

- [x] Linked list renderer joins the renderer contract suite and passes it
- [x] Click contract: nodes keyed by position; slots keyed "head" and "after position i", shown only when an insert op is allowed and the Tray is not empty
- [x] Insert and delete animate arrow re-routing; traversal and walk Steps highlight the current node
- [x] Delete button enabled only with exactly one node selected
- [x] Zone file for The Linked Marshes (unlocked after The Array Plains) passes the content contract: every Reference Solution finishes, the Hydra's Disruption fires, Hints pass lint, snippets exist in Python and Java
- [x] Content contract gains a random-play check for every Puzzle with Disruptions: across many seeded random sequences of legal Moves, whenever the Puzzle was winnable right after the player's Move, it is still winnable after the Disruption fires (no Disruption can make a Puzzle unwinnable, spec story 35). Measure between the Move and the Disruption, not before the Move, or the player's own dead ends get blamed on the Disruption
- [x] Dead-end prompt: when no Reference Solution exists from the current state (e.g. the player deleted a value the Tray can't replace; random play hits this in about two thirds of Marsh Hydra runs), the game says the Puzzle can no longer be finished and suggests Undo, and the third Hint tier says "Undo" instead of offering a Move. Session-level test plus a UI test
- [x] Play-through test: open the Zone, finish the Lesson, play every Puzzle via the click contract to 3 Stars, results saved
- [~] Launched and playable by hand

## Comments

Implemented. Waiting on the one human step: launch the game (`.venv/Scripts/python main.py`) and play The Linked Marshes by hand. Headless screenshots of the Lesson and the Marsh Hydra looked right.

- Renderer: `ui/renderers/linked_list.py`. Slots are keyed `"head"` and i ("after position i") and filtered by the Puzzle's ops. While a deleted node fades, the arrow that skips it bows over it. A `cur` marker follows walk Steps.
- Dead ends: `PuzzleSession.dead_end` is true when no Reference Solution exists from the current state. The scene then shows the Undo prompt, keeping any Disruption announcement next to it. In a dead end, Hints say Undo at every tier and aren't charged, because the prompt is already on screen.
- Random-play check: `test_disruptions_never_make_a_winnable_puzzle_unwinnable` in `tests/test_content.py`. Across 40 seeds the Hydra is checked in about 15 runs; the other 25 are the player's own dead ends.
- Known rough edge: when a Move and a Disruption land on the same frame, the board animates both at once, so the spawned node briefly overlaps a sliding node. The Array Plains boss does the same. Could be sequenced in a later polish pass.
