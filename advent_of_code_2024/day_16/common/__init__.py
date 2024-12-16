"""Common methods for the Day 16"""

import os
import typing as t

# Directions: North (0), East (1), South (2), West (3)
DIRECTIONS = [(-1, 0), (0, 1), (1, 0), (0, -1)]


class Node:
    """Node class."""

    x: int
    y: int
    direction: int
    cost: int
    heuristic: float
    total_cost: float
    parent: t.Optional["Node"]

    def __init__(
        self, x: int, y: int, direction: int, cost: int, heuristic: float
    ):
        self.x = x
        self.y = y
        self.direction = direction
        self.cost = cost
        self.heuristic = heuristic
        self.total_cost = cost + heuristic
        self.parent = None

    def __lt__(self, other: "Node") -> bool:
        return self.total_cost < other.total_cost


def compute_heuristic(
    start: t.Tuple[int, int], end: t.Tuple[int, int], divider: int = 1
) -> float:
    """Compute heuristic using Manhattan distance
    with a divider to encourage exploring more paths.

    Args:
        start (t.Tuple[int, int]): Start position.
        end (t.Tuple[int, int]): End position.
        divider (int, optional): Divider. Defaults to 1.

    Returns:
        float: Heuristic value.
    """
    return (abs(start[0] - end[0]) + abs(start[1] - end[1])) / divider


def parse_maze(
    file_name: str,
    from_file: str,
) -> t.Tuple[t.List[t.List[int]], t.Tuple[int, int], t.Tuple[int, int]]:
    """Initialize maze using configuration from a txt file.

    Args:
        file_name (str): Input file name.
        from_file (str): File from where the method is called.

    Returns:
        t.List[t.List[int]]: The parsed maze.
    """
    absolute_path_to_file: str = os.path.realpath(
        os.path.join(os.getcwd(), os.path.dirname(from_file), file_name)
    )
    raw_maze: t.List[t.List[str]] = []
    with open(absolute_path_to_file, "r", encoding="utf-8") as file_descriptor:
        raw_maze = [
            list(row) for row in file_descriptor.read().strip().split("\n")
        ]

    maze: t.List[t.List[int]] = [
        [0 for _ in range(len(raw_maze[0]))] for _ in range(len(raw_maze))
    ]
    start: t.Tuple[int, int] | None = None
    end: t.Tuple[int, int] | None = None
    for y, row in enumerate(raw_maze):
        for x, cell in enumerate(row):
            if cell == "S":
                start = (x, y)
                maze[y][x] = 0
            elif cell == "E":
                end = (x, y)
                maze[y][x] = 0
            elif cell == "#":
                maze[y][x] = 1

    if start is None or end is None:
        raise ValueError("Start or end position not found in the maze.")

    return maze, start, end
