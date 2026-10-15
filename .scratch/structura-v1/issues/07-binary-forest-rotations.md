# 07: The Binary Forest, part 2 (rotations and the Colossus)

**What to build:** Rotations that make balancing concrete. Students select a node and press Rotate Left or Rotate Right, and the affected nodes travel along arcs to their new places while edges follow. Two Optimize Puzzles teach a single rotation and a double (left-right) rotation. The Unbalanced Colossus Boss asks students to rebalance a tree that grew in a straight line, and its Disruption grows two new branches midway. Done means the tree satisfies the AVL rule, and the Reference Solution comes from fixing the deepest violation first.

**Blocked by:** 06 (The Binary Forest, part 1)

**Status:** ready-for-human

- [x] Rotate Left/Right buttons enabled only with one node selected that has the needed child; otherwise they are disabled, or the Move is a Glitch with the model's explanation
- [x] Rotation animation moves nodes along arcs, not straight lines (structure-specific motion test)
- [x] Optimize Puzzles "Lopsided Sapling" and "Zig-Zag" and the Colossus Boss added to the Zone file and pass the content contract, including the Disruption firing
- [x] The Zone's play-through test covers all Puzzles, Boss included, to 3 Stars
- [ ] Launched and playable by hand

## Comments

- **Rotations:** select one node, then press Rotate Left or Rotate Right. The buttons are enabled only when the model says the rotation is legal, so the rule lives in one place (ADR 0001). Hints, the Glitch shake and the click contract all cover rotations too.
- **Arcs:** in a rotation, nodes going up and nodes going down bow sideways, away from each other, like a wheel turning. Edges follow the nodes. Inserts and deletes still move in straight lines, and each has its own test.
- **The Colossus Disruption fires after Move 2, not 3 as drafted.** Three rotations are enough to balance the Colossus, so with `after = 3` a quick player won the Boss before it fired. A new content-contract test searches every Boss for a win before its first Disruption. The search stops at the first Disruption, because going further is too slow for the swap Bosses. Par is now 10 Moves, including the two inserts.
- **The Boss brief is shorter than the draft's**, so it fits the Puzzle screen's single brief line. A new test checks every brief's width.
- **The Zone page now flows (your choice):** cards run in unlock order down the columns, a Stage heading sits where each Stage starts, and three narrower columns are used only when two won't fit. Only the Forest needs three. Text too long for a card is shortened with "…". Locked cards lead with "Finish X first", so the unlock hint is never the part that gets cut.
- **To check by hand:** play through the Forest, watch a rotation and the Colossus Disruption, and look at the three-column Zone page.
