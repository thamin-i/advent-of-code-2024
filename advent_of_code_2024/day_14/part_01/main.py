"""Advent of code - Day 14 - Part 01"""

from advent_of_code_2024.day_14.common import Board, initialize_board


def main() -> None:
    """Main function."""
    board: Board = initialize_board(
        file_name="input.txt",
        from_file=__file__,
        board_width=101,
        board_height=103,
    )
    board.print()
    board.teleport_robots(100)
    board.print()
    robots_in_quadrants = board.count_robots_in_quadrants()
    print(robots_in_quadrants)


if __name__ == "__main__":
    main()
