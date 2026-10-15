import json

from structura.persistence import report
from structura.persistence.store import Store
from structura.puzzles.schema import Puzzle, Zone


def zone():
    p = Puzzle(id="z_p1", title="Swap", type="sort", stage="guided", structure="array",
               brief="", goal={"kind": "sorted"}, initial=[2, 1], ops=["swap"])
    return Zone(id="z", name="Test Zone", order=1, structure="array", color=(1, 2, 3), intro="",
                requires=[], map_pos=(0.5, 0.5), lesson=None, puzzles=[p])


def test_store_keeps_best_attempt(tmp_path):
    s = Store(tmp_path / "t.db")
    p = s.create_profile("Ana", "2024-001")
    s.record(p.id, "z_p1", stars=2, moves=3, glitches=1, hints=0)
    s.record(p.id, "z_p1", stars=1, moves=9, glitches=4, hints=2)
    r = s.record(p.id, "z_p1", stars=3, moves=1, glitches=0, hints=0)
    assert (r.stars, r.moves, r.attempts) == (3, 1, 3)


def test_report_signature_detects_edits(tmp_path):
    s = Store(tmp_path / "t.db")
    p = s.create_profile("Ana", "2024-001")
    s.record(p.id, "z_p1", stars=2, moves=2, glitches=0, hints=1)
    path = report.export(p, s.results(p.id), [zone()], folder=tmp_path)
    data = json.loads(path.read_text())
    assert report.verify(data)
    assert data["results"][0]["reference_moves"] == 1
    data["results"][0]["stars"] = 3
    assert not report.verify(data)


def exported_report(tmp_path) -> dict:
    s = Store(tmp_path / "t.db")
    p = s.create_profile("Ana", "2024-001")
    return json.loads(report.export(p, s.results(p.id), [zone()], folder=tmp_path).read_text())


def test_a_report_without_a_text_signature_is_not_verified(tmp_path):
    data = exported_report(tmp_path)
    for signature in (12345, ["abc"], None, "ñandú", json.loads('"\\ud800"')):
        assert not report.verify({**data, "signature": signature}), signature
    del data["signature"]
    assert not report.verify(data)


def test_something_that_is_not_a_report_is_not_verified(tmp_path):
    data = exported_report(tmp_path)
    for other in ([data], "a report", 7, None, {"name": "Ana"}, {**data, "format": "something-else/1"}):
        assert not report.verify(other), other
