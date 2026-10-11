# Spec: Structura v1 (Array Plains to Binary Forest)

Status: ready-for-agent

## Problem Statement

BSIT students meet data structures and algorithms as text and static diagrams. They can recite that a stack is LIFO or that binary search is O(log n), but they struggle to *trace* an algorithm step by step, to predict how a structure changes, or to choose the right structure for a job. Instructors have no low-effort way to give students hands-on practice between lectures and see who actually did it.

The course teaches both Java and Python, so practice material tied to one language leaves half the class translating. Students have phones and PCs, but practice tools that need accounts, servers or installs with admin rights are hard to roll out in school labs.

A thin playable slice already exists: Profile, Zone Map, The Array Plains (a Lesson and four Puzzles), Results, Progress Report export, and in-game animations. The faculty owner played it and confirmed it "feels right". This spec covers taking that slice to the full v1 curriculum and making it something an instructor can hand to a class.

## Solution

Structura is a desktop game. Students repair a corrupted "Datasphere" by manipulating data structures directly. Each **Zone** teaches one structure through a **Lesson** followed by **Puzzles**, and ends in a **Boss**. Every Move is checked by the game's own data structure code, which also produces the **Reference Solution** used for **Strict Puzzles**, Hints and **Stars** (ADR 0001). A **Code Mirror** panel shows the matching Python or Java code executing in sync with the player's Moves (ADR 0002).

Players cannot fail. Wrong Moves are **Glitches** with an explanation, and Stars reward efficiency. Students keep a local **Profile** (name and student ID, no password) on any PC, including shared lab machines. They export a signed **Progress Report** to attach to a Google Classroom assignment. Instructors combine a class's reports into one spreadsheet.

v1 ships, in order on the **Zone Map**: The Array Plains (done), The Linked Marshes, The Stack Towers, The Queue Canals, **Nexus Alpha** (comparing structures), and The Binary Forest (BSTs and AVL rotations). It is distributed as a Windows executable that runs without installing.

## User Stories

### Getting started
1. As a student, I want to create a Profile with just my name and student ID, so that I can start playing without an account or password.
2. As a student on a shared lab PC, I want to pick my Profile from a list of several, so that my progress doesn't mix with my classmates'.
3. As a student, I want to choose Python or Java for the Code Mirror when I create my Profile, so that the code I see matches the language I'm studying.
4. As a student, I want to switch the Code Mirror language later from the Zone Map, so that I can compare how the same operation looks in both languages.
5. As a student, I want to be told clearly when my name or student ID is missing, so that I don't create a broken Profile.
6. As a student, I want to switch Profiles from the Zone Map, so that a classmate can take the PC after me.

### Zone Map and progression
7. As a student, I want to see every Zone on a map with the paths between them, so that I understand how topics build on each other.
8. As a student, I want locked Zones to show as locked, so that I know what I have to finish first.
9. As a student, I want each Zone to show my Stars out of the total possible, so that I can see where I could improve.
10. As a student, I want The Linked Marshes to unlock once I finish The Array Plains, so that I meet structures in a sensible order.
11. As a student, I want The Stack Towers to unlock after The Linked Marshes, and The Queue Canals after The Stack Towers, so that the linear structures come one at a time.
12. As a student, I want Nexus Alpha to unlock after The Queue Canals, so that I compare structures only once I know them all.
13. As a student, I want The Binary Forest to unlock after Nexus Alpha, so that trees come after the linear structures.
14. As a student, I want a Zone's Puzzles to unlock in order, so that each one builds on the last.
15. As a student, I want to replay any Puzzle I've finished, so that I can try for more Stars.

### Lessons
16. As a student, I want every Zone to open with a short animated Lesson, so that I see how the structure behaves before I'm asked to use it.
17. As a student, I want to step through the Lesson at my own pace with Next, so that I can read each explanation fully.
18. As a student, I want the Code Mirror to highlight the line running during each Lesson animation, so that I connect the picture to the code.
19. As a student, I want to replay a Lesson whenever I like, so that I can refresh my memory before a hard Puzzle.

