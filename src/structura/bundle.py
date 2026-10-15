"""Where the game's data folders are, whether it runs from source, installed, or as the Windows build."""
from __future__ import annotations

import sys
from dataclasses import dataclass
from pathlib import Path

PACKAGE = Path(__file__).resolve().parent
REPO = PACKAGE.parents[1]


@dataclass(frozen=True)
class Folder:
    dest: str           # where the Windows build puts it
    in_package: bool    # inside the structura package, so an installed copy has it too

    def source(self) -> Path:
        return (PACKAGE.parent if self.in_package else REPO) / self.dest


ZONES = Folder("content/zones", in_package=False)
SNIPPETS = Folder("structura/codemirror/snippets", in_package=True)
FOLDERS = (ZONES, SNIPPETS)


def locate(folder: Folder) -> Path:
    root = getattr(sys, "_MEIPASS", None)
    return Path(root) / folder.dest if root else folder.source()


def pyinstaller_datas() -> list[tuple[str, str]]:
    """What structura.spec bundles: (folder on disk, where it goes in the build)."""
    return [(str(f.source()), f.dest) for f in FOLDERS]
