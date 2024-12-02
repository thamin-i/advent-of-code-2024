"""Common methods for the Day 02"""

import json
import os
import typing as t


def read_reports_from_files(
    file_name: str, from_file: str
) -> t.List[t.List[int]]:
    """Read reports from files.

    Args:
        file_name (str): File name.
        from_file (str): Path to the file that calls this function.

    Returns:
        t.List[t.List[int]]: List of reports.
    """
    absolute_path_to_file: str = os.path.realpath(
        os.path.join(os.getcwd(), os.path.dirname(from_file), file_name)
    )
    res: t.List[t.List[int]] = []
    with open(absolute_path_to_file, "r", encoding="utf-8") as file_descriptor:
        res = json.load(file_descriptor)
    return res
