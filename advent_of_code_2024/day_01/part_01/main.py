"""Advent of code - Day 01 - Part 01"""

import typing as t

from advent_of_code_2024.day_01.common import read_int_list_from_file


def compute_total_distance(list_1: t.List[int], list_2: t.List[int]) -> int:
    """Compute the total distance between two lists (with a one liner).

    Args:
        list_1 (t.List[int]): First list.
        list_2 (t.List[int]): Second list.

    Returns:
        int: Total distance between the two lists.
    """
    return sum(
        abs(item_1 - item_2)
        for item_1, item_2 in zip(sorted(list_1), sorted(list_2))
    )


def main() -> None:
    """Main function."""
    total_distance: int = compute_total_distance(
        read_int_list_from_file(
            file_name="list_1.json",
            from_file=__file__,
        ),
        read_int_list_from_file(
            file_name="list_2.json",
            from_file=__file__,
        ),
    )
    print(total_distance)


if __name__ == "__main__":
    main()
