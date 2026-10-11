# 03: The Stack Towers, plus answer buttons for quiz Puzzles

**What to build:** A playable Zone teaching stacks, plus the generic answer UI that every quiz-style Trace Puzzle will reuse. Students see a vertical tower with the top marked and an Output row of popped values. Push takes the next Tray value onto the top, and Pop moves the top to the Output row. Quiz Puzzles show an operation script and a few option buttons. A wrong option is a Glitch that explains the misconception (for stacks: LIFO), and the right option finishes the Puzzle. The Zone has a Lesson, Puzzles (stack the blocks, top of the tower, mirror spell, what falls out, the juggler) and the Tower of Echoes Boss.

**Blocked by:** 01 (Shared renderer contract and play-through helper)

**Status:** ready-for-human

- [x] Stack renderer joins the renderer contract suite; pushes drop in from above and pops lift off to the Output row
- [x] Push/Pop buttons appear only when those ops are allowed; Pop is disabled on an empty stack
- [x] Quiz answer UI: one button per option labelled with the option text; wrong choice shows the goal's explanation as a Glitch; right choice finishes the Puzzle
- [x] Click contract registered for stack Moves (buttons) and answer Moves (option labels)
- [x] Zone file for The Stack Towers (unlocked after The Linked Marshes) passes the content contract
- [x] Play-through test for the Zone passes to 3 Stars, including at least one quiz Puzzle
- [x] A session-level test covers a wrong then right answer (Glitch counted, Puzzle finished)
- [~] Launched and playable by hand

## Comments

Implemented. Waiting on the one human step: launch the game and play The Stack Towers by hand. Headless screenshots of the tower, a pop in flight and the quiz screen looked right.

- Renderer: `ui/renderers/stack.py`. The base gained `enter`/`leave` hooks (defaults: grow in place, fade out as a ghost). The stack drops pushed blocks in from above and flies popped ones to the Output row. Undoing a pop removes the value from the Output; the block drops back in from above. The renderer contract now checks "animates in" and "animates out". Arrays and linked lists keep their pop-in check in their own structure-specific tests.
- Fixed in passing: models change in place, so the values of removed elements are now remembered from the last sync. Ghosts and popped blocks had been drawn without their values.
- Buttons: `BUTTON_OPS` in the Puzzle scene (push/pop/enqueue/dequeue), shown only for the Puzzle's ops. A remove op is enabled only when the model allows it.
- Answer UI: any goal with `options` gets one button per option inside the board, and `Goal.question()` lines are shown in place of the board. Fits 4 options (2×2). Ticket 05 still needs to add the Big-O table for Select Puzzles.
- Open content question for faculty: the briefs of z3_p2 and z3_p4 restate their scripts, which `goal.script` already holds (same fact in two places, see ADR 0001). "Output" is now in CONTEXT.md.
