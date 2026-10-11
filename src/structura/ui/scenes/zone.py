"""A Zone's page: its Lesson and its Puzzles, unlocked in order.

Stages are grouped into two columns, Learn and Guided on the left and Challenge
and Boss on the right, so the path reads top to bottom, left to right. Each card
shows its step number, whether it is done or locked, and its Stars; the card to
play next is marked.
"""
from __future__ import annotations

from dataclasses import dataclass

import pygame

from ...persistence import progress
from .. import theme
from ..app import SIZE, Scene
from ..fx import mix
from ..widgets import Button

COLUMNS = (("learn", "guided"), ("challenge", "boss"))
SECTION = {"learn": "Learn", "guided": "Guided", "challenge": "Challenge", "boss": "Boss"}
CARD_W, CARD_H = 560, 62
CARD_GAP = 12
HEADING_H = 34
TOP = 178


@dataclass
class StageCard(Button):
    """A Lesson or Puzzle on the Zone page."""

    step: int = 0                 # 0 for the Lesson
    tag: str = ""                 # e.g. "Trace", shown under the title
    stars: int | None = None      # None until played
    next_up: bool = False
    boss: bool = False

    def _draw(self, surf):
        r, accent = self.rect, self.accent
        if not self.enabled:
            bg, edge = theme.PANEL, theme.PANEL_EDGE
        elif self.next_up:
            bg, edge = mix(theme.PANEL, accent, 0.28 if self.hover else 0.2), accent
        else:
            bg, edge = mix(theme.PANEL, theme.PANEL_EDGE, 0.8 if self.hover else 0.4), mix(theme.PANEL_EDGE, accent, 0.5)
        if self.boss and self.enabled:
            edge = theme.BAD
        pygame.draw.rect(surf, bg, r, border_radius=10)
        pygame.draw.rect(surf, edge, r, 2 + self.next_up, border_radius=10)

        # The step badge: a number, a check once played, or a lock.
        c = (r.x + 34, r.centery)
        if not self.enabled:
            pygame.draw.circle(surf, theme.PANEL_EDGE, c, 18)
            _lock(surf, c, theme.MUTED)
        elif self.stars is not None:
            pygame.draw.circle(surf, theme.GOOD, c, 18)
            pygame.draw.lines(surf, theme.BG, False, [(c[0] - 8, c[1]), (c[0] - 2, c[1] + 6), (c[0] + 8, c[1] - 6)], 3)
        else:
            pygame.draw.circle(surf, accent if self.next_up else theme.PANEL_EDGE, c, 18)
            label = "i" if self.step == 0 else str(self.step)
            colour = theme.BG if self.next_up else theme.TEXT
            img = theme.font(18, bold=True).render(label, True, colour)
            surf.blit(img, img.get_rect(center=c))

        title_colour = theme.TEXT if self.enabled else theme.DISABLED
        theme.draw_text(surf, self.label, (r.x + 66, r.y + 8), 21, title_colour, bold=self.next_up)
        sub = self.tag if self.enabled else f"{self.tag}  ·  finish the one before to unlock"
        sub_colour = (theme.BAD if self.boss else theme.MUTED) if self.enabled else theme.DISABLED
        theme.draw_text(surf, sub, (r.x + 66, r.y + 35), 15, sub_colour)

        if self.next_up:
            img = theme.font(15, bold=True).render("NEXT", True, theme.BG)
            pill = img.get_rect(midright=(r.right - 16, r.centery)).inflate(16, 6)
            pygame.draw.rect(surf, accent, pill, border_radius=pill.h // 2)
            surf.blit(img, img.get_rect(center=pill.center))
        elif self.stars is not None:
            theme.stars(surf, (r.right - 62, r.centery), self.stars, size=20)


def _lock(surf, c, colour):
    body = pygame.Rect(0, 0, 14, 11)
    body.midtop = (c[0], c[1] - 2)
    pygame.draw.rect(surf, colour, body, border_radius=2)
    pygame.draw.arc(surf, colour, pygame.Rect(c[0] - 5, c[1] - 10, 10, 14), 0, 3.15, 2)


class ZoneScene(Scene):
    def __init__(self, app, zone):
        super().__init__(app)
        self.zone = zone
        self.results = results = app.results()
        self.next_up = self._next_up()
        self.headings: list[tuple[str, tuple[int, int]]] = []
        self.buttons = [Button("Zone Map", pygame.Rect(40, SIZE[1] - 72, 160, 44), app.open_map)]

        groups: dict[str, list[StageCard]] = {k: [] for k in SECTION}
        if zone.lesson:
            groups["learn"].append(StageCard("Lesson", pygame.Rect(0, 0, CARD_W, CARD_H),
                                             lambda: app.open_lesson(zone), accent=zone.color,
                                             tag="How it works", next_up=self.next_up == "Lesson"))
        for i, p in enumerate(zone.puzzles):
            r = results.get(p.id)
            groups[p.stage].append(StageCard(
                p.title, pygame.Rect(0, 0, CARD_W, CARD_H), lambda p=p: app.open_puzzle(zone, p),
                enabled=progress.puzzle_unlocked(zone, i, results), accent=zone.color, step=i + 1,
                tag=p.type.title(), stars=r.stars if r else None,
                next_up=self.next_up == p.title, boss=p.stage == "boss"))

        for col, sections in enumerate(COLUMNS):
            x, y = 40 + col * (CARD_W + 80), TOP
            for key in sections:
                if not groups[key]:
                    continue
                self.headings.append((SECTION[key], (x, y)))
                y += HEADING_H
                for card in groups[key]:
                    card.rect.topleft = (x, y)
                    self.buttons.append(card)
                    y += CARD_H + CARD_GAP
                y += 8

    def _next_up(self) -> str | None:
        """The Lesson until something is played, then the first unplayed Puzzle."""
        if not any(p.id in self.results for p in self.zone.puzzles):
            return "Lesson" if self.zone.lesson else self.zone.puzzles[0].title
        return next((p.title for p in self.zone.puzzles if p.id not in self.results), None)

    def draw(self, surf):
        z = self.zone
        theme.draw_text(surf, z.name, (40, 30), 40, z.color, bold=True)
        theme.draw_text(surf, z.intro, (40, 88), 19, theme.MUTED, width=SIZE[0] - 420)

        # Progress: Stars earned and Puzzles cleared, top right.
        got, total = progress.zone_stars(z, self.results)
        cleared = sum(p.id in self.results for p in z.puzzles)
        right = SIZE[0] - 40
        theme.star(surf, (right - 150, 56), 26, theme.STAR)
        theme.draw_text(surf, f"{got} / {total}", (right - 130, 42), 24, theme.TEXT, bold=True)
        bar = pygame.Rect(right - 300, 92, 300, 8)
        pygame.draw.rect(surf, theme.PANEL_EDGE, bar, border_radius=4)
        if cleared:
            pygame.draw.rect(surf, z.color, (bar.x, bar.y, bar.w * cleared / len(z.puzzles), bar.h), border_radius=4)
        theme.draw_text(surf, f"{cleared} of {len(z.puzzles)} Puzzles cleared", (right - 300, 106), 15, theme.MUTED)

        for text, (x, y) in self.headings:
            colour = theme.BAD if text == "Boss" else theme.MUTED
            theme.draw_text(surf, text.upper(), (x + 2, y + 6), 15, colour, bold=True)
        super().draw(surf)
