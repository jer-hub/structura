"""The click contract: how each Move becomes the clicks a player makes.

Shared by every test that plays the game through real mouse events. Each
structure registers two things:

  * a player, turning one Move into clicks on renderer targets and buttons;
  * the targets its renderer promises for a model, as (kind, key) pairs.

A new Zone adds its structure here instead of copying the helper.
"""
import pygame

from structura.models import Move

PLAYERS = {}
PROMISED_TARGETS = {}


def player(structure):
    def register(fn):
        PLAYERS[structure] = fn
        return fn
    return register


def promised_targets(structure):
    def register(fn):
        PROMISED_TARGETS[structure] = fn
        return fn
    return register


# ---- acting like a player ---------------------------------------------------
def click_at(app, pos):
    app.handle(pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=1, pos=pos))
    app.handle(pygame.event.Event(pygame.MOUSEBUTTONUP, button=1, pos=pos))
    app.update(0.01)
    app.draw()


def button(app, label):
    matches = [b for b in app.scene.buttons if b.label == label]
    assert matches, f"no button {label!r} on {type(app.scene).__name__}: {[b.label for b in app.scene.buttons]}"
    return matches[0]


def click(app, label):
    b = button(app, label)
    assert b.enabled, f"button {label!r} is disabled"
    click_at(app, b.rect.center)


def settle(app):
    for _ in range(40):
        app.update(0.25)
    app.draw()


def target(app, kind, key):
    for t in app.scene.renderer.targets():
        if t.kind == kind and t.key == key:
            return t.rect.center
    raise AssertionError(f"no {kind} target {key!r}")


def play(app, move: Move):
    """Perform one Move the way a player would, then let the animation finish."""
    structure = app.scene.session.puzzle.structure
    assert structure in PLAYERS, f"no click contract for {structure!r}"
    PLAYERS[structure](app, move)
    settle(app)


# ---- array ---------------------------------------------------------------------
@player("array")
def play_array(app, move: Move):
    if move.op == "visit":
        click_at(app, target(app, "node", move.args[0]))
    elif move.op == "insert":
        click_at(app, target(app, "slot", move.args[0]))
    elif move.op == "swap":
        click_at(app, target(app, "node", move.args[0]))
        click_at(app, target(app, "node", move.args[1]))
        click(app, "Swap")
    else:
        raise AssertionError(move)


@promised_targets("array")
def array_targets(model, show_slots):
    n = len(model.values())
    nodes = {("node", i) for i in range(n)}
    slots = {("slot", i) for i in range(n + 1)} if show_slots else set()
    return nodes | slots
