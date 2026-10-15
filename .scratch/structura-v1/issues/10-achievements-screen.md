# 10: Achievements screen

**What to build:** A screen reachable from the Zone Map that lists every Achievement with its title and requirement, showing earned ones lit and the rest dimmed. Achievements are derived from results each time (nothing new is stored): First Repair, Clean Hands, Boss Breaker, Persistence, and one "Master of <Zone>" per Zone, so new Zones add their own automatically.

**Blocked by:** None (can start immediately)

**Status:** done

- [x] Zone Map has an Achievements button; the screen has a Back button to the Zone Map
- [x] Earned and unearned Achievements are visually distinct
- [x] Achievement evaluation tests cover each rule (earned and not earned)
- [x] UI test: a fresh Profile shows none earned; after finishing one Puzzle, First Repair shows as earned

## Comments

- New `AchievementsScene` (`ui/scenes/achievements.py`), opened by an "Achievements" button on the Zone Map. Earned cards have a green edge, a lit star and bold title text; unearned cards are dimmed. Cards are laid out in two columns and shrink to fit above the Back button, so the dozen Zones the spec plans for (about 16 Achievements) still fit on screen.
- Rule decisions (from the user):
  - Clean Hands counts Challenge and Boss Puzzles. Its description now reads "Finish a Challenge or Boss Puzzle with no Glitches and no Hints."
  - Persistence keeps counting finished runs. Its description now reads "Finish the same Puzzle three times."
- The rule tests in `tests/test_achievements.py` describe rules that already existed, so they passed on first run. The UI, layout and description tests were red first.
- **Known gap, not fixed here:** Clean Hands can miss a clean run. `store.record` keeps Glitch and Hint counts only from the best attempt, so a clean run that scores fewer stars than an earlier messy one is forgotten. Fixing it needs a stored flag (e.g. "ever finished clean"), which changes the schema. This needs its own ticket.
