"""Plays the thin slice headlessly by sending real pygame mouse and text events:
Profile -> Zone Map -> Z1 Lesson -> every Z1 Puzzle -> Results -> Progress Report."""
import json
import os

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")

import pygame
import pytest

from clicks import button, click, click_at, play, settle, target
from structura.models import Move
from structura.persistence import report
from structura.persistence.store import Store
from structura.puzzles.schema import load_all
from structura.puzzles.session import reference_moves
from structura.ui.app import App
from structura.ui.scenes.lesson import LessonScene
from structura.ui.scenes.profiles import ProfileScene
from structura.ui.scenes.puzzle import PuzzleScene
from structura.ui.scenes.results import ResultsScene
from structura.ui.scenes.zone import ZoneScene
from structura.ui.scenes.zone_map import ZoneMapScene


def type_into(app, field_label, text):
    field = next(f for f in app.scene.fields if f.label == field_label)
    click_at(app, field.rect.center)
    app.handle(pygame.event.Event(pygame.TEXTINPUT, text=text))


# ---- fixtures -------------------------------------------------------------
@pytest.fixture
def app(tmp_path):
    pygame.init()
    a = App(Store(tmp_path / "t.db"), load_all(), screen=pygame.display.set_mode((1280, 720)),
            report_dir=tmp_path)
    a.draw()
    yield a
    a.store.close()


def new_profile(app, name="Ana Cruz", sid="2024-0001", language="Java"):
    assert isinstance(app.scene, ProfileScene)
    click(app, "New Profile")
    type_into(app, "Name", name)
    type_into(app, "Student ID", sid)
    click(app, language)
    click(app, "Create")


# ---- tests ----------------------------------------------------------------
def test_profile_requires_name_and_id(app):
    click(app, "New Profile")
    type_into(app, "Name", "Ana")
    click(app, "Create")
    assert isinstance(app.scene, ProfileScene)
    assert "required" in app.scene.message


def test_full_slice(app, tmp_path):
    new_profile(app)
    assert isinstance(app.scene, ZoneMapScene)
    assert app.profile.language == "java"

    click(app, "The Array Plains")
    assert isinstance(app.scene, ZoneScene)
    # Puzzles unlock in order.
    assert not button(app, "Bubbling Up").enabled

    click(app, "Lesson")
    assert isinstance(app.scene, LessonScene)
    while not any(b.label == "Finish Lesson" for b in app.scene.buttons):
        click(app, "Next")
        settle(app)
    assert app.scene.code_panel.snippet.language == "java"
    click(app, "Finish Lesson")
    assert isinstance(app.scene, ZoneScene)

    zone = app.zones[0]
    for i, puzzle in enumerate(zone.puzzles):
        click(app, puzzle.title)
        scene = app.scene
        assert isinstance(scene, PuzzleScene) and scene.session.puzzle.id == puzzle.id
        for move in reference_moves(puzzle):
            play(app, move)
        assert scene.session.done
        click(app, "See Results")
        assert isinstance(app.scene, ResultsScene)
        assert app.scene.stars == 3
        click(app, "Back to Zone")

    results = app.store.results(app.profile.id)
    assert {p.id for p in zone.puzzles} <= set(results)

    click(app, "Zone Map")
    click(app, "Export Progress Report")
    files = list(tmp_path.glob("structura_2024-0001_*.json"))
    assert len(files) == 1
    data = json.loads(files[0].read_text())
    assert report.verify(data) and data["summary"]["puzzles_completed"] == len(zone.puzzles)
    assert str(files[0]) in app.scene.message


def test_glitch_hint_and_undo(app):
    new_profile(app)
    puzzle = app.zones[0].puzzles[2]           # Bubbling Up: strict bubble sort
    app.open_puzzle(app.zones[0], puzzle)
    scene = app.scene
    play_wrong = Move.of("swap", 0, 4)
    click_at(app, target(app, "node", 0))
    click_at(app, target(app, "node", 4))
    click(app, "Swap")
    assert scene.session.glitches == 1 and "neighbours" in scene.message

    click(app, "Hint")
    click(app, "Hint")
    click(app, "Hint")
    assert scene.session.hint_tier == 3 and scene.message.startswith("Next:")
    assert scene.hint_move == scene.session.expected()

    play(app, scene.session.expected())
    moves_before = scene.session.moves
    click(app, "Undo")
    assert scene.session.moves == moves_before
    assert scene.session.model.values() == puzzle.initial
    assert play_wrong != scene.session.expected()


def test_disruption_is_announced(app):
    new_profile(app)
    boss = app.zones[0].puzzles[-1]
    app.open_puzzle(app.zones[0], boss)
    announced = []
    for move in reference_moves(boss):
        play(app, move)
        announced.append(app.scene.message)
    assert any("Shuffler flips" in m for m in announced)


# ---- The Linked Marshes ---------------------------------------------------
def clear_zone(app, zone):
    for p in zone.puzzles:
        app.store.record(app.profile.id, p.id, 3, 1, 0, 0)


def test_linked_marshes_play_through(app):
    new_profile(app)
    z1, z2 = app.zones[0], app.zones[1]
    assert z2.name == "The Linked Marshes"
    clear_zone(app, z1)
    app.open_map()
    click(app, "The Linked Marshes")
    assert isinstance(app.scene, ZoneScene)

    click(app, "Lesson")
    while not any(b.label == "Finish Lesson" for b in app.scene.buttons):
        click(app, "Next")
        settle(app)
    click(app, "Finish Lesson")

    for puzzle in z2.puzzles:
        click(app, puzzle.title)
        scene = app.scene
        assert isinstance(scene, PuzzleScene) and scene.session.puzzle.id == puzzle.id
        for move in reference_moves(puzzle):
            play(app, move)
        assert scene.session.done, puzzle.id
        click(app, "See Results")
        assert app.scene.stars == 3, puzzle.id
        click(app, "Back to Zone")

    assert {p.id for p in z2.puzzles} <= set(app.store.results(app.profile.id))


def test_delete_needs_exactly_one_selected_node(app):
    new_profile(app)
    z2 = app.zones[1]
    app.open_puzzle(z2, next(p for p in z2.puzzles if p.id == "z2_p4"))     # Cut the Rot
    assert not button(app, "Delete").enabled
    click_at(app, target(app, "node", 2))
    assert button(app, "Delete").enabled and app.scene.selected == [2]
    click_at(app, target(app, "node", 3))
    assert app.scene.selected == [3], "selecting another node moves the selection"
    click_at(app, target(app, "node", 3))
    assert not button(app, "Delete").enabled


def test_dead_end_prompts_undo(app):
    new_profile(app)
    z2 = app.zones[1]
    app.open_puzzle(z2, z2.puzzles[-1])                                     # The Marsh Hydra
    scene = app.scene
    play(app, Move.of("delete", 0))                                          # 1 can't come back
    assert scene.session.dead_end
    assert "Undo" in scene.message and "Hydra" in scene.message, "the Disruption is still announced"
    click(app, "Hint")
    click(app, "Hint")
    click(app, "Hint")
    assert scene.message.startswith("Undo") and scene.hint_move is None
    click(app, "Undo")
    assert not scene.session.dead_end