### Playing Puzzles (all Zones)
20. As a student, I want each Puzzle to state its goal in one or two sentences, so that I know what "finished" means.
21. As a student, I want each Puzzle to show its Puzzle Type and Stage, so that I know whether I'm practising, being challenged, or facing a Boss.
22. As a student, I want a Glitch to explain why my Move was wrong without ending the Puzzle, so that mistakes teach me rather than punish me.
23. As a student, I want Glitches to explain the rule I broke in terms of the actual values (e.g. "6 < 8, so 6 belongs in 8's left subtree"), so that I can fix my thinking.
24. As a student in a Strict Puzzle, I want a Move that is legal but not what the algorithm does next to be a Glitch that names the algorithm's rule, so that I learn the algorithm itself, not just any solution.
25. As a student, I want up to three Hints, from a nudge to the exact next Move highlighted on the board, so that I can get unstuck at whatever level of help I need.
26. As a student, I want Undo, so that I can step back after a Move I regret, knowing the Move still counts toward my score.
27. As a student, I want to see my Moves, Glitches and Hints against the Reference Solution's Move count while I play, so that I know how efficient I'm being.
28. As a student, I want the Tray to show which value I must place next, so that I use values in the required order.
29. As a student, I want the Code Mirror to follow every Move I make, so that I always see the code for what I just did.
30. As a student, I want each structure animated (elements moving, appearing, disappearing, comparisons pulsing), so that I can follow what happened.
31. As a student, I want a celebration when I finish a Puzzle, so that finishing feels rewarding.
32. As a student, I want to leave a Puzzle at any time and come back to it, so that I'm never trapped.

### Boss Puzzles
33. As a student, I want a Boss at the end of each Zone that is longer and combines what the Zone taught, so that I can prove I've mastered it.
34. As a student, I want Disruptions in a Boss to change the structure partway through, with a clear announcement and a board shake, so that I have to adapt instead of following a memorised script.
35. As a student, I want Disruptions to never make a Boss impossible or failable, so that the Boss stays fair.

### The Linked Marshes
36. As a student, I want to see a linked list as nodes joined by arrows from a head pointer, so that I understand it is not stored side by side.
37. As a student, I want to trace a linked list by clicking nodes from the head in order, so that I feel why reaching a node is O(n).
38. As a student, I want to insert at the head and after a chosen node by clicking a slot, so that I learn which pointers change.
39. As a student, I want to delete a node by selecting it and pressing Delete, so that I see the previous node relinked past it.
40. As a student, I want arrows to re-route visibly when I insert or delete, so that the pointer changes are concrete.
41. As a student, I want a Puzzle where I can only add and remove nodes (no swapping), so that I learn what linked lists can't do cheaply.
42. As a student, I want to beat the Marsh Hydra Boss, which spawns a rotten node partway through, so that I apply deletion under pressure.

### The Stack Towers
43. As a student, I want to see a stack as a vertical tower with the top clearly marked, so that LIFO is visible.
44. As a student, I want Push and Pop buttons that take the next Tray value and remove the top, so that I can only use the stack the way a stack allows.
45. As a student, I want to see an Output row of popped values, so that I can reason about the order values come out in.
46. As a student, I want Trace Puzzles that show an operation script and ask me to choose the result from a few options, so that I practise predicting without the board doing it for me.
47. As a student, I want Puzzles that ask me to produce a specific Output order, so that I discover a stack reverses whatever passes through it.
48. As a student, I want to beat the Tower of Echoes Boss, which needs a non-obvious push/pop order, so that I master LIFO.

### The Queue Canals
49. As a student, I want to see a queue as a horizontal line with the front and back clearly marked, so that FIFO is visible.
50. As a student, I want Enqueue and Dequeue buttons, so that I can only use the queue the way a queue allows.
51. As a student, I want Puzzles that contrast with the Stack Towers (same input, order kept), so that I feel the difference between LIFO and FIFO.
52. As a student, I want Trace Puzzles where a wrong answer reminds me of FIFO, so that I correct the specific misconception.
53. As a student, I want to beat the Lock Keeper Boss, where an extra item sneaks into the back, so that I apply FIFO when the plan changes.

### Nexus Alpha
54. As a student, I want Select Puzzles that describe a real scenario (an undo history, a ticket line, seat lookups, a news feed) and ask which structure fits, so that I practise choosing structures.
55. As a student, I want a wrong choice explained by naming the operation that costs too much on my choice (e.g. "To read the item at a position, a Linked List takes O(n) but an Array takes O(1)"), so that I learn the Big-O reasoning, not just the answer.
56. As a student, I want the Code Mirror area to show the Big-O table for the choices during a Select Puzzle, so that I can reason from it.
57. As a student, I want a mixed-structure Trace Puzzle in the Nexus, so that I must notice which structure I'm working with.
58. As a student, I want to beat the Entropy Serpent Boss (sorting an array that it scrambles twice), so that the first half of the course ends on a big challenge.

