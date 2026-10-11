# 10: Achievements screen

**What to build:** A screen reachable from the Zone Map that lists every Achievement with its title and requirement, showing earned ones lit and the rest dimmed. Achievements are derived from results each time (nothing new is stored): First Repair, Clean Hands, Boss Breaker, Persistence, and one "Master of <Zone>" per Zone, so new Zones add their own automatically.

**Blocked by:** None (can start immediately)

**Status:** ready-for-agent

- [ ] Zone Map has an Achievements button; the screen has a Back button to the Zone Map
- [ ] Earned and unearned Achievements are visually distinct
- [ ] Achievement evaluation tests cover each rule (earned and not earned)
- [ ] UI test: a fresh Profile shows none earned; after finishing one Puzzle, First Repair shows as earned
