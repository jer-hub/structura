"""Draws an array as a row of cells with indexes, plus insertion gaps."""
from __future__ import annotations

import pygame

from ...models import ArrayModel
from .. import theme
from ..anim import approach
from .base import Target

GAP = 26


class ArrayRenderer:
    def __init__(self, rect: pygame.Rect):
        self.rect = rect
        self.model: ArrayModel | None = None
        self.pos: dict[int, list[float]] = {}     # element id -> [x, y, scale]
        self.show_slots = False

    def _cell_w(self, n: int) -> int:
        return int(max(40, min(84, (self.rect.w - 40 - GAP * (n + 1)) / max(n, 1))))

    def _layout(self) -> dict[int, tuple[float, float]]:
        ids = self.model.ids()
        n, w = len(ids), self._cell_w(len(ids))
        total = n * w + (n - 1) * GAP
        x0 = self.rect.centerx - total / 2
        y = self.rect.centery - w / 2
        return {eid: (x0 + i * (w + GAP), y) for i, eid in enumerate(ids)}

    def sync(self, model: ArrayModel) -> None:
        self.model = model
        layout = self._layout()
        for eid, (x, y) in layout.items():
            if eid not in self.pos:
                self.pos[eid] = [x, y - 40, 0.2]
        for eid in list(self.pos):
            if eid not in layout:
                del self.pos[eid]

    def update(self, dt: float) -> None:
        if not self.model:
            return
        for eid, (x, y) in self._layout().items():
            p = self.pos[eid]
            p[0], p[1], p[2] = approach(p[0], x, dt), approach(p[1], y, dt), approach(p[2], 1.0, dt)

    def targets(self) -> list[Target]:
        if not self.model:
            return []
        layout = self._layout()
        ids = self.model.ids()
        w = self._cell_w(len(ids))
        out = [Target("node", i, pygame.Rect(int(layout[eid][0]), int(layout[eid][1]), w, w))
               for i, eid in enumerate(ids)]
        if self.show_slots:
            if ids:
                xs = [layout[eid][0] - GAP for eid in ids] + [layout[ids[-1]][0] + w]
                y = layout[ids[0]][1]
            else:
                xs, y = [self.rect.centerx - GAP / 2], self.rect.centery - 30
            for i, x in enumerate(xs):
                out.append(Target("slot", i, pygame.Rect(int(x + 2), int(y - 12), GAP - 4, w + 24)))
        return out

    def draw(self, surf, highlights=None, selected=(), hinted=(), hint_slot=None) -> None:
        if not self.model:
            return
        highlights = highlights or {}
        ids = self.model.ids()
        w = self._cell_w(len(ids))
        f = theme.font(int(w * 0.42), bold=True)
        for t in self.targets():
            if t.kind == "slot":
                colour = theme.ACTIVE if t.key == hint_slot else theme.GOOD
                pygame.draw.rect(surf, colour, t.rect, 2, border_radius=6)
                pygame.draw.line(surf, colour, (t.rect.centerx, t.rect.y + 8), (t.rect.centerx, t.rect.bottom - 8), 2)
        for i, (eid, value) in enumerate(self.model.items):
            x, y, s = self.pos[eid]
            size = w * s
            rect = pygame.Rect(0, 0, size, size)
            rect.center = (x + w / 2, y + w / 2)
            fill = highlights.get(eid, theme.IDLE)
            pygame.draw.rect(surf, fill, rect, border_radius=10)
            if i in selected:
                pygame.draw.rect(surf, theme.SELECT, rect.inflate(10, 10), 3, border_radius=12)
            if i in hinted:
                pygame.draw.rect(surf, theme.ACTIVE, rect.inflate(16, 16), 3, border_radius=14)
            img = f.render(str(value), True, (15, 18, 30) if fill != theme.IDLE else theme.TEXT)
            surf.blit(img, img.get_rect(center=rect.center))
            theme.draw_text(surf, str(i), (rect.centerx, int(y + w + 8)), 16, theme.MUTED, center=True)
