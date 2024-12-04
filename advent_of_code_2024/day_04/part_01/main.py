"""Advent of code - Day 04 - Part 01"""

import re
import typing as t

from advent_of_code_2024.day_04.common import read_board


def horizontal_walk(board: t.List[t.List[str]]) -> t.Generator[t.List[str]]:
    """Horizontal walk through the board.

    Args:
        board (t.List[t.List[str]]): Board.

    Returns:
        t.Generator[t.List[str]]: Generator of lines.

    Yields:
        Iterator[t.Generator[t.List[str]]]: Line.
    """
    for line in board:
        yield line


def vertical_walk(board: t.List[t.List[str]]) -> t.Generator[t.List[str]]:
    """Vertical walk through the board.

    Args:
        board (t.List[t.List[str]]): Board.

    Returns:
        t.Generator[t.List[str]]: Generator of lines.

    Yields:
        Iterator[t.Generator[t.List[str]]]: Line.
    """
    for line in zip(*board):
        yield list(line)


def diagonal_walk(board: t.List[t.List[str]]) -> t.Generator[t.List[str]]:
    """Diagonal walk through the board.

    Args:
        board (t.List[t.List[str]]): Board.

    Returns:
        t.Generator[t.List[str]]: Generator of lines.

    Yields:
        Iterator[t.Generator[t.List[str]]]: Line.
    """
    # Bottom left to top right
    for i in range(len(board)):
        yield [board[i + j][j] for j in range(len(board) - i)]
    for i in range(1, len(board)):
        yield [board[j][i + j] for j in range(len(board) - i)]

    # Top left to bottom right
    for i in range(len(board)):
        yield [board[i - j][j] for j in range(i + 1)]
    for i in range(1, len(board)):
        yield [board[len(board) - 1 - j][i + j] for j in range(len(board) - i)]


def count_occurences_in_line(
    board: t.List[t.List[str]],
    walk_method: t.Callable[
        [t.List[t.List[str]]], t.Generator[list[str], None, None]
    ],
) -> int:
    """Count the occurrences of the patterns in the board
    using a specific walk through method.

    Args:
        board (t.List[t.List[str]]): Board.
        walk_method (t.Callable[]): Walk through method.

    Returns:
        int: Number of occurrences.
    """
    regex: re.Pattern[str] = re.compile(r"(?=(XMAS))|(?=(SAMX))")
    return sum(
        len(re.findall(regex, "".join(line))) for line in walk_method(board)
    )


def count_occurrences_in_board(board: t.List[t.List[str]]) -> int:
    """Count the occurrences of the patterns in the board.

    Args:
        board (t.List[t.List[str]]): Board.

    Returns:
        int: Number of occurrences.
    """
    occurrences: int = 0
    occurrences += count_occurences_in_line(board, horizontal_walk)
    occurrences += count_occurences_in_line(board, vertical_walk)
    occurrences += count_occurences_in_line(board, diagonal_walk)
    return occurrences


def main() -> None:
    """Main function."""
    board: t.List[t.List[str]] = read_board("input.txt", __file__)
    occurrences: int = count_occurrences_in_board(board)
    print(occurrences)


if __name__ == "__main__":
    main()
