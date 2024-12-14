"""Common methods for the Day 14"""

import os
import re
import typing as t


class Position:
    """Position class."""

    x: int
    y: int

    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y


class Velocity:
    """Velocity class."""

    x: int
    y: int

    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y


class Robot:
    """Robot class."""

    position: Position
    velocity: Velocity

    def __init__(self, raw_input_line: str) -> None:
        matches = re.findall(r"[-]?\d+", raw_input_line)
        if matches is None:
            raise ValueError("Invalid input line")
        px, py, vx, vy = map(int, matches)
        self.position = Position(px, py)
        self.velocity = Velocity(vx, vy)

    def teleport(
        self, board_width: int, board_height: int, seconds: int
    ) -> None:
        """Teleport the robot to a new position.

        Args:
            board_width (int): Board width.
            board_height (int): Board height.
            seconds (int): Number of seconds to teleport the robot to.
        """
        self.position.x += self.velocity.x * seconds
        self.position.y += self.velocity.y * seconds
        if self.position.x < 0:
            self.position.x = self.position.x % board_width
        elif self.position.x >= board_width:
            self.position.x = self.position.x % board_width
        if self.position.y < 0:
            self.position.y = self.position.y % board_height
        elif self.position.y >= board_height:
            self.position.y = self.position.y % board_height


class Board:
    """Board class."""

    width: int
    height: int
    robots: t.List[Robot]

    def __init__(self, width: int, height: int, robots: t.List[Robot]) -> None:
        self.width = width
        self.height = height
        self.robots = robots

    def print(self, empty_char: str = ".") -> None:
        """Print the board with all the robots on it.

        Args:
            empty_char (str, optional):
                Character used to represent empty slots.
                Defaults to ".".
        """
        board: t.List[t.List[int]] = [
            [0 for _ in range(self.height)] for _ in range(self.width)
        ]

        for robot in self.robots:
            board[robot.position.x][robot.position.y] += 1

        print()
        for column in range(self.height):
            for row in range(self.width):
                if board[row][column] == 0:
                    print(empty_char, end="")
                else:
                    print(board[row][column], end="")
            print()
        print()

    def teleport_robots(self, seconds: int) -> None:
        """Teleport all robots on the board.

        Args:
            seconds (int): Number of seconds to teleport the robots.
        """
        for robot in self.robots:
            robot.teleport(self.width, self.height, seconds)

    def count_robots_in_quadrants(self) -> int:
        """Count the number of robots in each quadrant.

        Returns:
            int: Number of robots in each quadrant.
        """
        quadrant_width: int = self.width // 2
        quadrant_height: int = self.height // 2

        top_left_count: int = 0
        top_right_count: int = 0
        bottom_left_count: int = 0
        bottom_right_count: int = 0

        for robot in self.robots:
            if (
                robot.position.x < quadrant_width
                and robot.position.y < quadrant_height
            ):
                top_left_count += 1
            elif (
                robot.position.x > quadrant_width
                and robot.position.y < quadrant_height
            ):
                top_right_count += 1
            elif (
                robot.position.x < quadrant_width
                and robot.position.y > quadrant_height
            ):
                bottom_left_count += 1
            elif (
                robot.position.x > quadrant_width
                and robot.position.y > quadrant_height
            ):
                bottom_right_count += 1

        return (
            top_left_count
            * top_right_count
            * bottom_left_count
            * bottom_right_count
        )

    def to_2d_array(self) -> t.List[t.List[int]]:
        """Convert the board to a 2D array.

        Returns:
            t.List[t.List[int]]: 2D array representation of the board.
        """
        board: t.List[t.List[int]] = [
            [0 for _ in range(self.width)] for _ in range(self.height)
        ]

        for robot in self.robots:
            board[robot.position.y][robot.position.x] += 1

        return board


def initialize_board(
    file_name: str,
    from_file: str,
    board_width: int,
    board_height: int,
) -> Board:
    """Initialize board using configuration from a txt file.

    Args:
        file_name (str): Input file name.
        from_file (str): File from where the method is called.
        board_width (int): Board width.
        board_height (int): Board height.

    Returns:
        Board: An instantiated board.
    """
    absolute_path_to_file: str = os.path.realpath(
        os.path.join(os.getcwd(), os.path.dirname(from_file), file_name)
    )

    board: Board = Board(board_width, board_height, [])
    with open(absolute_path_to_file, "r", encoding="utf-8") as file_descriptor:
        for line in file_descriptor.readlines():
            board.robots.append(Robot(line))
    return board
