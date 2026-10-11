# 07: The Binary Forest, part 2 (rotations and the Colossus)

**What to build:** Rotations that make balancing concrete. Students select a node and press Rotate Left or Rotate Right, and the affected nodes travel along arcs to their new places while edges follow. Two Optimize Puzzles teach a single rotation and a double (left-right) rotation. The Unbalanced Colossus Boss asks students to rebalance a tree that grew in a straight line, and its Disruption grows two new branches midway. Done means the tree satisfies the AVL rule, and the Reference Solution comes from fixing the deepest violation first.

**Blocked by:** 06 (The Binary Forest, part 1)

**Status:** ready-for-agent

- [ ] Rotate Left/Right buttons enabled only with one node selected that has the needed child; otherwise they are disabled, or the Move is a Glitch with the model's explanation
- [ ] Rotation animation moves nodes along arcs, not straight lines (structure-specific motion test)
- [ ] Optimize Puzzles "Lopsided Sapling" and "Zig-Zag" and the Colossus Boss added to the Zone file and pass the content contract, including the Disruption firing
- [ ] The Zone's play-through test covers all Puzzles, Boss included, to 3 Stars
- [ ] Launched and playable by hand
