"""This program controls a PyRat player by performing manh actions.

More precisely, at each turn, the program follows the cheese closest to it.
"""

import numpy as np

from src.ai_tools import decorator, distance, move_to_target, from_index_to_coord


@decorator.turn
def turn(maze_width, maze_height, name, player_locations, cheese, possible_actions):
    """Return the action that a Manhattan agent would do: go for the nearest cheese

    Parameters
    ----------
    maze_width : int
        Width of the maze in number of cells.
    maze_height : int
        Height of the maze in number of cells.
    name : str
        Name of the player controlled by this function.
    player_locations : Dict[str, int]
        Locations for all players in the game.
    cheese : List[int]
        List of available pieces of cheese in the maze.
    possible_actions : List[str]
        List of possible actions.

    Returns
    -------
    str
        The action taken by the program (one of ``possible_actions``).
    """
    closest_cheese = (-1, -1)
    best_distance = np.inf

    # Compute the nearest cheese
    player_position = from_index_to_coord(player_locations[name], maze_width, maze_height)
    for poc in cheese:
        poc = from_index_to_coord(poc, maze_width, maze_height)
        new_distance = distance(poc, player_position)
        if new_distance < best_distance:
            best_distance = new_distance
            closest_cheese = poc
    return move_to_target(player_position, closest_cheese, possible_actions)
