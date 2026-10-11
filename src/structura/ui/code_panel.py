"""The Code Mirror panel: shows a snippet and highlights the line that matches
the Step currently playing."""
from __future__ import annotations

import pygame

from ..codemirror import library
from . import theme


class CodePanel:
    def __init__(self, rect: pygame.Rect, language: str):
        self.rect = rect
        self.language = language
        self.snippet: library.Snippet | None = None

    def show(self, key: str | None) -> None:
        if key:
            self.snippet = library.load(key, self.language) or self.snippet

    def show_for(self, structure: str, op: str, preferred: str = "") -> None:
        self.show(preferred or library.DEFAULT_BY_OP.get((structure, op)))

    def draw(self, surf, step_kind: str | None) -> None:
        theme.panel(surf, self.rect)
        label = "CODE MIRROR · " + ("Java" if self.language == "java" else "Python")
        theme.draw_text(surf, label, (self.rect.x + 14, self.rect.y + 10), 15, theme.MUTED, bold=True)
        if not self.snippet:
            return
        active = set(self.snippet.lines_for(step_kind)) if step_kind else set()
        longest = max((len(l) for l in self.snippet.lines), default=1)
        f = theme.font(max(11, min(15, int((self.rect.w - 30) / (longest * 0.55)))), mono=True)
        y = self.rect.y + 40
        clip = surf.get_clip()
        surf.set_clip(self.rect.inflate(-8, -8))
        for i, line in enumerate(self.snippet.lines):
            if i in active:
                pygame.draw.rect(surf, (70, 62, 25), (self.rect.x + 6, y - 1, self.rect.w - 12, f.get_linesize() + 2),
                                 border_radius=4)
                pygame.draw.rect(surf, theme.ACTIVE, (self.rect.x + 6, y - 1, 4, f.get_linesize() + 2))
            img = f.render(line.replace("\t", "    "), True, theme.TEXT if i in active else (185, 195, 215))
            surf.blit(img, (self.rect.x + 16, y))
            y += f.get_linesize()
        surf.set_clip(clip)
