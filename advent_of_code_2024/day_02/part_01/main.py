"""Advent of code - Day 02 - Part 01"""

import enum
import typing as t
from itertools import pairwise

from advent_of_code_2024.day_02.common import read_reports_from_files


class SideEnum(enum.IntEnum):
    """Side enum."""

    UNSET = 0
    DECREASING = -1
    INCREASING = 1


def is_report_safe(report: t.List[int]) -> bool:
    """Check if a report is safe.

    Args:
        report (t.List[int]): List of integers.

    Returns:
        bool: True if the report is safe, False otherwise.
    """
    side: SideEnum = SideEnum.UNSET
    for a, b in pairwise(report):
        match b - a:
            case num if num in [1, 2, 3]:
                if side == SideEnum.INCREASING:
                    return False
                side = SideEnum.DECREASING
            case num if num in [-1, -2, -3]:
                if side == SideEnum.DECREASING:
                    return False
                side = SideEnum.INCREASING
            case _:
                return False
    return True


def count_safe_reports(reports: t.List[t.List[int]]) -> int:
    """Count safe reports.

    Args:
        reports (t.List[t.List[int]]): List of reports.

    Returns:
        int: Number of safe reports.
    """
    return sum(1 for report in reports if is_report_safe(report))


def main() -> None:
    """Main function."""
    safe_reports: int = count_safe_reports(
        read_reports_from_files(
            file_name="lists.json",
            from_file=__file__,
        )
    )
    print(safe_reports)


if __name__ == "__main__":
    main()
