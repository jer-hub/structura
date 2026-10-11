"""The Zone page: every stage card fits on screen without overlapping, and the
card to play next is marked."""
import os

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")

import pygame
import pytest

from structura.persistence.store import Store
from structura.puzzles.schema import load_all
from structura.ui.app import SIZE, App
from structura.ui.scenes.zone import ZoneScene

ZONES = load_all()


@pytest.fixture
def app(tmp_path):
    pygame.init()
    a = App(Store(tmp_path / "t.db"), ZONES, screen=pygame.display.set_mode(SIZE), report_dir=tmp_path)
    a.sign_in(a.store.create_profile("Ana", "1"))
    yield a
    a.store.close()


@pytest.mark.parametrize("zone", ZONES, ids=lambda z: z.id)
def test_every_card_fits_on_screen_without_overlapping(app, zone):
    scene = ZoneScene(app, zone)
    screen = pygame.Rect((0, 0), SIZE)
    rects = [b.rect for b in scene.buttons]
    for i, r in enumerate(rects):
        assert screen.contains(r), f"{scene.buttons[i].label} is off screen"
        assert r.collidelist(rects[:i] + rects[i + 1:]) == -1, f"{scene.buttons[i].label} overlaps"
    scene.draw(app.screen)


def test_the_lesson_is_next_before_anything_is_played(app):
    zone = ZONES[1]
    assert ZoneScene(app, zone).next_up is zone.lesson


def test_the_first_unfinished_puzzle_is_next(app):
    zone = ZONES[1]
    app.store.record(app.profile.id, zone.puzzles[0].id, 3, 4, 0, 0)
    assert ZoneScene(app, zone).next_up is zone.puzzles[1]


def test_nothing_is_next_once_the_zone_is_cleared(app):
    zone = ZONES[1]
    for p in zone.puzzles:
        app.store.record(app.profile.id, p.id, 3, 4, 0, 0)
    assert ZoneScene(app, zone).next_up is None


def cards(scene):
    return {b.label: b for b in scene.buttons if b.label != "Zone Map"}


def test_each_puzzle_card_names_its_stage_and_puzzle_type(app):
    zone = ZONES[1]
    scene = ZoneScene(app, zone)
    for p in zone.puzzles:
        assert cards(scene)[p.title].subtitle.startswith(f"{p.stage.title()} · {p.type.title()}")


def test_a_locked_card_names_the_puzzle_that_unlocks_it(app):
    zone = ZONES[1]
    boss = cards(ZoneScene(app, zone))[zone.puzzles[-1].title]
    assert not boss.enabled and zone.puzzles[-2].title in boss.subtitle


def test_a_next_card_is_found_by_puzzle_not_by_title(app):
    zone = ZONES[1]
    app.store.record(app.profile.id, zone.puzzles[0].id, 3, 4, 0, 0)
    marked = [label for label, card in cards(ZoneScene(app, zone)).items() if card.next_up]
    assert marked == [zone.puzzles[1].title]