### The Binary Forest
59. As a student, I want to see a BST laid out as a tree with left and right children, so that the ordering rule is visible.
60. As a student, I want to insert by clicking the empty spot where the next Tray value belongs, so that I practise the left/right decision at every node.
61. As a student, I want a wrong insertion spot explained at the exact node where I went the wrong way, so that I find my mistake.
62. As a student, I want to trace a BST search by clicking nodes in comparison order, so that I learn search follows a single path.
63. As a student, I want to delete a leaf, a node with one child, and a node with two children, so that I learn all three deletion cases.
64. As a student deleting a node with two children, I want to choose its replacement by clicking the in-order successor (or predecessor), so that I learn why only those values keep the tree ordered.
65. As a student, I want pre-order, in-order and post-order Trace Puzzles, so that I can tell the traversals apart.
66. As a student, I want to select a node and press Rotate Left or Rotate Right, with the nodes animating along arcs into their new places, so that rotations stop being abstract.
67. As a student, I want Optimize Puzzles that need a single rotation and a double rotation, so that I learn the four AVL cases.
68. As a student, I want to beat the Unbalanced Colossus Boss (rebalancing a degenerate tree that grows new branches midway), so that I master rebalancing.

### Results and feedback
69. As a student, I want a Results screen with my Stars popping in, Moves vs Reference Solution, Glitches and Hints, so that I know exactly how I did.
70. As a student, I want advice on how to earn more Stars, so that retrying has a clear target.
71. As a student, I want my best result kept even if a later attempt is worse, so that replaying never costs me.
72. As a student, I want to watch the Reference Solution play out after finishing a Puzzle, so that I can compare my approach with an efficient one.
73. As a student, I want Next Puzzle, Retry and Back to Zone on the Results screen, so that I can keep going without extra navigation.
74. As a student, I want to see which Achievements I've earned, so that I have goals beyond Stars.

### Settings and accessibility
75. As a student, I want to set the animation speed (0.5x, 1x, 2x), so that animations are slow enough to follow or fast enough not to bore me.
76. As a student, I want my animation speed and language saved with my Profile, so that I don't reset them every session.
77. As a student, I want to use the keyboard to advance Lessons, so that I don't have to keep clicking.

### Progress Reports and instructors
78. As a student, I want to export a Progress Report with one button, so that I can submit my progress without copying anything by hand.
79. As a student, I want to be told where the report was saved and that it goes to Google Classroom, so that I know what to do with it.
80. As an instructor, I want each Progress Report signed, so that casual edits to Stars or completion are detected.
81. As an instructor, I want a tool that reads a folder of downloaded Progress Reports and produces one spreadsheet row per student per Puzzle, so that I can grade a whole class at once.
82. As an instructor, I want that tool to flag reports whose signature doesn't verify, so that I can follow up on tampering.
83. As an instructor, I want each report to include the Reference Solution's Move count, attempts and Hints for every Puzzle, so that I can see effort as well as completion.
84. As an instructor, I want the option of an optional pre- and post-assessment (a fixed set of Trace and Select Puzzles taken without Hints) whose scores appear in the Progress Report, so that I can measure learning gains if I choose to.
85. As an instructor, I want a recommended syllabus that maps each week to a Zone, so that I can assign the game alongside lectures.

### Distribution
86. As an instructor, I want a single Windows executable that runs without installing or admin rights, so that it works on locked-down lab PCs.
87. As a student, I want my Profiles and results stored in my user folder, so that they survive the game being updated or moved.
88. As a faculty developer, I want to run the game from source with one command, so that colleagues can modify and extend it.

### Content authoring
89. As a faculty content author, I want to add Puzzles by writing a Zone file with only a starting state and a goal, so that I never hand-write answers that could be wrong.
90. As a faculty content author, I want the build to fail if any Puzzle can't be solved by its own Reference Solution, if a Disruption would never fire, or if a Hint contains a literal number, so that broken content never reaches students.
91. As a faculty content author, I want Hints to name values through tokens filled from the live Reference Solution, so that they always agree with the game.
92. As a faculty content author, I want Code Mirror snippets written once per language with markers for which line each Step runs, so that adding a snippet is easy and always available in both languages.

