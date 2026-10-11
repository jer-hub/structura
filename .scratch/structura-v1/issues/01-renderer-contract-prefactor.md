# 01: Shared renderer contract and play-through helper (prefactor)

**What to build:** Make adding a new structure renderer easy before any new Zone is built. The shared visual effects that currently live only in the array renderer (spawn pop-in, removal fade-out, shake, celebration wave, element centre and scale, board offset) move into a common base that every renderer inherits, so a new renderer only describes its layout and structure-specific motion. The array-only animation tests become a renderer contract suite parametrized over all renderers (initially just the array). The test helper that turns a Move into clicks becomes shared test infrastructure keyed by structure, so each later Zone ticket adds its own mapping (the click contract) instead of copying the helper. Nothing changes for players: The Array Plains looks and plays exactly as before.

**Blocked by:** None (can start immediately)

**Status:** ready-for-agent

- [ ] A renderer base provides the shared effects and the contract interface: sync, update, targets, draw (with highlights, selection, hint and board offset), shake, celebrate, celebration, center_of, scale, draw_offset
- [ ] The array renderer keeps only array layout, insertion gaps and swap-arc logic
- [ ] Renderer contract tests (pop-in, ghost fade-out, shake settles, celebration wave runs left to right, every target has the kind and key the click contract promises) run parametrized over a registry of renderers
- [ ] Array-specific motion tests (opposite swap arcs, straight shifts) remain as structure-specific tests
- [ ] The Move-to-clicks test helper is shared across test modules and dispatches by structure, with the array mapping registered
- [ ] The full existing suite passes unchanged in behaviour, and the Array Plains play-through still passes
