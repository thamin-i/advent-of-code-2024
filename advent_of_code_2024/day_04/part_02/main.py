"""Advent of code - Day 04 - Part 02"""

import typing as t

from advent_of_code_2024.day_04.common import read_board


def generate_patterns() -> t.List[t.List[t.List[str]]]:
    """Generate patterns.

    Returns:
        t.List[t.List[t.List[str]]]: List of patterns.
    """
    return [
        [["M", ".", "S"], [".", "A", "."], ["M", ".", "S"]],
        [["M", ".", "M"], [".", "A", "."], ["S", ".", "S"]],
        [["S", ".", "S"], [".", "A", "."], ["M", ".", "M"]],
        [["S", ".", "M"], [".", "A", "."], ["S", ".", "M"]],
    ]


def count_occurences(board: t.List[t.List[str]]) -> int:
    """Count the number of occurences of the patterns in the board.

    Args:
        board (t.List[t.List[str]]): Board.

    Returns:
        int: Count of occurences.
    """
    rows, cols = len(board), len(board[0])
    count: int = 0
    for pattern in generate_patterns():
        p_rows, p_cols = len(pattern), len(pattern[0])
        for i in range(rows - p_rows + 1):
            for j in range(cols - p_cols + 1):
                match = True
                # Check if the sub-board matches the pattern
                for pi in range(p_rows):
                    for pj in range(p_cols):
                        if pattern[pi][pj] == ".":
                            continue
                        if board[i + pi][j + pj] != pattern[pi][pj]:
                            match = False
                            break
                if match:
                    count += 1
    return count


def main() -> None:
    """Main function."""
    board: t.List[t.List[str]] = read_board("input.txt", __file__)
    count: int = count_occurences(board)
    print(count)


if __name__ == "__main__":
    main()
