# 09: Watch Reference Solution

**What to build:** After finishing a Puzzle, students can press "Watch Reference Solution" on the Results screen to see an efficient solution play out on the board. The replay starts from the Puzzle's starting state and applies the Reference Solution's Moves one at a time at the Profile's animation speed, with Disruptions firing and announced exactly as in play. The Code Mirror follows along. Player input is disabled during the replay, and the student can leave at any time. A replay never records a result.

**Blocked by:** None (can start immediately)

**Status:** ready-for-agent

- [ ] Results screen offers "Watch Reference Solution"
- [ ] Replay mode applies Reference Solution Moves on a timer, using the same renderer and effects as play
- [ ] Clicks on the board and Swap/Undo/Hint are ignored or hidden during replay; a Leave button returns to Results or the Zone
- [ ] Disruptions fire at the same points as in the Reference Solution, and the announcement appears
- [ ] A replay does not change stored results (test)
- [ ] UI test: finish an Array Plains Puzzle, watch the replay to completion, and the board ends solved
