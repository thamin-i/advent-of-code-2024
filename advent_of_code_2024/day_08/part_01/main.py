"""Advent of code - Day 08 - Part 01"""

import typing as t

from advent_of_code_2024.day_08.common import (
    Board,
    Position,
    read_antennas_positions,
)


def main() -> None:
    """Main function."""
    board: Board = read_antennas_positions("input.txt", __file__)
    antinodes: t.Set[Position] = board.compute_all_antinodes_positions_v1()
    board.print_board(antinodes)
    print(len(antinodes))


if __name__ == "__main__":
    main()
