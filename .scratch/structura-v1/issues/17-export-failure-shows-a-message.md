# 17: Exporting a Progress Report to a folder you can't write to shows a message instead of crashing

**What to build:** A student who presses Export Progress Report is never thrown out of the game. If the report can't be written (the folder isn't writable, a drive is missing, or a lab PC redirects Documents somewhere unavailable), the Zone Map says the report couldn't be saved and why, in plain words, and the game keeps running so the student can try again or tell their instructor. Today any error while saving the report crashes the game. A successful export behaves exactly as it does now (spec story 79).

**Blocked by:** None (can start immediately)

**Status:** done

- [x] A UI test driven by real pygame events exports to a folder that can't be written to; the Zone Map shows a failure message and the game keeps running
- [x] The failure message is visually distinct from the success message and names the folder it tried
- [x] After a failed export, other Zone Map actions still work (for example, opening a Zone)
- [x] A successful export still shows where the report was saved and that it goes to Google Classroom

## Comments

- The Zone Map catches any `OSError` from exporting and shows, in red, "Your Progress Report couldn't be saved in <folder>: <reason> Try again, or show this message to your instructor." Reasons in plain words: locked or not allowed, something that isn't a folder in the way, folder or drive unavailable (or name too long), otherwise the system's own reason. Success stays green with the same text.
- The UI test puts a file where the reports folder should be, exports (fails), removes the file, exports again (succeeds), then opens The Array Plains.
- `report.export` now creates its folder and takes it as a required argument, so the Zone Map alone chooses where reports go.
- From the spec review, test-first: a write that fails partway (disk full) used to leave a half-written report a student might upload; the report is now written to a `.partial` file and renamed into place only when complete.
- The message now sits just above the action buttons and grows upward, so a long OneDrive path wrapping to three lines doesn't cover them (checked by headless render). The success message sits slightly lower than before as a result.
- Not changed: the message disappears after leaving the Zone Map; `Path.home()` failing (no user profile at all) would still crash; a second export in the same minute overwrites the first. None is in this ticket.
