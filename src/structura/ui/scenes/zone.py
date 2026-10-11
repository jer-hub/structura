"""A Zone's page: its Lesson and its Puzzles, unlocked in order."""
from __future__ import annotations

import pygame

from ...persistence import progress
from .. import theme
from ..app import SIZE, Scene
from ..widgets import Button

STAGE_LABEL = {"guided": "Guided", "challenge": "Challenge", "boss": "BOSS"}


class ZoneScene(Scene):
    def __init__(self, app, zone):
        super().__init__(app)
        self.zone = zone
        results = app.results()
        self.results = results
        self.buttons = [Button("Zone Map", pygame.Rect(40, SIZE[1] - 72, 160, 44), app.open_map)]
        y = 220
        if zone.lesson:
            self.buttons.append(Button("Lesson", pygame.Rect(80, y, 360, 48),
                                       lambda: app.open_lesson(zone), accent=zone.color))
            y += 70
        for i, p in enumerate(zone.puzzles):
            self.buttons.append(Button(p.title, pygame.Rect(80, y, 360, 48),
                                       lambda p=p: app.open_puzzle(zone, p),
                                       enabled=progress.puzzle_unlocked(zone, i, results), accent=zone.color))
            y += 62

    def draw(self, surf):
        z = self.zone
        theme.draw_text(surf, z.name, (40, 30), 40, z.color, bold=True)
        theme.draw_text(surf, z.intro, (40, 90), 20, theme.MUTED, width=SIZE[0] - 80)
        super().draw(surf)
        for b in self.buttons:
            p = next((p for p in z.puzzles if p.title == b.label), None)
            if p is None:
                continue
            theme.draw_text(surf, f"{STAGE_LABEL[p.stage]} · {p.type.title()}", (b.rect.right + 20, b.rect.y + 12),
                            18, theme.BAD if p.stage == "boss" else theme.MUTED)
            r = self.results.get(p.id)
            if r:
                theme.stars(surf, (b.rect.right + 300, b.rect.centery), r.stars, size=22)
