# 05: Nexus Alpha

**What to build:** The comparison Zone where students choose the right structure for a job. Select Puzzles describe a real scenario (undo history, ticket line, seat lookups, news feed) and offer Array, Linked List, Stack and Queue as answer buttons. The correct answer is computed from the Big-O table (ADR 0001), never written by hand. A wrong choice is a Glitch naming the operation that costs too much on that structure versus the right one. During Select Puzzles the Code Mirror area shows the Big-O table for the choices. The Zone also has a mixed-structure quiz (a queue script where students may assume stack behaviour) and the Entropy Serpent Boss, sorting an array it scrambles twice.

**Blocked by:** 04 (The Queue Canals)

**Status:** ready-for-human

- [x] Select Puzzles reuse the answer UI with options labelled by structure display names
- [x] Wrong-choice explanations come from the complexity table and name a specific operation and its Big-O on both structures
- [x] The Code Mirror panel shows a Big-O table for the Puzzle's choices during Select Puzzles (in either language setting)
- [x] The Zone uses the structure each Puzzle declares (array, queue), not just the Zone default
- [x] Zone file for Nexus Alpha (unlocked after The Queue Canals) passes the content contract; every Select scenario has a unique best answer
- [x] Play-through test for the Zone passes to 3 Stars, including the Serpent's two Disruptions
- [ ] Launched and playable by hand
