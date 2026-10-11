"""Draws a singly linked list: a head pointer, nodes in a row joined by arrows,
and null at the end. The row is only for reading; the arrows are the structure.

Linked-list-specific motion:
  * arrows follow the nodes as they move, so inserts and deletes re-route them;
  * while a removed node fades, the arrow that now skips it bows over it;
  * a "cur" marker glides to whichever node the current walk Step is on.

Slots are keyed HEAD (insert at the head) and i (insert after position i).
Arrows run from HEAD or a node, to a node or None (null).
"""
from __future__ import annotations

import math

import pygame

from ...models import Move
from .. import theme
from ..anim import approach
from ..fx import mix
from .base import Renderer, Target

HEAD = "head"     # the head pointer: an arrow's start, and the insert-at-head slot key
HEAD_W = 56       # room for the "head" label
NULL_W = 50       # room for "null"
MAX_GAP = 60      # longest arrow between nodes


class LinkedListRenderer(Renderer):
    def __init__(self, rect):
        super().__init__(rect)
        self.cursor: int | None = None               # element id the "cur" marker is on
        self.cursor_x = 0.0

    # ---- layout -------------------------------------------------------------
    def elements(self):
        return list(self.model.nodes)

    def _track_width(self) -> float:
        return self.rect.w - 40 - HEAD_W - NULL_W

    def element_size(self) -> int:
        n = len(self.model.nodes)
        return int(max(40, min(76, (self._track_width() - MAX_GAP * (n + 1)) / max(n, 1))))

    def gap(self) -> float:
        """Arrow length: as long as fits, so long lists still fit the board."""
        n, w = len(self.model.nodes), self.element_size()
        return max(30, min(MAX_GAP, (self._track_width() - n * w) / (n + 1)))

    def _head_x(self) -> float:
        """Where the head pointer's arrow starts."""
        n, w, g = len(self.model.nodes), self.element_size(), self.gap()
        return self.rect.centerx - (HEAD_W + (n + 1) * g + n * w + NULL_W) / 2 + HEAD_W

    def layout(self):
        w, g = self.element_size(), self.gap()
        x0 = self._head_x() + g
        y = self.rect.centery - w / 2
        return {eid: (x0 + i * (w + g), y) for i, eid in enumerate(self.element_ids())}

    def slot_targets(self):
        w, g = self.element_size(), self.gap()
        y = self.rect.centery - w / 2

        def slot(key, x):
            return Target("slot", key, pygame.Rect(int(x + 6), int(y - 12), int(g - 12), w + 24))

        out = []
        if self.allows("insert_head"):
            out.append(slot(HEAD, self._head_x()))
        if self.allows("insert_after"):
            layout = self.layout()
            out += [slot(i, layout[eid][0] + w) for i, eid in enumerate(self.element_ids())]
        return out

    def slot_move(self, key, value):
        return Move.of("insert_head", value) if key == HEAD else Move.of("insert_after", key, value)

    def slot_for(self, move):
        if move.op == "insert_head":
            return HEAD
        return move.args[0] if move.op == "insert_after" else None

    # ---- arrows ---------------------------------------------------------------
    def arrows(self) -> list[tuple]:
        """(from, to, bowed) for every pointer: `from` is an element id or HEAD,
        `to` is an element id or None (null). A bowed arrow skips a fading node."""
        chain = [HEAD, *self.element_ids(), None]
        ghost_xs = [g[0] for g in self.ghosts.values()]

        def x_of(end):
            if end == HEAD:
                return self._head_x()
            return math.inf if end is None else self.pos[end][0]

        return [(a, b, any(x_of(a) < gx < x_of(b) for gx in ghost_xs)) for a, b in zip(chain, chain[1:])]

    # ---- the cur marker -------------------------------------------------------
    def on_step(self, step):
        eid = step.ids[0] if step is not None and step.kind == "walk" and step.ids else None
        if eid not in self.pos:
            eid = None
        if eid is not None and self.cursor is None:
            self.cursor_x = self._head_x()           # a fresh walk starts at the head
        self.cursor = eid

    def update(self, dt):
        super().update(dt)
        if self.cursor is not None:
            target = self.pos[self.cursor][0] + self.element_size() / 2
            self.cursor_x = approach(self.cursor_x, target, dt)

    # ---- drawing --------------------------------------------------------------
    def _anchor(self, end, side: str, w: float) -> tuple[float, float]:
        """Where an arrow leaves (side "out") or reaches (side "in") one of its ends."""
        cy = self.rect.centery
        if end == HEAD:
            return self._head_x(), cy
        if end is None:
            ids = self.element_ids()
            x = self.pos[ids[-1]][0] + w + self.gap() if ids else self._head_x() + self.gap()
            return x, cy
        x, y, s = self.pos[end]
        half = w * s / 2
        return x + w / 2 + (half if side == "out" else -half), y + w / 2

    def draw_under(self, surf, hint_slot, pulse, offset):
        ox, oy = offset
        w = self.element_size()
        for a, b, bowed in self.arrows():
            x1, y1 = self._anchor(a, "out", w)
            x2, y2 = self._anchor(b, "in", w)
            _arrow(surf, (x1 + ox, y1 + oy), (x2 + ox, y2 + oy), bow=w * 1.1 if bowed else 0.0)

        # A slot is a "+" badge sitting on the arrow it would split; the whole gap is clickable.
        if self.show_slots:
            for t in self.slot_targets():
                hinted = t.key == hint_slot
                colour = mix(theme.GOOD, theme.ACTIVE, pulse) if hinted else theme.GOOD
                c = (t.rect.centerx + ox, t.rect.centery + oy)
                pygame.draw.circle(surf, theme.BG, c, 13)
                pygame.draw.circle(surf, colour, c, 13 + 3 * hinted, 2)
                pygame.draw.line(surf, colour, (c[0] - 6, c[1]), (c[0] + 6, c[1]), 2)
                pygame.draw.line(surf, colour, (c[0], c[1] - 6), (c[0], c[1] + 6), 2)

        cy = self.rect.centery + oy
        theme.draw_text(surf, "head", (self._head_x() - HEAD_W / 2 + ox, cy - 11), 18, theme.ACTIVE,
                        center=True)
        null_x, _ = self._anchor(None, "in", w)
        theme.draw_text(surf, "null", (null_x + 22 + ox, cy - 10), 17, theme.MUTED, center=True)

        if self.cursor is not None:
            top = self.rect.centery - w / 2 - 40 + oy
            theme.draw_text(surf, "cur", (self.cursor_x + ox, top - 6), 17, theme.ACTIVE, center=True)
            tip = (self.cursor_x + ox, top + 30)
            pygame.draw.polygon(surf, theme.ACTIVE, [(tip[0] - 6, tip[1] - 10), (tip[0] + 6, tip[1] - 10), tip])


def _arrow(surf, start, end, bow: float = 0.0) -> None:
    """A pointer arrow, straight or bowed upward by `bow` pixels."""
    colour = theme.MUTED
    if bow:
        mid = ((start[0] + end[0]) / 2, (start[1] + end[1]) / 2 - 2 * bow)
        pts = [(_bezier(start[0], mid[0], end[0], t / 16), _bezier(start[1], mid[1], end[1], t / 16))
               for t in range(17)]
    else:
        pts = [start, end]
    pygame.draw.lines(surf, colour, False, pts, 2)
    (x1, y1), (x2, y2) = pts[-2], pts[-1]
    ang = math.atan2(y2 - y1, x2 - x1)
    pygame.draw.polygon(surf, colour, [
        (x2, y2),
        (x2 - 10 * math.cos(ang - 0.45), y2 - 10 * math.sin(ang - 0.45)),
        (x2 - 10 * math.cos(ang + 0.45), y2 - 10 * math.sin(ang + 0.45)),
    ])


def _bezier(a: float, m: float, b: float, t: float) -> float:
    return (1 - t) ** 2 * a + 2 * (1 - t) * t * m + t ** 2 * b
