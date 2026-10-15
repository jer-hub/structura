# 14: A malformed Progress Report is reported as unverified instead of crashing

**What to build:** Checking a Progress Report's signature never crashes, whatever the file holds. A report with no signature, a signature that isn't text, or a file that isn't a report object at all is simply "not verified". Today a missing or non-text signature raises an error instead. This is the base the instructor report combiner (ticket 11) builds on, so it can flag edited reports and skip unrelated files rather than stopping on the first odd one.

**Blocked by:** None (can start immediately)

**Status:** ready-for-agent

- [ ] A genuine report exported by the game still verifies
- [ ] A report with its signature removed is not verified, and nothing raises
- [ ] A report whose signature is a number, a list or null is not verified, and nothing raises
- [ ] Something that isn't a report object (a list, a string, a JSON object without the report format) is not verified, and nothing raises
- [ ] Tests sit at the report utility seam (spec Seam 5) and only use the public export and verify behaviour