## Implementation Decisions

### Already in place (do not rework)
- **Models** (array, linked list, stack, queue, BST with rotations) are the single source of truth. Each decides legality and explains illegal Moves in learner-facing language, applies Moves and returns animation Steps, parses script lines into textbook Moves, and offers candidate Moves for search. Moves are value-based for the BST and position-based for the linear structures.
- **Goals** produce a plan, the Reference Solution, from any state: sorted (by named algorithm or fewest swaps), target state/output (breadth-first search), script (the textbook way), traverse/search (visit sequences), balanced (deepest-violation-first AVL fix), quiz (computed answer plus distractors generated from plausible mistakes), select (Big-O table, ties broken toward the more restrictive structure).
- **PuzzleSession** owns all rules: Tray order, legality, Strict Puzzles, Glitches, Disruptions keyed to net Move count, undo (Moves stay counted), Hint tiers (tiers 1 and 2 written by people with tokens, tier 3 generated and highlighted), Stars.
- **Star formula:** efficiency = (Moves + Glitches) / Reference Solution Moves. 3 Stars if efficiency ≤ 1.0 and no Hints. 2 Stars if efficiency ≤ 1.5 and at most one Hint. Otherwise 1 Star. Time never counts.
- **No failure states and no difficulty modes.** Timers and lose conditions are explicitly rejected.
- **Persistence:** SQLite in the user's app-data folder. Profiles hold language and animation speed, and results keep the best attempt while counting every attempt. Achievements are derived from results, never stored.
- **Progress Report:** JSON with an HMAC signature using a key built into the game. This deters casual editing and is accepted as not secure against a student who reads the source.
- **Code Mirror:** snippets in Python and Java with `@@kind` line markers. One source script generates both files per snippet.
- **Animations** are visual-only and must never delay game state or scene changes. Scenes switch immediately, and a fade is drawn over them.

### To build
- **Renderer contract.** Every structure renderer implements the same interface: sync to a model, per-frame update, clickable targets (node or slot, with stable keys), draw with highlights/selection/hint/board offset, shake given elements, celebrate, element centre for ripples and particles, and element scale. A factory picks the renderer by structure. Shared behaviour (spawn pop-in, removal ghosts, shake, celebration wave) should live in one place so new renderers only describe layout and structure-specific motion.
- **Click contract (target keys per structure):**
  - Linked list: nodes keyed by position; slots keyed "head" and "after position i".
  - Stack and queue: no board targets. Moves come from Push/Pop or Enqueue/Dequeue buttons.
  - BST: nodes keyed by value; empty-child slots keyed by (parent value, side), and the root slot by (none).
  - Quiz and Select Puzzles: one answer button per option, labelled with the option text.
- **Linked list renderer:** nodes in a row with arrows and a head pointer label. Inserts and deletes re-route arrows, and traversal walks a "cur" marker.
- **Stack renderer:** a vertical tower with a top marker and an Output row. Pushes drop in from above, and pops lift off to the Output row.
- **Queue renderer:** a horizontal line with front/back markers and an Output row. Enqueues slide in at the back, and dequeues slide out at the front.
- **BST renderer:** an in-order-x / depth-y layout with edges. Insertion animates the compare path. Rotations move nodes along arcs. Two-children deletion prompts "click the node that replaces it" and treats the next click as the replacement choice.
- **Answer UI** for quiz and select goals: option buttons, a Glitch on a wrong choice with the goal's explanation, and a Big-O table in the Code Mirror area for Select Puzzles.
- **Zone content files** for The Linked Marshes, The Stack Towers, The Queue Canals, Nexus Alpha and The Binary Forest. They follow the Array Plains format: zone header, Lesson beats, Puzzles, Disruptions. Unlocks are sequential. Content was drafted earlier in the session and should be revalidated by the content contract.
- **Watch Reference Solution:** from Results, open the Puzzle in a replay mode that auto-plays the Reference Solution (Disruptions included) at the Profile's animation speed, with input disabled.
- **Settings:** animation speed (0.5x/1x/2x) beside the language toggle, saved to the Profile.
- **Achievements screen** reachable from the Zone Map.
- **Optional assessment:** a fixed assessment Puzzle set, with Hints disabled, taken as "pre" and "post". Scores are recorded per Profile and included in the Progress Report. It is never required for progression.
- **Report combiner (instructor tool):** reads every report in a folder, verifies signatures, and writes one CSV with a row per student per Puzzle plus a verified flag. It runs from source; no GUI is needed.
- **Windows packaging:** a PyInstaller one-folder or one-file build that bundles content and snippets. Resource lookup works both from source and from the frozen bundle.
- **Zone order:** follows the recommended syllabus for v1 Zones. The faculty owner has not yet supplied the department's own syllabus. If it arrives and differs, Zone order and unlock requirements change, but Zone content does not.

