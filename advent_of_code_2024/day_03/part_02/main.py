"""Advent of code - Day 03 - Part 02"""

import re

from advent_of_code_2024.day_03.common import read_expression_from_file


def compute_less_corrupted_expression(corrupted_expression: str) -> int:
    """Compute the corrupted expression.

    Args:
        corrupted_expression (str): Corrupted expression.

    Returns:
        int: Result of the expression.
    """
    mul_regex: re.Pattern[str] = re.compile(r"mul\([0-9]+,[0-9]+\)")
    num_regex: re.Pattern[str] = re.compile(r"[0-9]+")
    result: int = 0

    for mul_match in re.findall(mul_regex, corrupted_expression):
        left_num, right_num = re.findall(num_regex, mul_match)
        result += int(left_num) * int(right_num)

    return result


def compute_fully_corrupted_expression(corrupted_expression: str) -> int:
    """Compute the corrupted expression containing do() and don't().

    Args:
        expression (str): Corrupted expression.

    Returns:
        int: Result of the expression.
    """
    start_idx: int | None = None
    end_idx: int | None = None
    result: int = 0
    corrupted_expression = f"do(){corrupted_expression}"

    for m in re.finditer(r"do\(\)|don't\(\)", corrupted_expression):
        if start_idx is not None:
            end_idx = m.start()
            result += compute_less_corrupted_expression(
                corrupted_expression[start_idx:end_idx]
            )
            start_idx, end_idx = None, None
        if m.group() == "do()":
            start_idx = m.end()

    if start_idx is not None:
        result += compute_less_corrupted_expression(
            corrupted_expression[start_idx:]
        )

    return result


def main() -> None:
    """Main function."""
    corrupted_expression: str = read_expression_from_file("input.txt", __file__)
    result: int = compute_fully_corrupted_expression(corrupted_expression)
    print(result)


if __name__ == "__main__":
    main()
