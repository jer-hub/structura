"""The Windows build: what it bundles is what the game looks up, and player data stays outside it."""
import shutil
import sys

import pytest

from structura import bundle
from structura.codemirror import library
from structura.persistence import report
from structura.persistence.store import Store
from structura.puzzles.schema import load_all

@pytest.fixture
def frozen(tmp_path, monkeypatch):
    """Pretend to be the packaged game, unpacked into a folder holding exactly what the build bundles."""
    root = tmp_path / "Structura build"
    for source, dest in bundle.pyinstaller_datas():
        shutil.copytree(source, root / dest)
    monkeypatch.setattr(sys, "_MEIPASS", str(root), raising=False)
    library.load.cache_clear()
    yield root
    library.load.cache_clear()


def test_the_build_bundles_every_zone(frozen):
    from_bundle = load_all()
    assert [z.id for z in from_bundle] == [z.id for z in load_all(bundle.ZONES.source())]
    assert from_bundle


def test_the_build_file_bundles_what_the_game_looks_up():
    spec = (bundle.REPO / "structura.spec").read_text(encoding="utf-8")
    assert "datas=bundle.pyinstaller_datas()" in spec


def test_the_build_bundles_the_code_mirror_snippets(frozen):
    for language in ("python", "java"):
        snippet = library.load("binary_search", language)
        assert snippet and snippet.lines, language


def test_an_installed_copy_finds_its_snippets_without_the_repository(monkeypatch, tmp_path):
    monkeypatch.setattr(bundle, "REPO", tmp_path / "no repository here")
    library.load.cache_clear()
    try:
        assert library.load("binary_search", "python")
    finally:
        library.load.cache_clear()


def test_lookup_reads_from_the_bundle_not_the_source_tree(frozen):
    shutil.rmtree(frozen / bundle.ZONES.dest)
    (frozen / bundle.ZONES.dest).mkdir()
    assert load_all() == []


def test_player_data_and_reports_are_written_outside_the_build(frozen, tmp_path, monkeypatch):
    home = tmp_path / "home"
    monkeypatch.delenv("STRUCTURA_HOME", raising=False)
    monkeypatch.setenv("APPDATA", str(home / "AppData" / "Roaming"))
    monkeypatch.setenv("USERPROFILE", str(home))
    monkeypatch.setenv("HOME", str(home))
    store = Store()
    profile = store.create_profile("Ana Peña", "2024-0001")
    path = report.export(profile, store.results(profile.id), load_all())
    store.close()
    assert store.path.is_relative_to(home / "AppData" / "Roaming" / "Structura")
    assert path.is_relative_to(home / "Documents" / "Structura Reports")
    assert not any(p.is_relative_to(frozen) for p in (store.path, path))
