"""Choose or create a Profile. No passwords: a shared lab PC holds several."""
from __future__ import annotations

import pygame

from .. import theme
from ..app import SIZE, Scene
from ..widgets import Button, Row, TextField


class ProfileScene(Scene):
    def __init__(self, app):
        super().__init__(app)
        self.creating = False
        self.language = "python"
        self._build()

    def _build(self):
        self.buttons, self.fields = [], []
        cx = SIZE[0] // 2
        if not self.creating:
            y = 250
            for p in self.app.store.profiles():
                self.buttons.append(Button(f"{p.name}  ({p.student_id})", pygame.Rect(cx - 220, y, 440, 46),
                                           lambda p=p: self.app.sign_in(p)))
                y += 56
            self.buttons.append(Button("New Profile", pygame.Rect(cx - 110, max(y + 20, 330), 220, 48),
                                       self._start_create, accent=theme.GOOD))
            return
        self.name = TextField("Name", pygame.Rect(cx - 220, 260, 440, 44))
        self.sid = TextField("Student ID", pygame.Rect(cx - 220, 350, 440, 44))
        self.name.focused = True
        self.fields = [self.name, self.sid]
        row = Row(cx - 220, 440)
        self.buttons += [
            row.add("Python", lambda: self._lang("python"), selected=self.language == "python"),
            row.add("Java", lambda: self._lang("java"), selected=self.language == "java"),
        ]
        row = Row(cx - 220, 520)
        self.buttons += [row.add("Create", self._create, accent=theme.GOOD), row.add("Cancel", self._cancel)]

    def _start_create(self):
        self.creating, self.message = True, ""
        self._build()

    def _cancel(self):
        self.creating, self.message = False, ""
        self._build()

    def _lang(self, lang):
        self.language = lang
        for b in self.buttons:
            if b.label in ("Python", "Java"):
                b.selected = b.label.lower() == lang

    def _create(self):
        try:
            profile = self.app.store.create_profile(self.name.text, self.sid.text, self.language)
        except ValueError as exc:
            self.message = "Name and student ID are both required."
            return
        self.app.sign_in(profile)

    def on_event(self, event):
        if self.creating and event.type == pygame.KEYDOWN and event.key == pygame.K_TAB:
            self.name.focused, self.sid.focused = self.sid.focused, self.name.focused
        if self.creating and event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            self._create()

    def draw(self, surf):
        cx = SIZE[0] // 2
        theme.draw_text(surf, "STRUCTURA", (cx, 80), 64, theme.SELECT, bold=True, center=True)
        theme.draw_text(surf, "Repair the Datasphere, one data structure at a time.", (cx, 160), 22,
                        theme.MUTED, center=True)
        if self.creating:
            theme.draw_text(surf, "Code Mirror language", (cx - 220, 414), 18, theme.MUTED)
        else:
            theme.draw_text(surf, "Who's playing?", (cx, 210), 24, center=True)
        if self.message:
            theme.draw_text(surf, self.message, (cx, 600), 20, theme.BAD, center=True)
        super().draw(surf)
