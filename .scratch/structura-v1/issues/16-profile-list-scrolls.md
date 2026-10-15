# 16: The Profile list scrolls when there are more Profiles than fit

**What to build:** On a shared lab PC, every student can find and pick their Profile, however many Profiles the PC holds (spec story 2). Today the Profile screen lists Profiles in one column with no scrolling, so past about the seventh Profile the rest fall off the bottom of the window and can't be reached. When the list is longer than the space available, the mouse wheel and the up and down arrow keys scroll it, the New Profile button stays reachable, and it is clear that more Profiles lie above or below.

**Blocked by:** None (can start immediately)

**Status:** ready-for-agent

- [ ] With a few Profiles, the screen looks and behaves as it does today
- [ ] With 10 or more Profiles, a UI test driven by real pygame events scrolls with the mouse wheel and signs in as the last Profile
- [ ] The same works with the arrow keys
- [ ] New Profile can still be reached and used when the list is long
- [ ] The list shows when there are more Profiles above or below the visible ones
- [ ] Launched and checked by hand with a long list of Profiles
