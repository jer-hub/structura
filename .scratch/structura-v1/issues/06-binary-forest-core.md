# 06: The Binary Forest, part 1 (insert, search, delete, traversals)

**What to build:** A playable Zone teaching binary search trees, without rotations yet. Students see the tree laid out with left and right children joined by edges. They insert by clicking the empty spot where the next Tray value belongs, and a wrong spot is a Glitch explaining the comparison at the node where they went the wrong way. Searches are traced by clicking nodes in comparison order. Deletion covers a leaf, a node with one child, and a node with two children. For two children, after pressing Delete the student is prompted to click the node that replaces it, and only the in-order successor or predecessor is accepted. Pre-, in- and post-order Trace Puzzles and a pre-order prediction quiz complete the set. The Zone ships with its Lesson and Puzzles 1–6 and 9 from the draft (no Boss yet; that arrives in ticket 07).

**Blocked by:** 01 (Shared renderer contract and play-through helper), 03 (The Stack Towers, plus answer buttons for quiz Puzzles)

**Status:** done

- [x] BST renderer joins the renderer contract suite; layout uses in-order position for x and depth for y, with edges
- [x] Click contract: nodes keyed by value; empty-child slots keyed by (parent value, side); the root slot keyed by (none)
- [x] Insertion animates the comparison path before the new node pops in
- [x] Two-children deletion runs as a two-click interaction (select, Delete, then click the replacement); any other replacement is a Glitch with the successor explanation
- [x] Traversal and search Trace Puzzles are Strict; wrong clicks explain the traversal rule
- [x] Zone file for The Binary Forest (unlocked after Nexus Alpha) passes the content contract
- [x] Play-through test for the Zone's current Puzzles passes to 3 Stars
- [x] Launched and playable by hand

## Comments

- Renderer: `src/structura/ui/renderers/bst.py`. Columns alternate gap, node, gap: a tree of n nodes has n + 1 empty child spots, one in each in-order gap, so a "+" slot sits one level below its parent and never overlaps a node. The root slot is keyed `(None, "")`, the same as the model's `empty_slots()`. The "+" badge is now shared with the linked list (`draw_badge` in `renderers/base.py`).
- Motion: a new node stays hidden while its insert's comparison path plays and grows in at the "place" Step. After a delete, the old tree stays on the board (so the path and the successor light up on it) until the Step that removes the node. Both happen at once when no Steps are playing, and the starting tree always appears at once. The Lesson now syncs the board after every Move, so each insert in a beat gets its own comparison path.
- Two-children delete: select, Delete, then click the replacement; clicking the same node again cancels. The scene asks the model (`needs_replacement`, `delete_move`) instead of checking for "bst". The successor and the predecessor both finish the Puzzle: Script goals now accept every textbook way to run a line (`Model.alternatives`), so the predecessor isn't a dead end. Any other node is a Glitch with the successor explanation. A third-tier Hint points at the replacement; a Hint about a different Move cancels the pending delete. Undo now drops the Steps still queued for the undone Move.
- Content (asked and agreed 2026-10-15): the draft had no one-child deletion and no post-order trace, which spec stories 63 and 65 ask for, so two Puzzles were added in the draft's style: `z5_p10` "Splice the Branch" (delete 10, which has one child) and `z5_p11` "Fallen Leaves" (post-order). A content test pins all three deletion cases and all three traversal orders. The Heart of the Tree brief no longer states "it has two children" by hand (ADR 0001); the game says so when Delete is pressed. Ids p7, p8 and `z5_boss` stay reserved for ticket 07; the draft stays in `.scratch` for it.
- Checked by headless renders: Plant the Seeds with slots, the 9-node search tree, the replacement prompt, and the Lesson mid-insert. **Still to do by hand:** play The Binary Forest in a real window (Lesson, then every Puzzle, including a wrong insert spot, a wrong replacement, and the predecessor as replacement). Tick the box and set Status to done.
- 2026-10-15: the faculty owner played The Binary Forest by hand and confirmed it is good. Ticket closed; 07 is unblocked.
- Not changed: the Code Mirror's delete snippet only shows the successor loop, so a student who picks the predecessor sees successor lines highlighted. Small labels on ticket 07's 9-node Boss chains (about 28 px nodes) should be checked by eye when that ticket lands.
