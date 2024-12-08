"""Advent of code - Day 06 - Part 02"""

import typing as t
from copy import deepcopy
from enum import Enum

from advent_of_code_2024.day_06.common import read_board


class AlreadyVisitedException(Exception):
    """Already visited exception."""


class DirectionEnum(Enum):
    """Direction Enu."""

    UP = "^"
    DOWN = "v"
    LEFT = "<"
    RIGHT = ">"


class Board:
    """Board class."""

    value: t.List[t.List[str]]

    def __init__(self, raw_board: t.List[t.List[str]]) -> None:
        self.value = raw_board

    def __str__(self) -> str:
        """Return the board as a string.

        Returns:
            str: The board as a string.
        """
        str_board: str = ""
        for line in self.value:
            str_board += "".join(line) + "\n"
        str_board += "\n"
        return str_board

    def count_unique_positions(self, position_chars: t.List[str]) -> int:
        """Count the number of unique positions in the board.

        Args:
            position_chars (t.List[str]):
                The list of characters representing a position.

        Returns:
            int: The number of unique positions in the board.
        """
        unique_positions: int = 0
        for row in self.value:
            for cell in row:
                if cell in position_chars:
                    unique_positions += 1
        return unique_positions


class Guard:
    """Guard class."""

    pos_x: int
    pos_y: int
    board: Board
    direction: DirectionEnum
    already_visited_positions: t.Dict[str, t.List[str]]

    def __init__(self, board: Board) -> None:
        """Initialize the guard object.

        Args:
            board (t.List[t.List[str]]): The board.
        """
        self.already_visited_positions = {}
        self.board = board
        for y, row in enumerate(self.board.value):
            for x, cell in enumerate(row):
                if cell in [direction.value for direction in DirectionEnum]:
                    self.pos_x = x
                    self.pos_y = y
                    self.direction = DirectionEnum(cell)
                    return

    def update_direction(self) -> None:
        """Update the guard direction after hitting an obstacle.

        Returns:
            DirectionEnum: The updated guard object.
        """
        match self.direction:
            case DirectionEnum.UP:
                self.direction = DirectionEnum.RIGHT
            case DirectionEnum.RIGHT:
                self.direction = DirectionEnum.DOWN
            case DirectionEnum.DOWN:
                self.direction = DirectionEnum.LEFT
            case DirectionEnum.LEFT:
                self.direction = DirectionEnum.UP

    def is_in_front_of_obstacle(self) -> bool:
        """Check if the guard is in front of an obstacle.

        Returns:
            bool: True if the guard is in front of an obstacle, False otherwise.
        """
        match self.direction:
            case DirectionEnum.UP:
                if self.pos_y == 0:
                    return False
                return self.board.value[self.pos_y - 1][self.pos_x] == "#"
            case DirectionEnum.RIGHT:
                if self.pos_x == len(self.board.value[self.pos_y]) - 1:
                    return False
                return self.board.value[self.pos_y][self.pos_x + 1] == "#"
            case DirectionEnum.DOWN:
                if self.pos_y == len(self.board.value) - 1:
                    return False
                return self.board.value[self.pos_y + 1][self.pos_x] == "#"
            case DirectionEnum.LEFT:
                if self.pos_x == 0:
                    return False
                return self.board.value[self.pos_y][self.pos_x - 1] == "#"

    def is_out_of_board(self) -> bool:
        """Check if the guard is out of the board.

        Returns:
            bool: True if the guard is out of the board, False otherwise.
        """
        if self.pos_y < 0 or self.pos_y >= len(self.board.value):
            return True

        if self.pos_x < 0 or self.pos_x >= len(self.board.value[self.pos_y]):
            return True

        return False

    def step_forward(self) -> None:
        """Move the guard one step forward."""
        self.board.value[self.pos_y][self.pos_x] = self.direction.value
        match self.direction:
            case DirectionEnum.UP:
                self.pos_y -= 1
            case DirectionEnum.RIGHT:
                self.pos_x += 1
            case DirectionEnum.DOWN:
                self.pos_y += 1
            case DirectionEnum.LEFT:
                self.pos_x -= 1
        if self.is_out_of_board():
            return
        if self.already_visited_new_position():
            raise AlreadyVisitedException(
                f"Guard already visited position ({self.pos_x}, {self.pos_y})"
            )
        self.board.value[self.pos_y][self.pos_x] = self.direction.value
        if (
            self.already_visited_positions.get(f"{self.pos_x},{self.pos_y}")
            is None
        ):
            self.already_visited_positions[f"{self.pos_x},{self.pos_y}"] = []
        self.already_visited_positions[f"{self.pos_x},{self.pos_y}"].append(
            self.direction.value
        )

    def already_visited_new_position(self) -> bool:
        """Check if the guard has already visited the new position.

        Returns:
            bool: True if the guard has already visited the new position.
        """
        return self.direction.value in self.already_visited_positions.get(
            f"{self.pos_x},{self.pos_y}", []
        )

    def walk(self) -> None:
        """Walk the guard through the board."""
        while not self.is_out_of_board():
            if self.is_in_front_of_obstacle():
                self.update_direction()
            else:
                self.step_forward()


def main() -> None:
    """Main function."""
    raw_board: t.List[t.List[str]] = read_board("input.txt", __file__)
    infinite_loop_positions: t.List[t.Tuple[int, int]] = []
    for pos_y, row in enumerate(raw_board):
        for pos_x, cell in enumerate(row):
            if cell == ".":
                new_board: t.List[t.List[str]] = deepcopy(raw_board)
                new_board[pos_y][pos_x] = "#"
                board: Board = Board(new_board)
                guard: Guard = Guard(board)
                try:
                    guard.walk()
                except AlreadyVisitedException:
                    infinite_loop_positions.append((pos_x, pos_y))
    print(len(infinite_loop_positions))


if __name__ == "__main__":
    main()
