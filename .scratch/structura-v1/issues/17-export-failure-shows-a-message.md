# 17: Exporting a Progress Report to a folder you can't write to shows a message instead of crashing

**What to build:** A student who presses Export Progress Report is never thrown out of the game. If the report can't be written (the folder isn't writable, a drive is missing, or a lab PC redirects Documents somewhere unavailable), the Zone Map says the report couldn't be saved and why, in plain words, and the game keeps running so the student can try again or tell their instructor. Today any error while saving the report crashes the game. A successful export behaves exactly as it does now (spec story 79).

**Blocked by:** None (can start immediately)

**Status:** ready-for-agent

- [ ] A UI test driven by real pygame events exports to a folder that can't be written to; the Zone Map shows a failure message and the game keeps running
- [ ] The failure message is visually distinct from the success message and names the folder it tried
- [ ] After a failed export, other Zone Map actions still work (for example, opening a Zone)
- [ ] A successful export still shows where the report was saved and that it goes to Google Classroom
