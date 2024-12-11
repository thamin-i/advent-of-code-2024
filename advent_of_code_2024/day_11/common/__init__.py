"""Common methods for the Day 11"""

import os
import typing as t
from collections import defaultdict


def read_stones_line(
    file_name: str,
    from_file: str,
) -> t.List[int]:
    """Read stones line from a txt file.

    Args:
        file_name (str): Input file name.
        from_file (str): File from where the method is called.

    Returns:
        t.List[int]: Stones line.
    """
    absolute_path_to_file: str = os.path.realpath(
        os.path.join(os.getcwd(), os.path.dirname(from_file), file_name)
    )

    stones_line: t.List[int] = []
    with open(absolute_path_to_file, "r", encoding="utf-8") as file_descriptor:
        stones_line = [
            int(stone) for stone in file_descriptor.readline().split(" ")
        ]
    return stones_line


def blinks(stones_line: t.List[int], num_blinks: int) -> int:
    """Compute the number of stones after a number of blinks.

    Args:
        stones_line (t.List[int]): Initial stones line.
        num_blinks (int): Number of blinks.

    Returns:
        int: Number of stones after ${num_blinks} blinks.
    """
    stones_dict: t.DefaultDict[int, int] = defaultdict(
        int, {stone: stones_line.count(stone) for stone in stones_line}
    )

    for _ in range(num_blinks):
        new_stones_dict: t.DefaultDict[int, int] = defaultdict(int)

        for stone, count in stones_dict.items():
            if stone == 0:
                new_stones_dict[1] += count
            elif len(stone_str := str(stone)) % 2 == 0:
                middle: int = len(stone_str) // 2
                new_stones_dict[int(stone_str[:middle])] += count
                new_stones_dict[int(stone_str[middle:])] += count
            else:
                new_stones_dict[stone * 2024] += count

        stones_dict = new_stones_dict

    return sum(stones_dict[stone] for stone in stones_dict)
