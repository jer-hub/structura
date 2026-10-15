# 08: Animation speed setting

**What to build:** Students choose how fast animations play (0.5x, 1x or 2x) from the Zone Map, beside the Code Mirror language toggle. The choice is saved to their Profile and applies to Lesson animations, Puzzle Step playback and element motion. It also applies to the Reference Solution replay once ticket 09 exists.

**Blocked by:** None (can start immediately)

**Status:** done

- [x] A speed control on the Zone Map cycles through or selects 0.5x / 1x / 2x and shows the current value
- [x] The setting persists on the Profile across restarts (store round-trip test)
- [x] Step playback duration and element travel time scale with the setting (test at 2x finishes in roughly half the time of 1x)
- [x] UI test: change the speed, open a Puzzle, and the scene uses the new speed

## Comments

Done. A "Speed: 1x" button beside the Code Mirror language toggle cycles 1x, 2x, 0.5x and saves to the Profile. The store already had the column, and the round-trip is tested by reopening the database after clicking. Renderers have a `speed` set when they are made (`make_renderer(structure, rect, speed)`). It scales element motion only: travel, pop-in, fade-out, the celebration wave, Output-row flyers and the linked-list `cur` marker. Highlight and hint pulses, Glitch shakes, the board shake, particles and the scene fade stay at real time, so feedback feels the same at every speed. Step playback already used the Profile speed.

Tests: Zone Map cycling and saving, a Puzzle and a Lesson each animating in about half the time at 2x, and a renderer-contract test that 0.5x slows motion but not Glitch shakes. `tests/clicks.py` gained `perform`, which makes a Move without waiting for its animation, for timing tests. For ticket 09, a replay scene gets the speed by passing `app.profile.speed` to both `StepPlayer` and `make_renderer`.
