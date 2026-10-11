"""Draws a stack as a tower (bottom to top) with the top marked, beside an
Output row of popped values in the order they came out.

Stack-specific motion:
  * a pushed block drops onto the tower from above;
  * a popped block lifts off the top and flies to the end of the Output row;
  * undoing a pop takes the value back off the Output row.

There is nothing to click on the board: Moves come from the Push and Pop buttons.
"""
from __future__ import annotations

from typing import NamedTuple

import pygame

from .. import theme
from ..fx import mix
from .base import Motion, Renderer

GAP = 8           # between blocks in the tower
OUT_W = 52        # Output row box size
OUT_GAP = 10


class StackRenderer(Renderer):
    def __init__(self, rect):
        super().__init__(rect)
        self.flyers: dict[int, Flyer] = {}           # popped element id -> its flight to the Output
        self._out_count = 0                          # Output values already shown or in flight

    # ---- layout -------------------------------------------------------------
    def elements(self):
        return list(self.model.items)

    def _floor(self) -> float:
        return self.rect.bottom - 30

    def _tower_x(self) -> float:
        return self.rect.x + self.rect.w * 0.28

    def element_size(self) -> int:
        n = len(self.model.items)
        room = self._floor() - (self.rect.y + 70)
        return int(max(32, min(64, room / max(n, 1) - GAP)))

    def layout(self):
        w = self.element_size()
        x = self._tower_x() - w / 2
        return {eid: (x, self._floor() - (i + 1) * (w + GAP)) for i, eid in enumerate(self.element_ids())}

    def targets(self):
        return []

    def _out_slot(self, index: int) -> pygame.Rect:
        x0 = self.rect.x + self.rect.w * 0.5
        return pygame.Rect(int(x0 + index * (OUT_W + OUT_GAP)), int(self.rect.centery - OUT_W / 2), OUT_W, OUT_W)

    def output(self) -> list[tuple[object, pygame.Rect]]:
        """Landed Output values with their boxes, in removal order."""
        flying = {f.index for f in self.flyers.values()}
        return [(v, self._out_slot(i)) for i, v in enumerate(self.model.out) if i not in flying]

    # ---- motion -------------------------------------------------------------
    def sync(self, model):
        if self.model is None:
            self._out_count = len(model.out)
        if len(model.out) < self._out_count:         # Undo took values back off the Output
            self._out_count = len(model.out)
            self.flyers = {eid: f for eid, f in self.flyers.items() if f.index < self._out_count}
        super().sync(model)

    def enter(self, eid, target):
        self.pos[eid] = [target[0], self.rect.y - 10, 1.0]
        self.motions[eid] = Motion((target[0], self.rect.y - 10), target)

    def leave(self, eid, x, y, value):
        if len(self.model.out) <= self._out_count:   # not a pop (e.g. a Disruption): just fade
            super().leave(eid, x, y, value)
            return
        w = self.element_size()
        slot = self._out_slot(self._out_count)
        end = (slot.x + (OUT_W - w) / 2, slot.y + (OUT_W - w) / 2)
        self.flyers[eid] = Flyer(self._out_count, value, Motion((x, y), end, arc=-1.4 * w))
        self._out_count += 1

    def leaving(self):
        return super().leaving() | set(self.flyers)

    def update(self, dt):
        super().update(dt)
        for eid, f in list(self.flyers.items()):
            f.motion.tween.update(dt)
            if f.motion.tween.done:
                del self.flyers[eid]

    # ---- drawing --------------------------------------------------------------
    def draw_under(self, surf, hint_slot, pulse, offset):
        ox, oy = offset
        w = self.element_size()
        tx = self._tower_x()
        pygame.draw.line(surf, theme.PANEL_EDGE, (tx - w + ox, self._floor() + 4 + oy),
                         (tx + w + ox, self._floor() + 4 + oy), 3)

        ids = self.element_ids()
        if ids:
            x, y, _ = self.pos[ids[-1]]
            tip = (x - 10 + ox, y + w / 2 + oy)
            theme.draw_text(surf, "top", (tip[0] - 42, tip[1] - 11), 18, theme.ACTIVE)
            pygame.draw.polygon(surf, theme.ACTIVE, [tip, (tip[0] - 10, tip[1] - 6), (tip[0] - 10, tip[1] + 6)])
        else:
            theme.draw_text(surf, "(empty)", (tx + ox, self._floor() - 30 + oy), 17, theme.MUTED, center=True)

        first = self._out_slot(0)
        theme.draw_text(surf, "Output", (first.x + ox, first.y - 30 + oy), 18, theme.MUTED)
        f = theme.font(22, bold=True)
        for value, box in self.output():
            _block(surf, box.move(ox, oy), value, mix(theme.IDLE, theme.BG, 0.35), f)
        for flyer in self.flyers.values():
            x, y = flyer.motion.at()
            _block(surf, pygame.Rect(int(x + ox), int(y + oy), w, w), flyer.value, theme.BAD, f)


class Flyer(NamedTuple):
    """A popped value on its way to the Output row."""

    index: int            # its place in the Output
    value: object
    motion: Motion


def _block(surf, rect, value, fill, font) -> None:
    pygame.draw.rect(surf, fill, rect, border_radius=10)
    img = font.render(str(value), True, theme.TEXT)
    surf.blit(img, img.get_rect(center=rect.center))
