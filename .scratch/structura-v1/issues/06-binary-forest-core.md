# 06: The Binary Forest, part 1 (insert, search, delete, traversals)

**What to build:** A playable Zone teaching binary search trees, without rotations yet. Students see the tree laid out with left and right children joined by edges. They insert by clicking the empty spot where the next Tray value belongs, and a wrong spot is a Glitch explaining the comparison at the node where they went the wrong way. Searches are traced by clicking nodes in comparison order. Deletion covers a leaf, a node with one child, and a node with two children. For two children, after pressing Delete the student is prompted to click the node that replaces it, and only the in-order successor or predecessor is accepted. Pre-, in- and post-order Trace Puzzles and a pre-order prediction quiz complete the set. The Zone ships with its Lesson and Puzzles 1–6 and 9 from the draft (no Boss yet; that arrives in ticket 07).

**Blocked by:** 01 (Shared renderer contract and play-through helper), 03 (The Stack Towers, plus answer buttons for quiz Puzzles)

**Status:** ready-for-agent

- [ ] BST renderer joins the renderer contract suite; layout uses in-order position for x and depth for y, with edges
- [ ] Click contract: nodes keyed by value; empty-child slots keyed by (parent value, side); the root slot keyed by (none)
- [ ] Insertion animates the comparison path before the new node pops in
- [ ] Two-children deletion runs as a two-click interaction (select, Delete, then click the replacement); any other replacement is a Glitch with the successor explanation
- [ ] Traversal and search Trace Puzzles are Strict; wrong clicks explain the traversal rule
- [ ] Zone file for The Binary Forest (unlocked after Nexus Alpha) passes the content contract
- [ ] Play-through test for the Zone's current Puzzles passes to 3 Stars
- [ ] Launched and playable by hand
