# 03: The Stack Towers, plus answer buttons for quiz Puzzles

**What to build:** A playable Zone teaching stacks, plus the generic answer UI that every quiz-style Trace Puzzle will reuse. Students see a vertical tower with the top marked and an Output row of popped values. Push takes the next Tray value onto the top, and Pop moves the top to the Output row. Quiz Puzzles show an operation script and a few option buttons. A wrong option is a Glitch that explains the misconception (for stacks: LIFO), and the right option finishes the Puzzle. The Zone has a Lesson, Puzzles (stack the blocks, top of the tower, mirror spell, what falls out, the juggler) and the Tower of Echoes Boss.

**Blocked by:** 01 (Shared renderer contract and play-through helper)

**Status:** ready-for-agent

- [ ] Stack renderer joins the renderer contract suite; pushes drop in from above and pops lift off to the Output row
- [ ] Push/Pop buttons appear only when those ops are allowed; Pop is disabled on an empty stack
- [ ] Quiz answer UI: one button per option labelled with the option text; wrong choice shows the goal's explanation as a Glitch; right choice finishes the Puzzle
- [ ] Click contract registered for stack Moves (buttons) and answer Moves (option labels)
- [ ] Zone file for The Stack Towers (unlocked after The Linked Marshes) passes the content contract
- [ ] Play-through test for the Zone passes to 3 Stars, including at least one quiz Puzzle
- [ ] A session-level test covers a wrong then right answer (Glitch counted, Puzzle finished)
- [ ] Launched and playable by hand
