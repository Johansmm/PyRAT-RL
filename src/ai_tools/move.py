__all__ = ["from_index_to_coord", "distance", "move_to_target", "play_action", "update_scores"]

from enum import Enum, auto
from collections import defaultdict


class Moves(Enum):
    nothing = 0
    up = auto()
    right = auto()
    down = auto()
    left = auto()


def from_index_to_coord(pos, maze_width, maze_height):
    """Convert the position from index to coordiantes in a 2D plane

    Example
    -------
    A maze of maze_width = 4 and maze_height = 2 is represented by the following ids:

    ```
    y = 1 | 0    -    1    -    2    -    3
    y = 0 | 4    -    5    -    6    -    7
          |---------------------------------
            |         |         |         |
          x = 0     x = 1     x = 2     x = 3
    ```

    That means:
    >>> assert from_index_to_coord(5, maze_width = 4, maze_height = 2) == (1, 0)

    Parameters
    ----------
    pos : int
        The position
    maze_width : int
        The maze width
    maze_height : int
        The maze height

    Returns
    -------
    Tuple[int, int]
        The coordinates
    """
    assert pos < maze_width * maze_height, f"Invalid position: {pos} is outside of the maze"
    return (pos % maze_width, maze_height - pos // maze_width - 1)


def distance(la, lb):
    """Calculate the distance between two locations

    Parameters
    ----------
    la : Tuple[int, int]
        First location
    lb : Tuple[int, int]
        Second location

    Returns
    -------
    int
        Distance between locations
    """
    ax, ay = la
    bx, by = lb
    return abs(bx - ax) + abs(by - ay)


def move_to_target(location, target, possible_actions):
    """Choose the action that the agent must take to reach the target

    Given that one agent only moves once and can't move diagonally, it suffices to move in
    the direction of the target, moving vertically first and then horizontally

    Parameters
    ----------
    location : Tuple[int, int]
        Current location
    target : Tuple[int, int]
        Coordinates of cheese target
    possible_actions : List[str]
        List of possible actions

    Returns
    -------
    Tuple[int, int]
        The updated location
    """
    if target[1] > location[1]:
        return possible_actions[Moves.up.value]
    if target[1] < location[1]:
        return possible_actions[Moves.down.value]
    if target[0] > location[0]:
        return possible_actions[Moves.right.value]
    if target[0] < location[0]:
        return possible_actions[Moves.left.value]
    # We are in the target !
    return possible_actions[Moves.nothing.value]


def play_action(location, action, possible_actions, maze_width, maze_height):
    """Update an input location (x, y) with the desired action

    Parameters
    ----------
    location : Tuple[int, int]
        Current location
    action : str
        One of `possible_actions`
    possible_actions : List[str]
        List of possible actions.
    maze_width : int
        The maze width
    maze_height : int
        The maze height

    Returns
    -------
    Tuple[int, int]
        The updated location
    """
    id_action = possible_actions.index(action)
    x, y = location
    if id_action == Moves.up.value:
        y = min(y + 1, maze_height - 1)
    elif id_action == Moves.down.value:
        y = max(y - 1, 0)
    elif id_action == Moves.right.value:
        x = min(x + 1, maze_width - 1)
    elif id_action == Moves.left.value:
        x = max(x - 1, 0)
    return (x, y)


def update_scores(player_locations, player_scores, cheeses):
    """Update player scores

    Each player win +1 point iff they are alone on the square with a cheese.
    If several players are in the same square and there is a cheese on it,
    each player gets `1 - (num_players_in_square - 1)/total_players` points.

    Parameters
    ----------
    player_locations : Dict[str, Union[int, Tuple[int, int]]]
        Locations for all players in the game.
    player_scores : Dict[str, float]
        Scores for all players in the game
    cheeses : List[Union[int, Tuple[int, int]]]
        List of remaining cheeses

    Returns
    List[Union[int, Tuple[int, int]]]
        Cheeses that were not consumed
    """
    # Each player in cheese wins 1.0 point
    total_players = len(player_locations)
    num_players_in_targets = defaultdict(lambda: -1 / total_players)
    for player_name, player_position in player_locations.items():
        if player_position in cheeses:
            player_scores[player_name] += 1
            num_players_in_targets[player_position] += 1 / total_players

    # Penalizes players if they obtained the same cheese
    for player_name, player_position in player_locations.items():
        player_scores[player_name] -= num_players_in_targets.get(player_position, 0.0)

    # Remove cheeses
    return [x for x in cheeses if x not in num_players_in_targets]
