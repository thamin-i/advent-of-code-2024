"""Common methods for the Day 18"""

import os
import typing as t
from collections import deque


class BFSSolver:
    """Breadth-first search solver."""

    maze: t.List[t.List[str]]
    empty_cell: str
    walked_cell: str

    def __init__(
        self,
        maze: t.List[t.List[str]],
        empty_cell: str = ".",
        walked_cell: str = "O",
    ) -> None:
        self.maze = maze
        self.empty_cell = empty_cell
        self.walked_cell = walked_cell

    def __is_valid_position(self, position_x: int, position_y: int) -> bool:
        """Check if the position is valid.

        Args:
            position_x (int): X position.
            position_y (int): Y position.

        Returns:
            bool: True if the position is valid, False otherwise.
        """
        return (
            0 <= position_x < len(self.maze[0])
            and 0 <= position_y < len(self.maze)
            and self.maze[position_y][position_x] == self.empty_cell
        )

    def __get_adjacent_positions(
        self,
        position_x: int,
        position_y: int,
    ) -> t.List[t.Tuple[int, int]]:
        """Get the adjacent positions of the given position.

        Args:
            position_x (int): X position.
            position_y (int): Y position.

        Returns:
            t.List[t.Tuple[int, int]]: The adjacent positions.
        """
        return [
            (position_x - 1, position_y),
            (position_x + 1, position_y),
            (position_x, position_y - 1),
            (position_x, position_y + 1),
        ]

    def compute_shortest_path(
        self,
        start_position: t.Tuple[int, int],
        end_position: t.Tuple[int, int],
        print_maze: bool = False,
    ) -> t.List[t.Tuple[int, int]] | None:
        """Solve the maze using BFS.

        Args:
            start_position (t.Tuple[int, int]):
                Start position.
            end_position (t.Tuple[int, int]):
                End position.
            print_maze (bool):
                Print the maze with the path. Defaults to False.

        Returns:
            t.List[t.Tuple[int, int]]:
                The shortest path from the start to the end position.
        """
        visited: t.Set[t.Tuple[int, int]] = set()
        queue: t.Deque[t.Tuple[int, int]] = deque([start_position])
        parent: t.Dict[t.Tuple[int, int], t.Tuple[int, int] | None] = {}

        visited.add(start_position)
        parent[start_position] = None

        while queue:
            current_position: t.Tuple[int, int] | None = queue.popleft()
            if current_position is None:
                raise ValueError("Current position is None.")

            if current_position == end_position:
                path: t.List[t.Tuple[int, int]] = []
                while current_position:
                    path.append(current_position)
                    current_position = parent[current_position]
                if print_maze:
                    self.print_maze(path)
                return path[::-1]

            for adjacent_position in self.__get_adjacent_positions(
                position_x=current_position[0],
                position_y=current_position[1],
            ):
                if (
                    adjacent_position not in visited
                    and self.__is_valid_position(
                        position_x=adjacent_position[0],
                        position_y=adjacent_position[1],
                    )
                ):
                    queue.append(adjacent_position)
                    visited.add(adjacent_position)
                    parent[adjacent_position] = current_position

        return None

    def compute_minimum_steps(
        self,
        start_position: t.Tuple[int, int],
        end_position: t.Tuple[int, int],
        print_maze: bool = False,
    ) -> int:
        """Find the minimum steps from the start to the end position.

        Args:
            start_position (t.Tuple[int, int]): Start position.
            end_position (t.Tuple[int, int]): End position.
            print_maze (bool): Print the maze with the path. Defaults to False.

        Returns:
            int: The minimum steps from the start to the end position.
        """
        shortest_path: t.List[t.Tuple[int, int]] | None = (
            self.compute_shortest_path(
                start_position=start_position,
                end_position=end_position,
                print_maze=print_maze,
            )
        )
        return len(shortest_path) - 1 if shortest_path is not None else -1

    def print_maze(
        self,
        path: t.List[t.Tuple[int, int]] | None = None,
    ) -> None:
        """Print the path in the maze.

        Args:
            path (t.List[t.Tuple[int, int]] | None):
                The path to print in the maze.
                Defaults to None.
        """
        print("> Maze:")
        for position_y, row in enumerate(self.maze):
            for position_x, cell in enumerate(row):
                if path is not None and (position_x, position_y) in path:
                    print(self.walked_cell, end="")
                else:
                    print(cell, end="")
            print()
        print()


def corrupt_memory_space(
    memory_space: t.List[t.List[str]],
    bytes_positions: t.List[t.Tuple[int, int]],
    max_bytes: int | None = None,
) -> t.List[t.List[str]]:
    """Corrupt the memory space with the given bytes positions.

    Args:
        memory_space (t.List[t.List[str]]):
            Memory space to corrupt.
        bytes_positions (t.List[t.Tuple[int, int]]):
            Bytes positions to corrupt the memory space.
        max_bytes (int | None):
            Maximum number of bytes to corrupt the memory space.

    Returns:
        t.List[t.List[str]]: The corrupted memory space.
    """
    max_bytes = max_bytes if max_bytes is not None else len(bytes_positions)
    for position_x, position_y in bytes_positions[:max_bytes]:
        if position_x < len(memory_space[0]) and position_y < len(memory_space):
            memory_space[position_y][position_x] = "#"

    return memory_space


def generate_memory_space(width: int, height: int) -> t.List[t.List[str]]:
    """Generate a memory space with the given width and height.

    Args:
        width (int): Width of the memory space.
        height (int): Height of the memory space.

    Returns:
        t.List[t.List[str]]: The generated memory space.
    """
    return [["." for _ in range(width + 1)] for _ in range(height + 1)]


def read_bytes_positions(
    file_name: str,
    from_file: str,
) -> t.List[t.Tuple[int, int]]:
    """Read list of bytes positions from a txt file.

    Args:
        file_name (str): Input file name.
        from_file (str): File from where the method is called.

    Returns:
        t.List[t.Tuple[int, int]]: The list of bytes positions.
    """
    absolute_path_to_file: str = os.path.realpath(
        os.path.join(os.getcwd(), os.path.dirname(from_file), file_name)
    )

    bytes_positions: t.List[t.Tuple[int, int]] = []
    with open(absolute_path_to_file, "r", encoding="utf-8") as file_descriptor:
        for line in file_descriptor.readlines():
            position_x: int = int(line.split(",")[0])
            position_y: int = int(line.split(",")[1])
            bytes_positions.append((position_x, position_y))

    return bytes_positions
