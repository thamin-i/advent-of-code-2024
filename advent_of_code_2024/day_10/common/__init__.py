"""Common methods for the Day 10"""

import os
import typing as t


def is_valid_position(
    x: int, y: int, topographic_map: t.List[t.List[int]]
) -> bool:
    """Check if a position is within bounds.

    Args:
        x (int): X coordinate.
        y (int): Y coordinate.
        topographic_map (t.List[t.List[int]]): Topographic map.

    Returns:
        bool: True if the position is within bounds, False otherwise.
    """
    return 0 <= x < len(topographic_map) and 0 <= y < len(topographic_map[0])


def find_trailheads(
    topographic_map: t.List[t.List[int]],
) -> t.List[t.Tuple[int, int]]:
    """Find trailheads in the topographic map.

    Args:
        topographic_map (t.List[t.List[int]]): Topographic map.

    Returns:
        t.List[t.Tuple[int, int]]: List of trailheads.
    """
    trailheads: t.List[t.Tuple[int, int]] = []
    for i, _ in enumerate(topographic_map):
        for j, _ in enumerate(topographic_map[i]):
            if topographic_map[i][j] == 0:
                trailheads.append((i, j))
    return trailheads


def read_topographic_map(
    file_name: str,
    from_file: str,
) -> t.List[t.List[int]]:
    """Read topographic map from a txt file.

    Args:
        file_name (str): Input file name.
        from_file (str): File from where the method is called.

    Returns:
        List[List[int]]: Topographic map.
    """
    absolute_path_to_file: str = os.path.realpath(
        os.path.join(os.getcwd(), os.path.dirname(from_file), file_name)
    )

    topographic_map: t.List[t.List[int]] = []
    with open(absolute_path_to_file, "r", encoding="utf-8") as file_descriptor:
        for line in file_descriptor:
            topographic_map.append([int(char) for char in line.strip()])
    return topographic_map
