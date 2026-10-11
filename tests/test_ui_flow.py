"""Plays the thin slice headlessly by sending real pygame mouse and text events:
Profile -> Zone Map -> Z1 Lesson -> every Z1 Puzzle -> Results -> Progress Report."""
import json
import os

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")

import pygame
import pytest

from clicks import button, click, click_at, labels, play, settle, target
from structura.models import Move
from structura.persistence import report
from structura.persistence.store import Store
from structura.puzzles.schema import load_all
from structura.puzzles.session import reference_moves
from structura.ui.app import App
from structura.ui.renderers import RENDERERS
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


# ---- The Stack Towers -------------------------------------------------------
def test_stack_towers_play_through(app):
    new_profile(app)
    z1, z2, z3 = app.zones[0], app.zones[1], app.zones[2]
    assert z3.name == "The Stack Towers"
    clear_zone(app, z1)
    app.open_map()
    assert not button(app, "The Stack Towers").enabled, "locked until The Linked Marshes is cleared"
    clear_zone(app, z2)
    app.open_map()
    click(app, "The Stack Towers")

    click(app, "Lesson")
    while not any(b.label == "Finish Lesson" for b in app.scene.buttons):
        click(app, "Next")
        settle(app)
    click(app, "Finish Lesson")

    quizzes = 0
    for puzzle in z3.puzzles:
        click(app, puzzle.title)
        scene = app.scene
        quizzes += scene.session.goal.options is not None
        for move in reference_moves(puzzle):
            play(app, move)
        assert scene.session.done, puzzle.id
        click(app, "See Results")
        assert app.scene.stars == 3, puzzle.id
        click(app, "Back to Zone")
    assert quizzes >= 1
    assert {p.id for p in z3.puzzles} <= set(app.store.results(app.profile.id))


def test_push_and_pop_buttons_follow_the_ops(app):
    new_profile(app)
    z3 = app.zones[2]
    by_id = {p.id: p for p in z3.puzzles}
    app.open_puzzle(z3, by_id["z3_p1"])                # Stack the Blocks: push only
    assert "Push" in labels(app) and "Pop" not in labels(app)

    app.open_puzzle(z3, by_id["z3_p3"])                # Mirror Spell: push and pop
    assert button(app, "Push").enabled and not button(app, "Pop").enabled, "nothing to pop yet"
    click(app, "Push")
    assert button(app, "Pop").enabled
    assert "Swap" not in labels(app) and "Delete" not in labels(app)


def test_quiz_wrong_then_right_answer(app):
    new_profile(app)
    z3 = app.zones[2]
    quiz = next(p for p in z3.puzzles if p.id == "z3_p2")
    app.open_puzzle(z3, quiz)
    scene = app.scene
    options, right = scene.session.goal.options, scene.session.goal.correct
    assert all(o in labels(app) for o in options)
    assert "Push" not in labels(app) and "Pop" not in labels(app)
    wrong = next(o for i, o in enumerate(options) if i != right)
    click(app, wrong)
    assert scene.session.glitches == 1 and "LIFO" in scene.message and not scene.session.done
    click(app, options[right])
    assert scene.session.done


# ---- The Queue Canals -------------------------------------------------------
def test_queue_canals_play_through(app):
    new_profile(app)
    z1, z2, z3, z4 = app.zones[:4]
    assert z4.name == "The Queue Canals"
    for z in (z1, z2):
        clear_zone(app, z)
    app.open_map()
    assert not button(app, "The Queue Canals").enabled, "locked until The Stack Towers is cleared"
    clear_zone(app, z3)
    app.open_map()
    click(app, "The Queue Canals")

    click(app, "Lesson")
    while not any(b.label == "Finish Lesson" for b in app.scene.buttons):
        click(app, "Next")
        settle(app)
    click(app, "Finish Lesson")

    quizzes = 0
    for puzzle in z4.puzzles:
        click(app, puzzle.title)
        scene = app.scene
        quizzes += scene.session.goal.options is not None
        for move in reference_moves(puzzle):
            play(app, move)
        assert scene.session.done, puzzle.id
        click(app, "See Results")
        assert app.scene.stars == 3, puzzle.id
        click(app, "Back to Zone")
    assert quizzes >= 1
    assert {p.id for p in z4.puzzles} <= set(app.store.results(app.profile.id))


