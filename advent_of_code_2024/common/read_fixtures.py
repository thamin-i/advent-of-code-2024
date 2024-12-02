"""Read fixtures from files."""

import json
import os
import typing as t


def read_int_list_from_file(file_name: str, from_file: str) -> t.List[int]:
    """Read a list of integers from a file.

    Args:
        file_name (str): File name.
        from_file (str): Path to the file that calls this function.

    Returns:
        t.List[int]: List of integers.
    """
    absolute_path_to_file: str = os.path.realpath(
        os.path.join(os.getcwd(), os.path.dirname(from_file), file_name)
    )
    res: t.List[int] = []
    with open(absolute_path_to_file, "r", encoding="utf-8") as file_descriptor:
        res = json.load(file_descriptor)
    return res
