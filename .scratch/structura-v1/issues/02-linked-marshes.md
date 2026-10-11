# 02: The Linked Marshes

**What to build:** A playable Zone teaching singly linked lists. Students see nodes joined by arrows from a head pointer. They trace by clicking nodes from the head, insert at the head or after a node by clicking a slot (using the Tray value), and delete by selecting a node and pressing Delete. Arrows visibly re-route on insert and delete, and a "cur" marker walks the list during traversal Steps. The Zone has a Lesson, Guided and Challenge Puzzles (traverse, insert at head, mend a missing node, cut a corrupted node, search, reassemble without swaps) and the Marsh Hydra Boss, whose Disruption spawns a rotten node.

**Blocked by:** 01 (Shared renderer contract and play-through helper)

**Status:** ready-for-agent

- [ ] Linked list renderer joins the renderer contract suite and passes it
- [ ] Click contract: nodes keyed by position; slots keyed "head" and "after position i", shown only when an insert op is allowed and the Tray is not empty
- [ ] Insert and delete animate arrow re-routing; traversal and walk Steps highlight the current node
- [ ] Delete button enabled only with exactly one node selected
- [ ] Zone file for The Linked Marshes (unlocked after The Array Plains) passes the content contract: every Reference Solution finishes, the Hydra's Disruption fires, Hints pass lint, snippets exist in Python and Java
- [ ] Content contract gains a random-play check for every Puzzle with Disruptions: across many seeded random sequences of legal Moves, after each Disruption fires, the Puzzle still has a Reference Solution (no Disruption can make a Puzzle unwinnable, spec story 35)
- [ ] Play-through test: open the Zone, finish the Lesson, play every Puzzle via the click contract to 3 Stars, results saved
- [ ] Launched and playable by hand
