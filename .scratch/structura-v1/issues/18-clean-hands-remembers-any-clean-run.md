# 18: Clean Hands is earned by any clean run, not only the best-scoring one

**What to build:** A student who finishes a Challenge or Boss Puzzle with no Glitches and no Hints earns Clean Hands, whatever they scored on other attempts. Today a Puzzle keeps only its best attempt (most stars, then fewest Moves), including that attempt's Glitch and Hint counts. So a clean run that scores fewer stars than an earlier messy run is forgotten, and Clean Hands stays dimmed. The fix is for each Puzzle's saved result to also remember whether it has ever been finished clean. The best attempt's stars, Moves and the Progress Report stay exactly as they are now.

Save files already on lab PCs must keep working. The schema is created with `CREATE TABLE IF NOT EXISTS`, so a new column won't appear in an existing database by itself; opening an old save file has to add it. Old results count as clean only if their stored best attempt was clean.

**Blocked by:** None (can start immediately)

**Status:** ready-for-agent

- [ ] Store test: a clean run recorded after a higher-scoring messy run is remembered as clean, and the best attempt's stars, Moves, Glitches and Hints are unchanged
- [ ] Store test: a messy run recorded after a clean run doesn't make the Puzzle forget it was finished clean
- [ ] Store test: a save file created before this change opens without error, and its results count as clean only if their stored best attempt was clean
- [ ] Achievement test: Clean Hands is earned from that "ever finished clean" record, on a Challenge or Boss Puzzle only
- [ ] UI test driven by real pygame events: finish a Challenge Puzzle with one Glitch (two stars), then again cleanly but with enough extra Moves to score one star; the Achievements screen shows Clean Hands earned. Glitches count against stars (`stars_for`), so a messy run can't score three, but it can beat a clean, wandering run.

## Comments

- Found during ticket 10's code review. See that ticket's comments.
