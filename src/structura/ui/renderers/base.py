from __future__ import annotations

from dataclasses import dataclass

import pygame


@dataclass
class Target:
    """Something the player can click: a `node` (an element) or a `slot` (an empty place)."""

    kind: str
    key: object
    rect: pygame.Rect


def make_renderer(structure: str, rect: pygame.Rect):
    from .array import ArrayRenderer

    renderers = {"array": ArrayRenderer}
    if structure not in renderers:
        raise NotImplementedError(f"no renderer for {structure} yet")
    return renderers[structure](rect)
