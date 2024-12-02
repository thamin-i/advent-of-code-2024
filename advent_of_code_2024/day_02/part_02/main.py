"""Advent of code - Day 02 - Part 02"""

import enum
import typing as t
from copy import deepcopy

from advent_of_code_2024.day_02.common import read_reports_from_files


class SideEnum(enum.IntEnum):
    """Side enum."""

    UNSET = 0
    DECREASING = -1
    INCREASING = 1


def is_report_safe(report: t.List[int]) -> t.Tuple[bool, t.List[t.List[int]]]:
    """Check if a report is safe.

    Args:
        report (t.List[int]): Report.

    Returns:
        t.Tuple[bool, t.List[t.List[int]]]:
            Tuple with a boolean indicating if the report is safe
            and a list of reports to retry.
    """
    side: SideEnum = SideEnum.UNSET
    for idx in range(len(report) - 1):
        match report[idx + 1] - report[idx]:
            case num if num in [1, 2, 3]:
                if side == SideEnum.INCREASING:
                    return False, [
                        report[0 : idx - 1] + report[idx:],
                        report[0:idx] + report[idx + 1 :],
                        report[0 : idx + 1] + report[idx + 2 :],
                    ]
                side = SideEnum.DECREASING
            case num if num in [-1, -2, -3]:
                if side == SideEnum.DECREASING:
                    return False, [
                        report[0 : idx - 1] + report[idx:],
                        report[0:idx] + report[idx + 1 :],
                        report[0 : idx + 1] + report[idx + 2 :],
                    ]
                side = SideEnum.INCREASING
            case _:
                return False, [
                    report[0 : idx - 1] + report[idx:],
                    report[0:idx] + report[idx + 1 :],
                    report[0 : idx + 1] + report[idx + 2 :],
                ]
    return True, []


def count_safe_reports(reports: t.List[t.List[int]]) -> int:
    """Count safe reports.

    Args:
        reports (t.List[t.List[int]]): List of reports.

    Returns:
        int: Number of safe reports.
    """
    # Generate list of reports that we can retry.
    reports_to_retry: t.List[t.List[t.List[int]]] = []
    for report in reports:
        safeness, report_to_retry = is_report_safe(deepcopy(report))
        if safeness is False:
            reports_to_retry.append(report_to_retry)

    # Retry reports and count the fixed ones.
    fixed_reports_count: int = 0
    for report_1, report_2, report_3 in reports_to_retry:
        safeness_1, _ = is_report_safe(deepcopy(report_1))
        safeness_2, _ = is_report_safe(deepcopy(report_2))
        safeness_3, _ = is_report_safe(deepcopy(report_3))
        if safeness_1 is True or safeness_2 is True or safeness_3 is True:
            fixed_reports_count += 1

    return len(reports) - len(reports_to_retry) + fixed_reports_count


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
