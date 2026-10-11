"""A Zone's page: its Lesson and its Puzzles, unlocked in order.

The Lesson comes first, then the Puzzles grouped by Stage in two columns, Guided
on the left and Challenge and Boss on the right, so the path reads top to
bottom, left to right. Each card shows its number in that order, its Stage and
Puzzle Type, whether it is done or locked, and its Stars; the card to play next
is marked.
"""
from __future__ import annotations

from dataclasses import dataclass

import pygame

from ...persistence import progress
from .. import theme
from ..app import SIZE, Scene
from ..fx import mix
from ..widgets import Button

COLUMNS = (("guided",), ("challenge", "boss"))     # Stages per column; the Lesson heads the first
CARD_W, CARD_H = 560, 62
CARD_GAP = 12
HEADING_H = 34
TOP = 178


@dataclass
class ZoneCard(Button):
    """A Lesson or Puzzle on the Zone page."""

    number: int = 0               # the Puzzle's place in unlock order; 0 for the Lesson
    subtitle: str = ""            # e.g. "Guided · Trace", shown under the title
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

        # The badge: a check once played, else the number (dimmed while locked).
        c = (r.x + 34, r.centery)
        if not self.enabled:
            pygame.draw.circle(surf, theme.PANEL_EDGE, c, 18)
            img = theme.font(18, bold=True).render(str(self.number), True, theme.DISABLED)
            surf.blit(img, img.get_rect(center=c))
        elif self.stars is not None:
            pygame.draw.circle(surf, theme.GOOD, c, 18)
            pygame.draw.lines(surf, theme.BG, False, [(c[0] - 8, c[1]), (c[0] - 2, c[1] + 6), (c[0] + 8, c[1] - 6)], 3)
        else:
            pygame.draw.circle(surf, accent if self.next_up else theme.PANEL_EDGE, c, 18)
            label = "i" if self.number == 0 else str(self.number)
            colour = theme.BG if self.next_up else theme.TEXT
            img = theme.font(18, bold=True).render(label, True, colour)
            surf.blit(img, img.get_rect(center=c))

        title_colour = theme.TEXT if self.enabled else theme.DISABLED
        theme.draw_text(surf, self.label, (r.x + 66, r.y + 8), 21, title_colour, bold=self.next_up)
        sub_colour = (theme.BAD if self.boss else theme.MUTED) if self.enabled else theme.DISABLED
        theme.draw_text(surf, self.subtitle, (r.x + 66, r.y + 35), 15, sub_colour)
        if not self.enabled:
            _lock(surf, (r.right - 28, r.centery), theme.MUTED)

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
        self.headings: list[tuple[str, tuple[int, int]]] = []     # (Stage, where its heading goes)
        self.buttons = [Button("Zone Map", pygame.Rect(40, SIZE[1] - 72, 160, 44), app.open_map)]

        lesson = None
        if zone.lesson:
            lesson = ZoneCard("Lesson", pygame.Rect(0, 0, CARD_W, CARD_H), lambda: app.open_lesson(zone),
                              accent=zone.color, subtitle="How it works", next_up=self.next_up is zone.lesson)
        groups: dict[str, list[ZoneCard]] = {stage: [] for stage in theme.STAGE_LABEL}
        for i, p in enumerate(zone.puzzles):
            r = results.get(p.id)
            unlocked = progress.puzzle_unlocked(zone, i, results)
            subtitle = f"{theme.STAGE_LABEL[p.stage]} · {p.type.title()}"
            if not unlocked:
                subtitle += f"  ·  finish {zone.puzzles[i - 1].title} to unlock"
            groups[p.stage].append(ZoneCard(
                p.title, pygame.Rect(0, 0, CARD_W, CARD_H), lambda p=p: app.open_puzzle(zone, p),
                enabled=unlocked, accent=zone.color, number=i + 1, subtitle=subtitle,
                stars=r.stars if r else None, next_up=self.next_up is p, boss=p.stage == "boss"))

        for col, stages in enumerate(COLUMNS):
            x, y = 40 + col * (CARD_W + 80), TOP
            if col == 0 and lesson:
                lesson.rect.topleft = (x, y + HEADING_H)
                self.buttons.append(lesson)
                y += HEADING_H + CARD_H + CARD_GAP + 8
            for stage in stages:
                if not groups[stage]:
                    continue
                self.headings.append((stage, (x, y)))
                y += HEADING_H
                for card in groups[stage]:
                    card.rect.topleft = (x, y)
                    self.buttons.append(card)
                    y += CARD_H + CARD_GAP
                y += 8

    def _next_up(self):
        """The Lesson until a Puzzle is played, then the first unplayed Puzzle; None when cleared."""
        played = any(p.id in self.results for p in self.zone.puzzles)
        if not played and self.zone.lesson:
            return self.zone.lesson
        return next((p for p in self.zone.puzzles if p.id not in self.results), None)

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

        for stage, (x, y) in self.headings:
            colour = theme.BAD if stage == "boss" else theme.MUTED
            theme.draw_text(surf, theme.STAGE_LABEL[stage].upper(), (x + 2, y + 6), 15, colour, bold=True)
        super().draw(surf)
