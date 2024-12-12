"""Common methods for the Day 12"""

import os
import typing as t


def read_garden_map(
    file_name: str,
    from_file: str,
) -> t.List[t.List[str]]:
    """Read garden map from a txt file.

    Args:
        file_name (str): Input file name.
        from_file (str): File from where the method is called.

    Returns:
        t.List[t.List[str]]: Garden map.
    """
    absolute_path_to_file: str = os.path.realpath(
        os.path.join(os.getcwd(), os.path.dirname(from_file), file_name)
    )

    garden_map: t.List[t.List[str]] = []
    with open(absolute_path_to_file, "r", encoding="utf-8") as file_descriptor:
        garden_map = [
            list(plants.strip()) for plants in file_descriptor.readlines()
        ]
    return garden_map
