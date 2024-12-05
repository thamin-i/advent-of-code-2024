"""Advent of code - Day 05 - Part 02"""

import typing as t
from functools import cmp_to_key

from advent_of_code_2024.day_05.common import is_valid_update, read_input_file


def main() -> None:
    """Main function."""
    page_ordering_rules, updates = read_input_file("input.txt", __file__)
    invalid_updates: t.List[t.List[int]] = [
        update
        for update in updates
        if not is_valid_update(page_ordering_rules, update)
    ]

    for update in invalid_updates:
        update.sort(
            key=cmp_to_key(
                lambda x, y: (
                    -1 if y in (page_ordering_rules.get(x) or []) else 0  # type: ignore # noqa E501
                )
            )
        )

    print(sum(update[(int(len(update) // 2))] for update in invalid_updates))


if __name__ == "__main__":
    main()
