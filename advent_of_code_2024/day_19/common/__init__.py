"""Common methods for the Day 19"""

import os
import typing as t
from functools import lru_cache


def count_possible_solutions(design: str, towels: t.List[str]) -> int:
    """Count possible solutions for the design using list of infinite towels.

    Args:
        design (str): Desired design.
        towels (t.List[str]): List of infinite towels.

    Returns:
        int: Number of possible solutions.
    """
    design_length: int = len(design)

    @lru_cache(None)
    def count_ways(start: int) -> int:
        """Count possible solutions from start index for the design.

        Args:
            start (int): Start index in the design.

        Returns:
            int: Number of possible solutions from start index.
        """
        if start == design_length:
            return 1

        solutions_count: int = 0
        for towel in towels:
            end: int = start + len(towel)
            if end <= design_length and design[start:end] == towel:
                solutions_count += count_ways(end)

        return solutions_count

    return count_ways(0)


def parse_input_file(
    file_name: str,
    from_file: str,
) -> t.Tuple[t.List[str], t.List[str]]:
    """Parse txt file.

    Args:
        file_name (str): Input file name.
        from_file (str): File from where the method is called.

    Returns:
        t.Tuple[t.List[str], t.List[str]]:
            List of towels.
            List of designs.
    """
    absolute_path_to_file: str = os.path.realpath(
        os.path.join(os.getcwd(), os.path.dirname(from_file), file_name)
    )

    towels: t.List[str] = []
    designs: t.List[str] = []
    with open(absolute_path_to_file, "r", encoding="utf-8") as file_descriptor:
        for line in file_descriptor.readlines():
            if "," in line:
                towels = [p.strip() for p in line.split(",")]
            elif len(line.strip()) > 0:
                designs.append(line.strip())

    return towels, designs
