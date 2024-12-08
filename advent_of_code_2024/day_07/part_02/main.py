"""Advent of code - Day 07 - Part 02"""

import typing as t

from advent_of_code_2024.day_07.common import (
    OperatorsEnum,
    is_equation_valid,
    read_equations,
)


def main() -> None:
    """Main function."""
    equations: t.List[t.Tuple[int, t.List[int]]] = read_equations(
        "input.txt", __file__
    )
    operators: t.List[str] = [operator.value for operator in OperatorsEnum]
    valid_equations: t.List[t.Tuple[int, t.List[int]]] = []
    for equation in equations:
        if is_equation_valid(equation[0], equation[1], operators):
            valid_equations.append(equation)
    print(sum(equation[0] for equation in valid_equations))


if __name__ == "__main__":
    main()
