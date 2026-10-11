"""Progress Reports: signed JSON a student uploads to the class's online classroom.

The signature is an HMAC with a key built into the game. It stops casual
editing of a report in a text editor. It is not proof against a student who
reads the source code, which is acceptable for low-stakes coursework.
"""
from __future__ import annotations

import hashlib
import hmac
import json
from datetime import datetime, timezone
from pathlib import Path

from .. import __version__
from ..puzzles.schema import Zone
from ..puzzles.session import reference_count
from .store import Profile, Result

FORMAT = "structura-progress-report/1"
_KEY = b"structura/bsit/progress-report/v1"


def _sign(body: dict) -> str:
    canonical = json.dumps(body, sort_keys=True, separators=(",", ":")).encode()
    return hmac.new(_KEY, canonical, hashlib.sha256).hexdigest()


def build(profile: Profile, results: dict[str, Result], zones: list[Zone]) -> dict:
    rows = []
    for zone in zones:
        for p in zone.puzzles:
            r = results.get(p.id)
            rows.append({
                "zone": zone.name, "puzzle_id": p.id, "title": p.title, "stage": p.stage,
                "stars": r.stars if r else 0, "moves": r.moves if r else None,
                "reference_moves": reference_count(p), "glitches": r.glitches if r else None,
                "hints": r.hints if r else None, "attempts": r.attempts if r else 0,
                "completed_at": r.completed_at if r else None,
            })
    body = {
        "format": FORMAT,
        "game_version": __version__,
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "student": {"name": profile.name, "student_id": profile.student_id},
        "summary": {
            "puzzles_total": len(rows),
            "puzzles_completed": sum(1 for r in rows if r["stars"] > 0),
            "stars": sum(r["stars"] for r in rows),
            "stars_possible": 3 * len(rows),
        },
        "results": rows,
    }
    return {**body, "signature": _sign(body)}


def verify(report: dict) -> bool:
    body = {k: v for k, v in report.items() if k != "signature"}
    return report.get("format") == FORMAT and hmac.compare_digest(_sign(body), report.get("signature", ""))


def default_folder() -> Path:
    folder = Path.home() / "Documents" / "Structura Reports"
    folder.mkdir(parents=True, exist_ok=True)
    return folder


def export(profile: Profile, results: dict[str, Result], zones: list[Zone], folder: Path | None = None) -> Path:
    report = build(profile, results, zones)
    safe_id = "".join(c for c in profile.student_id if c.isalnum() or c in "-_") or "student"
    stamp = datetime.now().strftime("%Y%m%d-%H%M")
    path = (folder or default_folder()) / f"structura_{safe_id}_{stamp}.json"
    path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    return path
