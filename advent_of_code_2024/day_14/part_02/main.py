"""Advent of code - Day 14 - Part 02"""

from matplotlib import pyplot as plt

from advent_of_code_2024.day_14.common import Board, initialize_board


def main() -> None:
    """Main function."""
    board: Board = initialize_board(
        file_name="input.txt",
        from_file=__file__,
        board_width=101,
        board_height=103,
    )
    for second in range(10_000):
        plt.imshow(board.to_2d_array(), interpolation="nearest", cmap="gray")
        plt.savefig(f"/tmp/dumps/{second}.png")
        board.teleport_robots(1)


if __name__ == "__main__":
    main()
