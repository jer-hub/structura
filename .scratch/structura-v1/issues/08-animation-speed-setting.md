# 08: Animation speed setting

**What to build:** Students choose how fast animations play (0.5x, 1x or 2x) from the Zone Map, beside the Code Mirror language toggle. The choice is saved to their Profile and applies to Lesson animations, Puzzle Step playback and element motion. It also applies to the Reference Solution replay once ticket 09 exists.

**Blocked by:** None (can start immediately)

**Status:** ready-for-agent

- [ ] A speed control on the Zone Map cycles through or selects 0.5x / 1x / 2x and shows the current value
- [ ] The setting persists on the Profile across restarts (store round-trip test)
- [ ] Step playback duration and element travel time scale with the setting (test at 2x finishes in roughly half the time of 1x)
- [ ] UI test: change the speed, open a Puzzle, and the scene uses the new speed
