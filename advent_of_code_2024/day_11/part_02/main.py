"""Advent of code - Day 11 - Part 02"""

import typing as t

from advent_of_code_2024.day_11.common import blinks, read_stones_line


def main() -> None:
    """Main function."""
    stones_line: t.List[int] = read_stones_line("input.txt", __file__)
    stones_count: int = blinks(stones_line, 75)
    print(stones_count)


if __name__ == "__main__":
    main()
