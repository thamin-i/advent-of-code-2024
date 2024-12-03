"""Advent of code - Day 03 - Part 01"""

import re

from advent_of_code_2024.day_03.common import read_expression_from_file


def fix_expression(corrupted_expression: str) -> str:
    """Fix the corrupted expression.

    Args:
        expression (str): Corrupted expression.

    Returns:
        str: Valid expression.
    """
    mul_regex: re.Pattern[str] = re.compile(r"mul\([0-9]+,[0-9]+\)")
    num_regex: re.Pattern[str] = re.compile(r"[0-9]+")
    fixed_expression: str = "+".join(
        "*".join(re.findall(num_regex, mul_match))
        for mul_match in re.findall(mul_regex, corrupted_expression)
    )
    return fixed_expression


def main() -> None:
    """Main function."""
    corrupted_expression: str = read_expression_from_file("input.txt", __file__)
    fixed_expression: str = fix_expression(corrupted_expression)
    result: int = eval(fixed_expression)  # pylint: disable=eval-used
    print(result)


if __name__ == "__main__":
    main()
