__all__ = ["from_index_to_coord", "distance", "move_to_target"]

from enum import Enum, auto


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