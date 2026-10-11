"""Every shipped Zone must load, and every Puzzle in it must be solvable by its
own Reference Solution (ADR 0001)."""
import copy
import random

import pytest

from structura.codemirror import library
from structura.models import complexity, make
from structura.puzzles.hints import lint
from structura.puzzles.schema import ContentError, load_all, load_zone
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


def legal_moves(s: PuzzleSession):
    for m in s.model.candidate_moves(s.tray_next):
        if m.op in s.puzzle.ops and not s.model.why_illegal(m):
            yield m


@pytest.mark.parametrize("puzzle", [p for p in PUZZLES if p.disruptions], ids=lambda p: p.id)
def test_disruptions_never_make_a_winnable_puzzle_unwinnable(puzzle):
    """Spec story 35. Winnability is measured between the player's Move and the
    Disruption, so the player's own dead ends aren't blamed on the Disruption."""
    for seed in range(40):
        rng = random.Random(seed)
        s = PuzzleSession(puzzle)
        while len(s.fired) < len(puzzle.disruptions) and s.moves < 12:
            moves = list(legal_moves(s))
            if s.done or not moves:
                break
            move = rng.choice(moves)
            calm = copy.deepcopy(s)
            calm.fired = frozenset(range(len(puzzle.disruptions)))
            calm.try_move(move)
            out = s.try_move(move)
            if out.disruption and not calm.dead_end:
                assert not s.dead_end, f"seed {seed}: {out.disruption!r} after {move} left no way to finish"


def test_linked_marshes_follow_the_array_plains():
    z2 = next(z for z in ZONES if z.id == "z2")
    assert z2.structure == "linked_list" and z2.requires == ["z1"]
    assert z2.puzzles[-1].stage == "boss" and z2.puzzles[-1].disruptions
    assert all(p.code.startswith("ll_") for p in z2.puzzles)


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
        if beat.structure:
            model = make(beat.structure, beat.initial)
        model.run(beat.do)
        if beat.code:
            assert library.load(beat.code, "java") is not None


def test_queue_canals_follow_the_stack_towers():
    z4 = next(z for z in ZONES if z.id == "z4")
    assert z4.name == "The Queue Canals" and z4.structure == "queue" and z4.requires == ["z3"]
    assert z4.puzzles[-1].stage == "boss" and z4.puzzles[-1].disruptions
    assert any(p.goal["kind"] == "quiz" for p in z4.puzzles)


def test_nexus_alpha_follows_the_queue_canals():
    nx = next(z for z in ZONES if z.id == "nexus_alpha")
    assert nx.name == "Nexus Alpha" and nx.is_nexus and nx.requires == ["z4"]
    assert ZONES.index(nx) == ZONES.index(next(z for z in ZONES if z.id == "z4")) + 1
    assert sum(p.type == "select" for p in nx.puzzles) >= 4
    assert any(p.structure == "queue" and p.goal["kind"] == "quiz" for p in nx.puzzles), "mixed-structure quiz"
    boss = nx.puzzles[-1]
    assert boss.stage == "boss" and boss.structure == "array" and len(boss.disruptions) == 2


@pytest.mark.parametrize("puzzle", [p for p in PUZZLES if p.goal["kind"] == "select"], ids=lambda p: p.id)
def test_every_select_scenario_has_a_unique_best_answer(puzzle):
    goal = PuzzleSession(puzzle).goal
    ranked = complexity.ranking(puzzle.goal["choices"], puzzle.goal["scenario"])
    assert puzzle.goal["choices"][goal.correct] == ranked[0]
    first, second = ranked[:2]
    key = lambda s: (complexity.cost(s, puzzle.goal["scenario"]), len(complexity.TABLE[s]))
    assert key(first) < key(second)


def test_a_lesson_beat_with_an_unknown_big_o_operation_is_rejected(tmp_path):
    path = tmp_path / "z.toml"
    path.write_text('''[zone]
id = "zx"
name = "X"
order = 1
structure = "array"

[lesson]
initial = []

[[lesson.beat]]
say = "Compare."
big_o = ["teleport"]
''', encoding="utf-8")
    with pytest.raises(ContentError, match="teleport"):
        load_zone(path)
