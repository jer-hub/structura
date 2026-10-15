# 13: Windows executable

**What to build:** A Windows build of Structura that students run on lab PCs without installing anything or needing admin rights. Double-clicking it opens the game, with all Zone content and Code Mirror snippets bundled. Profiles and results live in the user's app-data folder and Progress Reports go to the user's Documents folder, so replacing the build with a newer one keeps everyone's progress. Faculty have one documented command to rebuild after content changes.

**Blocked by:** None (can start immediately). Re-run the build before release, after Zone tickets land.

**Status:** ready-for-human (only the manual Array Plains check below remains)

- [x] A build command produces a runnable Windows build (one folder or one file) that bundles content and snippets
- [x] Content and snippet lookup works both from source and from inside the packaged build; a test simulates the bundle root to prove it
- [ ] The packaged build launches, reaches the Profile screen and can open The Array Plains (manual check recorded in the ticket's Comments)
- [x] Player data and reports are written outside the build folder (test with a temporary home)
- [x] Build and distribution instructions for faculty are in the docs

## Comments

- Build: `.venv\Scripts\pyinstaller --noconfirm structura.spec` gives `dist\Structura.exe`, one windowed file of about 15 MB. PyInstaller is the optional `build` extra (`pip install -e ".[build]"`). Faculty guide: `docs/windows-build.md`.
- `src/structura/bundle.py` names each bundled folder once (`ZONES`, `SNIPPETS`). `structura.spec` bundles `bundle.pyinstaller_datas()`, and both lookups (`schema.content_dir`, `library._dir`) go through `bundle.locate`. `tests/test_packaging.py` builds a fake bundle from that same list, points `sys._MEIPASS` at it, and checks Zones and snippets load from it and not from the source tree.
- Code review caught a regression in the first version: snippets were looked up from the repository rather than the package, which would have broken an installed copy. Fixed test-first: snippets are found next to the package.
- Manual check, 2026-10-15: `dist\Structura.exe` launched with a temporary `STRUCTURA_HOME` and showed the Profile screen ("Who's playing?", New Profile). Rebuilt after the review fixes and launched again; window opened. **Not yet checked:** opening The Array Plains in the packaged build. Automated clicking couldn't bring the game window to the front, so this needs a person: double-click `dist\Structura.exe`, pick or create a Profile, open The Array Plains. Then tick the box and set Status to done.
- Known limitation, not changed here: Progress Reports go to `<home>\Documents\Structura Reports`. If a school account redirects Documents to OneDrive, that is the local Documents folder rather than the OneDrive one. The game shows the exact path after export, so students can still find it. Using Windows' known-folder lookup would fix it; it's a candidate ticket alongside 17 (export failures).
