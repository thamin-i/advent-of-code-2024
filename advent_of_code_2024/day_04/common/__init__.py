"""Common methods for the Day 04"""

import os
import typing as t


def read_board(file_name: str, from_file: str) -> t.List[t.List[str]]:
    """Read a board from a txt file.

    Args:
        file_name (str): File name.
        from_file (str): Path to the file that calls this function.

    Returns:
        t.List[t.List[str]]: List of lines.
    """
    absolute_path_to_file: str = os.path.realpath(
        os.path.join(os.getcwd(), os.path.dirname(from_file), file_name)
    )
    board: t.List[t.List[str]] = []
    with open(absolute_path_to_file, "r", encoding="utf-8") as file_descriptor:
        board = [list(line) for line in file_descriptor]
    return board
