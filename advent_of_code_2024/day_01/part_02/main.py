"""Advent of code - Day 01 - Part 02"""

import typing as t
from collections import Counter

from advent_of_code_2024.day_01.common import read_int_list_from_file


def compute_similarity_score(list_1: t.List[int], list_2: t.List[int]) -> int:
    """Compute the similarity score between two lists.

    Args:
        list_1 (t.List[int]): First list.
        list_2 (t.List[int]): Second list.

    Returns:
        int: Similarity score.
    """
    list_2_counts: Counter[int] = Counter(list_2)
    return sum(item_1 * list_2_counts.get(item_1, 0) for item_1 in list_1)


def main() -> None:
    """Main function."""
    similarity_score: int = compute_similarity_score(
        read_int_list_from_file(
            file_name="list_1.json",
            from_file=__file__,
        ),
        read_int_list_from_file(
            file_name="list_2.json",
            from_file=__file__,
        ),
    )
    print(similarity_score)


if __name__ == "__main__":
    main()
