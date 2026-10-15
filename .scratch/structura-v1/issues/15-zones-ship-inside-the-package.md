# 15: Zone files ship inside the game package

**What to build:** A faculty developer who installs Structura as a package and launches it with the `structura` command gets every Zone, exactly as when running from source. Today the Zone files sit at the repository root, outside the package, so an installed copy can't find them; only the Code Mirror snippets are packaged. The Zone files move inside the game package beside the snippets and are declared as package data, and content lookup finds them the same way whether the game runs from source or installed. Anything that names the old location (docs, the spec's notes on draft content, tests, tools) points at the new one. Players see no change.

This is also groundwork for the Windows executable (ticket 13), which needs content lookup to work from inside a packaged build.

**Blocked by:** None (can start immediately)

**Status:** ready-for-agent

- [ ] Running from source loads the same Zones, in the same order, as before the move
- [ ] A test proves content lookup does not depend on the repository layout (for example, by loading Zones through the installed package's own location rather than the repo root)
- [ ] The package declares the Zone files as package data alongside the snippets
- [ ] No doc, test or tool still refers to the old location
- [ ] The full suite passes, including the content contract over every shipped Puzzle
