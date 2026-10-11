"""Where a Puzzle is played. Clicks become Moves; the PuzzleSession judges them."""
from __future__ import annotations

import pygame

from ...models import Move
from ...puzzles.session import PuzzleSession, reference_count
from .. import theme
from ..anim import StepPlayer
from ..app import SIZE, Scene
from ..code_panel import CodePanel
from ..fx import Effects, Shake
from ..renderers import make_renderer
from ..widgets import Row

VIZ = pygame.Rect(30, 110, 820, 400)
CODE = pygame.Rect(870, 110, 380, 400)
STAGE = {"guided": "Guided", "challenge": "Challenge", "boss": "BOSS"}


class PuzzleScene(Scene):
    def __init__(self, app, zone, puzzle):
        super().__init__(app)
        self.zone, self.puzzle = zone, puzzle
        self.session = PuzzleSession(puzzle)
        self.renderer = make_renderer(puzzle.structure, VIZ)
        self.player = StepPlayer(app.profile.speed)
        self.code_panel = CodePanel(CODE, app.profile.language)
        self.code_panel.show(puzzle.code)
        self.selected: list[int] = []
        self.hint_move: Move | None = None
        self.glitch_flash = 0.0
        self.fx = Effects()
        self.board_shake = Shake()
        self.message = puzzle.intro or puzzle.brief
        self.message_colour = theme.TEXT
        self._sync()

    # ---- state -> view ---------------------------------------------------
    def _sync(self):
        s = self.session
        self.renderer.show_slots = "insert" in self.puzzle.ops and s.tray_next is not None and not s.done
        self.renderer.sync(s.model)
        row = Row(30, SIZE[1] - 70)
        self.buttons = []
        if "swap" in self.puzzle.ops:
            self.buttons.append(row.add("Swap", self._swap, enabled=len(self.selected) == 2 and not s.done,
                                        accent=self.zone.color))
        self.buttons += [
            row.add("Undo", self._undo, enabled=bool(s.history) and not s.done),
            row.add("Hint", self._hint, enabled=not s.done, accent=theme.ACTIVE),
        ]
        right = Row(SIZE[0] - 360, SIZE[1] - 70)
        if s.done:
            right.x = SIZE[0] - 220
            self.buttons.append(right.add("See Results", self._results, width=190, accent=theme.GOOD))
        else:
            right.x = SIZE[0] - 200
            self.buttons.append(right.add("Leave Puzzle", lambda: self.app.open_zone(self.zone), width=170))

    def _say(self, text, colour=theme.TEXT):
        self.message, self.message_colour = text, colour

    # ---- actions -----------------------------------------------------------
    def _attempt(self, move: Move):
        out = self.session.try_move(move)
        self.selected = []
        if not out.ok:
            self.glitch_flash = 0.6
            cells = [a for a in move.args[:2] if isinstance(a, int)] if move.op in ("swap", "visit") else []
            if cells:
                self.renderer.shake(cells)
            else:
                self.board_shake = Shake(0.35, amplitude=6)
            self._say(f"Glitch! {out.glitch}", theme.BAD)
            self._sync()
            return
        self.hint_move = None
        self.code_panel.show(self.puzzle.code) if self.puzzle.code else \
            self.code_panel.show_for(self.puzzle.structure, move.op)
        self.player.play(out.steps)
        if out.steps:
            self._say(out.steps[-1].text)
        self._sync()
        if move.op == "visit":
            self.fx.ripple(self.renderer.center_of(move.args[0]), theme.ACTIVE, radius=70)
        if out.disruption:
            self.player.play(out.disruption_steps)
            self._say(out.disruption, theme.BAD)
            self.board_shake = Shake(0.7, amplitude=16)
        if out.done:
            self._say(self.puzzle.outro or "Structure repaired!", theme.GOOD)
            self._celebrate()

    def _celebrate(self):
        self.renderer.celebrate()
        colours = [theme.GOOD, theme.STAR, theme.SELECT, self.zone.color, theme.TEXT]
        for k in range(5):
            self.fx.particles.burst((VIZ.x + VIZ.w * (k + 0.5) / 5, VIZ.centery), 26, colours)

    def _swap(self):
        if len(self.selected) == 2:
            self._attempt(Move.of("swap", *self.selected))

    def _undo(self):
        if self.session.undo():
            self.selected, self.hint_move = [], None
            self._say("Undone. (The Move still counts toward your score.)", theme.MUTED)
            self._sync()

    def _hint(self):
        tier, text, move = self.session.hint()
        self.hint_move = move
        self._say(text, theme.ACTIVE)

    def _results(self):
        from .results import ResultsScene
        self.app.go(ResultsScene(self.app, self.zone, self.puzzle, self.session))

    def on_event(self, event):
        if event.type != pygame.MOUSEBUTTONUP or event.button != 1 or self.session.done:
            return
        for t in self.renderer.targets():
            if not t.rect.collidepoint(event.pos):
                continue
            if t.kind == "slot":
                self._attempt(Move.of("insert", t.key, self.session.tray_next))
            elif "visit" in self.puzzle.ops:
                self._attempt(Move.of("visit", t.key))
            elif "swap" in self.puzzle.ops:
                if t.key in self.selected:
                    self.selected.remove(t.key)
                else:
                    self.selected = (self.selected + [t.key])[-2:]
                self._sync()
            return

    # ---- frame -------------------------------------------------------------
    def update(self, dt):
        self.player.update(dt)
        self.renderer.update(dt)
        self.code_panel.update(dt)
        self.fx.update(dt)
        self.board_shake.update(dt)
        self.glitch_flash = max(0.0, self.glitch_flash - dt)

    def draw(self, surf):
        s, p = self.session, self.puzzle
        theme.draw_text(surf, f"{self.zone.name}  ·  {STAGE[p.stage]}", (30, 14), 17, self.zone.color)
        theme.draw_text(surf, p.title, (30, 36), 30, bold=True)
        theme.draw_text(surf, f"Moves {s.moves}   Par {reference_count(p)}   Glitches {s.glitches}   "
                              f"Hints {s.hints_used}", (SIZE[0] - 30 - 420, 46), 18, theme.MUTED)
        theme.draw_text(surf, p.brief, (30, 78), 17, theme.MUTED, width=840)

        edge = theme.BAD if self.glitch_flash > 0 or self.board_shake.active else theme.PANEL_EDGE
        theme.panel(surf, VIZ.move(*self.board_shake.offset()), edge=edge)
        if s.state.tray:
            theme.draw_text(surf, "Tray  next:", (VIZ.x + 16, VIZ.y + 16), 18, theme.MUTED)
            theme.draw_text(surf, str(s.state.tray[0]), (VIZ.x + 120, VIZ.y + 8), 30, theme.GOOD, bold=True)
            if len(s.state.tray) > 1:
                rest = "  ".join(str(v) for v in s.state.tray[1:])
                theme.draw_text(surf, f"then  {rest}", (VIZ.x + 170, VIZ.y + 16), 18, theme.MUTED)
        hinted, hint_slot = (), None
        m = self.hint_move
        if m is not None:
            if m.op == "swap":
                hinted = m.args
            elif m.op == "visit":
                hinted = (m.args[0],)
            elif m.op == "insert":
                hint_slot = m.args[0]
        self.renderer.draw(surf, self.player.highlights(), self.selected, hinted, hint_slot,
                           offset=self.board_shake.offset())
        step = self.player.current
        self.code_panel.draw(surf, step.kind if step else None)

        box = pygame.Rect(30, 525, SIZE[0] - 60, 100)
        theme.panel(surf, box)
        y = theme.draw_text(surf, self.message, (box.x + 18, box.y + 14), 21, self.message_colour, width=box.w - 36)
        if step and step.text and self.message_colour != theme.BAD:
            theme.draw_text(surf, step.text, (box.x + 18, y + 4), 17, theme.ACTIVE)
        super().draw(surf)
        self.fx.draw(surf)
