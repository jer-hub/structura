"""Every shipped Zone must load, and every Puzzle in it must be solvable by its
own Reference Solution (ADR 0001)."""
import pytest

from structura.codemirror import library
from structura.models import make
from structura.puzzles.hints import lint
from structura.puzzles.schema import load_all
from structura.puzzles.session import PuzzleSession, reference_moves

ZONES = load_all()
PUZZLES = [p for z in ZONES for p in z.puzzles]


def test_array_plains_is_the_first_zone():
    z1 = ZONES[0]
    assert z1.id == "z1" and z1.structure == "array" and z1.requires == []
    assert z1.lesson is not None and len(z1.lesson.beats) >= 3
    assert 3 <= len(z1.puzzles) <= 4
    assert z1.puzzles[-1].stage == "boss"
    assert {p.type for p in z1.puzzles} >= {"trace", "build", "sort"}


@pytest.mark.parametrize("puzzle", PUZZLES, ids=lambda p: p.id)
def test_reference_solution_finishes(puzzle):
    moves = reference_moves(puzzle)
    assert moves, "a Puzzle that is already solved teaches nothing"


@pytest.mark.parametrize("puzzle", PUZZLES, ids=lambda p: p.id)
def test_disruptions_actually_fire(puzzle):
    if not puzzle.disruptions:
        return
    s = PuzzleSession(puzzle)
    fired = 0
    for m in reference_moves(puzzle):
        fired += bool(s.try_move(m).disruption)
    assert fired == len(puzzle.disruptions), "a Disruption is scheduled after the Puzzle would end"


@pytest.mark.parametrize("puzzle", PUZZLES, ids=lambda p: p.id)
def test_written_hints_pass_lint(puzzle):
    assert len(puzzle.hints) == 2
    for h in puzzle.hints:
        assert lint(h) == [], h


@pytest.mark.parametrize("puzzle", PUZZLES, ids=lambda p: p.id)
def test_code_mirror_snippet_exists_in_both_languages(puzzle):
    if puzzle.code:
        for lang in library.LANGUAGES:
            assert library.load(puzzle.code, lang) is not None, (puzzle.code, lang)


@pytest.mark.parametrize("zone", ZONES, ids=lambda z: z.id)
def test_lesson_scripts_run(zone):
    model = make(zone.lesson.structure, zone.lesson.initial)
    for beat in zone.lesson.beats:
        model.run(beat.do)
        if beat.code:
            assert library.load(beat.code, "java") is not None
