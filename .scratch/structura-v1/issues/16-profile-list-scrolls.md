# 16: The Profile list scrolls when there are more Profiles than fit

**What to build:** On a shared lab PC, every student can find and pick their Profile, however many Profiles the PC holds (spec story 2). Today the Profile screen lists Profiles in one column with no scrolling, so past about the seventh Profile the rest fall off the bottom of the window and can't be reached. When the list is longer than the space available, the mouse wheel and the up and down arrow keys scroll it, the New Profile button stays reachable, and it is clear that more Profiles lie above or below.

**Blocked by:** None (can start immediately)

**Status:** ready-for-human (only the hand check below remains)

- [x] With a few Profiles, the screen looks and behaves as it does today
- [x] With 10 or more Profiles, a UI test driven by real pygame events scrolls with the mouse wheel and signs in as the last Profile
- [x] The same works with the arrow keys
- [x] New Profile can still be reached and used when the list is long
- [x] The list shows when there are more Profiles above or below the visible ones
- [ ] Launched and checked by hand with a long list of Profiles

## Comments

- Up to seven Profiles: exactly today's layout (a test pins the row and New Profile positions for 3 and 7). More than seven: seven rows show; the mouse wheel and the Up/Down arrow keys scroll one row at a time; New Profile stays below the list; "↑ N more" / "↓ N more" sit beside the top and bottom rows, with "Scroll or use the arrow keys".
- Names up to 40 characters didn't fit on a row and would have run over those hints, so long names are now shortened with "…" and the student ID is kept (found by the spec review; test-first).
- Checked by a headless render (12 Profiles, scrolled by 2): layout and arrow glyphs look right. **Still to do by hand:** with 10+ Profiles in a real window, scroll with the wheel and the arrow keys, open New Profile and Cancel, sign in as the last Profile, then Switch Profile. Tick the box and set Status to done.
- Not changed: a button fires on mouse release over it even if the press began elsewhere, so holding the mouse down while scrolling could release onto a different Profile. That's how every button in the game works today, not something this ticket introduced.
- `wheel` and `press` joined the shared player helpers in `tests/clicks.py`.
