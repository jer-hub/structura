# 04: The Queue Canals

**What to build:** A playable Zone teaching queues. Students see a horizontal line with the front and back marked and an Output row. Enqueue slides the next Tray value in at the back, and Dequeue slides the front value out to the Output row. Puzzles deliberately contrast with The Stack Towers (same input, order kept). The Zone has a Lesson, Puzzles (launch the boats, who's first, same order out, canal log, keep two afloat) and the Lock Keeper Boss, whose Disruption opens the gate early and sweeps the front value out. (An earlier draft enqueued an extra value at the back instead. That could make the Boss unwinnable, so the draft was changed. The random-play check from ticket 02 guards against this.)

**Blocked by:** 03 (The Stack Towers, plus answer buttons for quiz Puzzles)

**Status:** ready-for-human

- [x] Queue renderer joins the renderer contract suite; enqueue slides in at the back, dequeue slides out at the front to the Output row
- [x] Enqueue/Dequeue buttons via the same mechanism as Push/Pop; Dequeue disabled when empty
- [x] Quiz Puzzles reuse the answer UI; a wrong answer explains FIFO
- [x] Zone file for The Queue Canals (unlocked after The Stack Towers) passes the content contract, including the Lock Keeper's Disruption firing
- [x] Play-through test for the Zone passes to 3 Stars
- [ ] Launched and playable by hand
