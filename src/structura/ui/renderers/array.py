"""Draws an array as a row of cells with indexes, plus insertion gaps.

Animation rules:
  * cells that trade places travel on opposite arcs (one over, one under);
  * cells that all move the same way (a shift) slide straight;
  * new cells drop in with a little overshoot, removed cells shrink and fade.
"""
from __future__ import annotations

import math

import pygame

from ...models import ArrayModel
from .. import theme
from ..fx import Shake, Tween, ease_in_out_sine, ease_out_back, lerp, mix
from .base import Target

GAP = 26
TRAVEL = 0.45     # seconds for a cell to reach its new place


class _Motion:
    def __init__(self, start, end, arc):
        self.start, self.end, self.arc = start, end, arc
        self.tween = Tween(TRAVEL)

    def at(self):
        t = ease_in_out_sine(self.tween.progress)
        x = lerp(self.start[0], self.end[0], t)
        y = lerp(self.start[1], self.end[1], t) + self.arc * math.sin(math.pi * t)
        return x, y


class ArrayRenderer:
    def __init__(self, rect: pygame.Rect):
        self.rect = rect
        self.model: ArrayModel | None = None
        self.pos: dict[int, list[float]] = {}        # element id -> [x, y, scale]
        self.motions: dict[int, _Motion] = {}
        self.spawns: dict[int, Tween] = {}
        self.ghosts: dict[int, tuple] = {}           # id -> (x, y, value, Tween)
        self.shakes: dict[int, Shake] = {}
        self.cheer: dict[int, Tween] = {}
        self.clock = 0.0
        self.show_slots = False

    # ---- layout -------------------------------------------------------------
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
        old_values = {eid: v for eid, v in self.model.items} if self.model else {}
        self.model = model
        layout = self._layout()
        w = self._cell_w(len(layout))
        moving = {}
        for eid, target in layout.items():
            if eid not in self.pos:
                self.pos[eid] = [target[0], target[1], 0.0]
                self.spawns[eid] = Tween(0.4)
                continue
            current = (self.pos[eid][0], self.pos[eid][1])
            heading = self.motions[eid].end if eid in self.motions else current
            if abs(heading[0] - target[0]) > 0.5 or abs(heading[1] - target[1]) > 0.5:
                moving[eid] = (current, target)
        rightward = any(t[0] > c[0] for c, t in moving.values())
        leftward = any(t[0] < c[0] for c, t in moving.values())
        trade = rightward and leftward
        for eid, (current, target) in moving.items():
            arc = 0.0
            if trade:
                arc = -0.95 * w if target[0] > current[0] else 0.95 * w
            self.motions[eid] = _Motion(current, target, arc)
        for eid in list(self.pos):
            if eid not in layout:
                x, y, _ = self.pos.pop(eid)
                self.ghosts[eid] = (x, y, old_values.get(eid, ""), Tween(0.35))
                self.motions.pop(eid, None)
                self.spawns.pop(eid, None)

    # ---- effects --------------------------------------------------------------
    def shake(self, indexes) -> None:
        ids = self.model.ids()
        for i in indexes:
            if 0 <= i < len(ids):
                self.shakes[ids[i]] = Shake(0.45, amplitude=9)

    def celebrate(self) -> None:
        for i, eid in enumerate(self.model.ids()):
            self.cheer[eid] = Tween(0.3, delay=i * 0.08)

    def celebration(self, eid: int) -> float:
        return self.cheer[eid].progress if eid in self.cheer else 0.0

    def scale(self, eid: int) -> float:
        return self.pos[eid][2]

    def draw_offset(self, eid: int) -> tuple[int, int]:
        s = self.shakes.get(eid)
        return s.offset() if s else (0, 0)

    def update(self, dt: float) -> None:
        if not self.model:
            return
        self.clock += dt
        for eid, m in list(self.motions.items()):
            m.tween.update(dt)
            self.pos[eid][0], self.pos[eid][1] = m.at()
            if m.tween.done:
                del self.motions[eid]
        for eid, t in list(self.spawns.items()):
            t.update(dt)
            self.pos[eid][2] = max(0.0, ease_out_back(t.progress))
            if t.done:
                self.pos[eid][2] = 1.0
                del self.spawns[eid]
        for eid, g in list(self.ghosts.items()):
            g[3].update(dt)
            if g[3].done:
                del self.ghosts[eid]
        for eid, s in list(self.shakes.items()):
            s.update(dt)
            if not s.active:
                del self.shakes[eid]
        for t in self.cheer.values():
            t.update(dt)

    # ---- hit testing ------------------------------------------------------------
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

    def center_of(self, index: int, offset=(0, 0)) -> tuple[int, int]:
        eid = self.model.ids()[index]
        w = self._cell_w(len(self.model.items))
        x, y, _ = self.pos[eid]
        return int(x + w / 2 + offset[0]), int(y + w / 2 + offset[1])

    # ---- drawing ------------------------------------------------------------------
    def draw(self, surf, highlights=None, selected=(), hinted=(), hint_slot=None, offset=(0, 0)) -> None:
        if not self.model:
            return
        highlights = highlights or {}
        ids = self.model.ids()
        w = self._cell_w(len(ids))
        f = theme.font(int(w * 0.42), bold=True)
        pulse = 0.5 + 0.5 * math.sin(self.clock * 6)
        ox, oy = offset

        for t in self.targets():
            if t.kind == "slot":
                colour = mix(theme.GOOD, theme.ACTIVE, pulse) if t.key == hint_slot else theme.GOOD
                r = t.rect.move(ox, oy)
                pygame.draw.rect(surf, colour, r, 2, border_radius=6)
                pygame.draw.line(surf, colour, (r.centerx, r.y + 8), (r.centerx, r.bottom - 8), 2)

        for t in self.targets():
            if t.kind == "node":
                theme.draw_text(surf, str(t.key), (t.rect.centerx + ox, t.rect.bottom + 8 + oy), 16,
                                theme.MUTED, center=True)

        for x, y, value, tw in self.ghosts.values():
            s = 1 - tw.progress
            rect = pygame.Rect(0, 0, w * s, w * s)
            rect.center = (x + w / 2 + ox, y + w / 2 + oy + 20 * tw.progress)
            pygame.draw.rect(surf, mix(theme.BG, theme.BAD, s), rect, border_radius=10)

        # Cells in flight draw last so the arcing pair stays visible over neighbours.
        order = sorted(range(len(ids)), key=lambda i: ids[i] in self.motions)
        for i in order:
            eid, value = self.model.items[i]
            x, y, s = self.pos[eid]
            dx, dy = self.draw_offset(eid)
            colour = highlights.get(eid)
            grow = 1 + (0.08 * pulse if colour else 0)
            size = w * s * grow
            rect = pygame.Rect(0, 0, size, size)
            rect.center = (x + w / 2 + dx + ox, y + w / 2 + dy + oy)
            fill = mix(colour or theme.IDLE, theme.GOOD, self.celebration(eid))
            if colour:
                glow = pygame.Surface((rect.w + 24, rect.h + 24), pygame.SRCALPHA)
                pygame.draw.rect(glow, (*colour, 70), glow.get_rect(), border_radius=18)
                surf.blit(glow, (rect.x - 12, rect.y - 12))
            if eid in self.shakes:
                fill = mix(fill, theme.BAD, 0.7)
            pygame.draw.rect(surf, fill, rect, border_radius=10)
            if i in selected:
                pygame.draw.rect(surf, theme.SELECT, rect.inflate(10, 10), 3, border_radius=12)
            if i in hinted:
                pygame.draw.rect(surf, mix(theme.ACTIVE, theme.TEXT, pulse), rect.inflate(16, 16), 3, border_radius=14)
            dark = fill != theme.IDLE
            img = f.render(str(value), True, (15, 18, 30) if dark else theme.TEXT)
            if s < 0.98:
                img = pygame.transform.smoothscale_by(img, max(0.05, s))
            surf.blit(img, img.get_rect(center=rect.center))
