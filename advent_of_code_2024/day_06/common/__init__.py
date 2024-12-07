"""Common methods for the Day 06"""

import os
import typing as t


def read_board(
    file_name: str,
    from_file: str,
) -> t.List[t.List[str]]:
    """Read the input file and return the board.

    Args:
        file_name (str): Input file name.
        from_file (str): File from where the method is called.

    Returns:
        t.List[t.List[str]]: The board.
    """
    absolute_path_to_file: str = os.path.realpath(
        os.path.join(os.getcwd(), os.path.dirname(from_file), file_name)
    )

    board: t.List[t.List[str]] = []
    with open(absolute_path_to_file, "r", encoding="utf-8") as file_descriptor:
        board = [
            list(line.replace("\n", ""))
            for line in file_descriptor
            if len(line.replace("\n", "")) > 0
        ]
    return board