def test_enqueue_and_dequeue_buttons_follow_the_ops(app):
    new_profile(app)
    z4 = app.zones[3]
    by_id = {p.id: p for p in z4.puzzles}
    app.open_puzzle(z4, by_id["z4_p1"])                # Launch the Boats: enqueue only
    assert "Enqueue" in labels(app) and "Dequeue" not in labels(app)

    app.open_puzzle(z4, by_id["z4_p3"])                # Same Order Out: enqueue and dequeue
    assert button(app, "Enqueue").enabled and not button(app, "Dequeue").enabled, "nothing to dequeue yet"
    click(app, "Enqueue")
    assert button(app, "Dequeue").enabled
    assert "Push" not in labels(app) and "Pop" not in labels(app)


def test_queue_quiz_wrong_answer_explains_fifo(app):
    new_profile(app)
    z4 = app.zones[3]
    app.open_puzzle(z4, next(p for p in z4.puzzles if p.id == "z4_p2"))
    scene = app.scene
    options, right = scene.session.goal.options, scene.session.goal.correct
    click(app, next(o for i, o in enumerate(options) if i != right))
    assert scene.session.glitches == 1 and "FIFO" in scene.message and not scene.session.done
    click(app, options[right])
    assert scene.session.done


def test_the_lock_keeper_sweeps_the_front_boat_to_the_output(app):
    new_profile(app)
    z4 = app.zones[3]
    boss = z4.puzzles[-1]
    app.open_puzzle(z4, boss)
    scene = app.scene
    front = scene.session.model.front()
    moves = reference_moves(boss)
    for move in moves[:boss.disruptions[0].after]:
        play(app, move)
    assert "Lock Keeper" in scene.message
    assert front in scene.session.model.out
    assert front in [v for v, _ in scene.renderer.output()], "the swept boat lands on the Output row"


# ---- Nexus Alpha ------------------------------------------------------------
def nexus(app):
    return next(z for z in app.zones if z.id == "nexus_alpha")


def test_nexus_alpha_play_through(app):
    new_profile(app)
    nx = nexus(app)
    for z in app.zones[:3]:
        clear_zone(app, z)
    app.open_map()
    assert not button(app, "Nexus Alpha").enabled, "locked until The Queue Canals is cleared"
    clear_zone(app, app.zones[3])
    app.open_map()
    click(app, "Nexus Alpha")

    click(app, "Lesson")
    while not any(b.label == "Finish Lesson" for b in app.scene.buttons):
        click(app, "Next")
        settle(app)
    click(app, "Finish Lesson")

    said = []
    for puzzle in nx.puzzles:
        click(app, puzzle.title)
        scene = app.scene
        assert type(scene.renderer) is RENDERERS[puzzle.structure], "each Puzzle's own structure, not the Zone's"
        for move in reference_moves(puzzle):
            play(app, move)
            said.append(scene.message)
        assert scene.session.done, puzzle.id
        click(app, "See Results")
        assert app.scene.stars == 3, puzzle.id
        click(app, "Back to Zone")
    assert all(d.say in said for d in nx.puzzles[-1].disruptions), "both of the Serpent's strikes are shown"
    assert {p.id for p in nx.puzzles} <= set(app.store.results(app.profile.id))


@pytest.mark.parametrize("language", ["Java", "Python"])
def test_select_puzzle_offers_structures_and_shows_their_big_o(app, language):
    new_profile(app, language=language)
    nx = nexus(app)
    puzzle = next(p for p in nx.puzzles if p.id == "nx_p3")          # Seat Numbers
    app.open_puzzle(nx, puzzle)
    scene = app.scene
    options = ["Array", "Linked List", "Stack", "Queue"]
    assert scene.session.goal.options == options and all(o in labels(app) for o in options)
    head, rows = scene.code_panel.table
    assert "read the item at a position" in head
    assert [name for name, _ in rows] == options
    app.draw()

    click(app, "Linked List")
    assert scene.session.glitches == 1 and not scene.session.done
    assert "Linked List takes O(n)" in scene.message and "Array takes O(1)" in scene.message
    assert scene.code_panel.table is not None, "the table stays up after a Glitch"
    click(app, "Array")
    assert scene.session.done


def test_a_regular_puzzle_shows_code_not_a_table(app):
    new_profile(app)
    nx = nexus(app)
    app.open_puzzle(nx, nx.puzzles[-1])
    assert app.scene.code_panel.table is None and app.scene.code_panel.snippet is not None
