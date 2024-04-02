import pytest

from src.ai_tools import from_index_to_coord, distance, move_to_target, play_action, update_scores
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


@pytest.mark.parametrize(
    "location, action, exp_location",
    [
        [(5, 4), "up", (5, 5)],
        [(5, 4), "down", (5, 3)],
        [(4, 4), "right", (5, 4)],
        [(4, 4), "left", (3, 4)],
        [(4, 4), "nothing", (4, 4)],
        [(9, 9), "up", (9, 9)],
        [(9, 0), "down", (9, 0)],
        [(9, 9), "right", (9, 9)],
        [(0, 9), "left", (0, 9)],
    ],
    ids=["up", "down", "right", "left", "nothing", "uclip", "dclip", "rclip", "lclip"],
)
def test_play_action(location, action, exp_location):
    possible_actions = [x.name for x in Moves]
    new_location = play_action(location, action, possible_actions, maze_height=10, maze_width=10)
    assert new_location == exp_location


@pytest.mark.parametrize(
    "locations, scores, cheeses, final_scores, exp_remaining_cheeses",
    [
        ((5, 4), (0.0, 5.0), [4, 1], (0.0, 6.0), [1]),
        (((1, 1), (1, 5), (1, 5)), (0.5, 1 / 3, 4 / 3), [(1, 1), (1, 5)], (1.5, 1.0, 2.0), []),
        ((2, 2, 3, 4), (0.5, 0.75, 1.0, 0.0), [2, 4, 1], (1.25, 1.5, 1.0, 1.0), [1]),
    ],
    ids=["2-players", "3-players", "4-players"],
)
def test_update_scores(locations, scores, cheeses, final_scores, exp_remaining_cheeses):
    player_locations = {f"player_{key}": x for key, x in enumerate(locations)}
    player_scores = {f"player_{key}": x for key, x in enumerate(scores)}
    final_scores = {f"player_{key}": x for key, x in enumerate(final_scores)}
    remaining_cheeses = update_scores(player_locations, player_scores, cheeses)
    assert remaining_cheeses == exp_remaining_cheeses
