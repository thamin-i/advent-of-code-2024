"""Advent of code - Day 05 - Part 01"""

import typing as t

from advent_of_code_2024.day_05.common import is_valid_update, read_input_file


def main() -> None:
    """Main function."""
    page_ordering_rules, updates = read_input_file("input.txt", __file__)

    valid_updates: t.List[t.List[int]] = [
        update
        for update in updates
        if is_valid_update(page_ordering_rules, update)
    ]

    print(sum(update[(int(len(update) // 2))] for update in valid_updates))


if __name__ == "__main__":
    main()
