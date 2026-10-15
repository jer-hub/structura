# 09: Watch Reference Solution

**What to build:** After finishing a Puzzle, students can press "Watch Reference Solution" on the Results screen to see an efficient solution play out on the board. The replay starts from the Puzzle's starting state and applies the Reference Solution's Moves one at a time at the Profile's animation speed, with Disruptions firing and announced exactly as in play. The Code Mirror follows along. Player input is disabled during the replay, and the student can leave at any time. A replay never records a result.

**Blocked by:** None (can start immediately)

**Status:** done

- [x] Results screen offers "Watch Reference Solution"
- [x] Replay mode applies Reference Solution Moves on a timer, using the same renderer and effects as play
- [x] Clicks on the board and Swap/Undo/Hint are ignored or hidden during replay; a Leave button returns to Results or the Zone
- [x] Disruptions fire at the same points as in the Reference Solution, and the announcement appears
- [x] A replay does not change stored results (test)
- [x] UI test: finish an Array Plains Puzzle, watch the replay to completion, and the board ends solved

## Comments

Done. `ReplayScene` (in `ui/scenes/replay.py`) is the Puzzle scene with input switched off. It plays its own queue of the Reference Solution's Moves through the normal Move path, so the board, effects, Code Mirror and Disruption announcements match play exactly. It shows only "Leave Replay", which becomes "Back to Results" at the end. Quiz and select answers stay visible but disabled, and the right one is marked at the end. Leaving returns to the *same* Results scene, because making a new one would record another attempt.

Pacing: one beat (`BEAT / speed`) after the previous Move's Steps finish. This is a deliberate exception to "animations must never delay game state". The replay exists to be watched, so the next Move waits for the last one to finish playing. Play itself is unaffected.

Tests (UI seam): the replay ends solved and records nothing; input is ignored and Leave works partway; each Disruption is announced after the same Move as in play; a quiz replay marks the right answer; and the replay finishes in about half the time at 2x. Only the first test was written red-first; the rest came after the code. There's no PuzzleSession-level test because the replay adds no session rule; it feeds Reference Moves through `try_move` like a player.
