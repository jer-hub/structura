# 12: Optional pre/post assessment

**What to build:** An optional assessment that instructors can use to measure learning. Students open it from the Zone Map and take it as "Pre" (before playing) or "Post" (after). It is a fixed set of Trace (quiz) and Select Puzzles across arrays, linked lists, stacks, queues and BSTs. Hints are disabled, there is no Code Mirror help, and each question is a single attempt that is scored right or wrong (no Glitch retries, so the score reflects understanding). Scores are stored on the Profile and appear in the Progress Report, and the report combiner gets matching pre and post score columns. The assessment never gates progression.

**Blocked by:** 05 (Nexus Alpha), 06 (The Binary Forest, part 1), 11 (Instructor report combiner)

**Status:** ready-for-agent

- [ ] Assessment content is defined in a content file; every question's answer is computed by the models (content contract covers it)
- [ ] Single-attempt scoring mode in the session layer, tested without pygame
- [ ] Pre and Post attempts are stored separately per Profile (latest attempt of each kind kept)
- [ ] The Progress Report includes pre/post scores and dates; the signature still verifies
- [ ] The combiner CSV gains pre and post score columns (test)
- [ ] UI test: take Pre, answer all questions, and the score appears on the summary screen and in an exported report
- [ ] Zones and Puzzles are unaffected by whether the assessment was taken