## Testing Decisions

- **Good tests exercise external behaviour only:** Moves in, observable state and messages out, clicks in, scenes and saved results out. Tests never reach into private fields to assert how something is done, except to read rendered positions in animation tests, which are the observable behaviour of a renderer.
- **Tests are written before the code for each new piece** (red, then green). The faculty owner asked for this explicitly.
- **Seam 1, the App driven by real pygame events with no window (primary).** One play-through per Zone: create a Profile, open the Zone, finish the Lesson, play every Puzzle by translating its Reference Solution into clicks through the click contract, then check Results, saved Stars and the Progress Report. The Move-to-clicks helper becomes shared test infrastructure. Prior art: the existing UI flow test.
- **Seam 2, PuzzleSession.** Any new rule (answer handling, replay mode, assessment scoring) is tested here without pygame. Prior art: the existing session tests.
- **Seam 3, the content contract.** A single parametrized suite over every shipped Puzzle and Lesson: Reference Solution finishes, every Disruption fires, Hints pass the lint, and snippets exist in both languages. New Zones are covered by adding their file. Prior art: the existing content test.
- **Seam 4, the renderer contract.** One parametrized suite across all renderers for the shared effects (pop-in, ghost fade-out, shake settles, celebration wave, hit targets match the click contract), plus structure-specific motion tests only where motion is unique (array swap arcs, BST rotation arcs, stack drop-in). Prior art: the existing animation tests, which become the first member of the shared suite.
- **Seam 5, small utility seams.** The report combiner is tested on a folder of real signed reports plus one tampered report. Frozen-bundle resource lookup is tested by simulating the PyInstaller bundle root.
- **Model tests** stay as they are for structure rules and are extended for any model change.

## Out of Scope

- Zones beyond The Binary Forest: Hash Bazaar, Graph Web, Heap Forge, Nexus Beta/Gamma, The Core. The syllabus orders Heap before Graph when they are built.
- A recursion Zone, doubly and circular linked lists, and O(n log n) sorts (merge, quick, heap). These are noted as curriculum gaps in the syllabus.
- A browser or phone build (Pygbag), macOS/Linux packaged builds (source still runs there), and app-store distribution.
- Direct Google Classroom or other LMS integration. Students upload the report file manually.
- Accounts, passwords, servers, cloud sync and leaderboards.
- Difficulty modes, timers, fail states, adaptive difficulty, streak multipliers, currency/cosmetics, the "You Teach" step.
- Free-typed Code Puzzles that compile or run student code (ADR 0002). A drag-and-arrange Code Puzzle Type is deferred, not designed.
- A walkable overworld, tilemaps, character sprites, music and sound effects.
- Colour-blind palettes, screen-reader support and localisation.
- Tamper-proof reporting. The signature only deters casual editing.

## Further Notes

- The faculty owner played the Array Plains slice and approved the feel, then asked for richer animation, which is done. Expect the same loop per Zone: build, launch, play, adjust.
- The department syllabus is still outstanding. The recommended 18-week syllabus in the docs folder is the working assumption.
- Grade Progress Reports on completion, not Stars. Stars reward efficiency in a no-fail game, and grading them would push students to look up answers.
- The Appendix A example in the original plan was wrong (it treated 7 as having two children). The current design makes that class of error impossible, and a model test pins that specific case.
- Draft Zone files for Zones 2 to 5 live in the `content-drafts` folder beside this spec. Every draft Puzzle's Reference Solution finishes, and every Disruption was checked against random play. Each Zone ticket moves its draft into the shipped content and runs the real content contract.
