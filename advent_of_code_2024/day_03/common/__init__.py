"""Common methods for the Day 03"""

import os


def read_expression_from_file(file_name: str, from_file: str) -> str:
    """Read a raw expression from a file.

    Args:
        file_name (str): File name.
        from_file (str): Path to the file that calls this function.

    Returns:
        str: Raw expression.
    """
    absolute_path_to_file: str = os.path.realpath(
        os.path.join(os.getcwd(), os.path.dirname(from_file), file_name)
    )
    res: str = ""
    with open(absolute_path_to_file, "r", encoding="utf-8") as file_descriptor:
        res = file_descriptor.read()
    return res
