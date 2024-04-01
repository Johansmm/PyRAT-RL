import pytest

from src.ai_tools import from_index_to_coord, distance, move_to_target
from src.ai_tools.move import Moves


@pytest.mark.parametrize(
    "pos, x, y, exp", [(105, 10, 15, (5, 4)), (4, 2, 3, (0, 0))], ids=["pos1", "pos2"]
)
def test_from_index_to_coord(pos, x, y, exp):
    assert from_index_to_coord(pos, x, y) == exp


def test_from_index_to_coord_ko():
    with pytest.raises(AssertionError, match="outside"):
        from_index_to_coord(pos=100, maze_height=20, maze_width=5)


@pytest.mark.parametrize(
    "x1, x2, exp",
    [[(5, 4), (7, 6), 4], [(4, 4), (4, 4), 0]],
    ids=["diff", "same"],
)
def test_distance(x1, x2, exp):
    assert distance(x1, x2) == exp


@pytest.mark.parametrize(
    "x, target, exp_move",
    [
        [(5, 4), (7, 6), "up"],
        [(5, 4), (6, 2), "down"],
        [(4, 4), (2, 4), "left"],
        [(4, 4), (6, 4), "right"],
        [(4, 4), (4, 4), "nothing"],
    ],
    ids=["up", "down", "left", "right", "nothing"],
)
def test_move_to_target(x, target, exp_move):
    possible_actions = [x.name for x in Moves]
    # Note vertical moves have priority than horizontal ones
    assert move_to_target(x, target, possible_actions) == exp_move
