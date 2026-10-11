# 13: Windows executable

**What to build:** A Windows build of Structura that students run on lab PCs without installing anything or needing admin rights. Double-clicking it opens the game, with all Zone content and Code Mirror snippets bundled. Profiles and results live in the user's app-data folder and Progress Reports go to the user's Documents folder, so replacing the build with a newer one keeps everyone's progress. Faculty have one documented command to rebuild after content changes.

**Blocked by:** None (can start immediately). Re-run the build before release, after Zone tickets land.

**Status:** ready-for-agent

- [ ] A build command produces a runnable Windows build (one folder or one file) that bundles content and snippets
- [ ] Content and snippet lookup works both from source and from inside the packaged build; a test simulates the bundle root to prove it
- [ ] The packaged build launches, reaches the Profile screen and can open The Array Plains (manual check recorded in the ticket's Comments)
- [ ] Player data and reports are written outside the build folder (test with a temporary home)
- [ ] Build and distribution instructions for faculty are in the docs
