"""Common methods for the Day 07"""

import os
import re
import typing as t
from enum import Enum
from itertools import product


def read_equations(
    file_name: str,
    from_file: str,
) -> t.List[t.Tuple[int, t.List[int]]]:
    """Read equations from a file.

    Args:
        file_name (str): Input file name.
        from_file (str): File from where the method is called.

    Returns:
        t.List[t.Tuple[int, t.List[int]]]: List of equations.
    """
    absolute_path_to_file: str = os.path.realpath(
        os.path.join(os.getcwd(), os.path.dirname(from_file), file_name)
    )

    equations: t.List[t.Tuple[int, t.List[int]]] = []
    with open(absolute_path_to_file, "r", encoding="utf-8") as file_descriptor:
        for line in file_descriptor:
            line = line.strip()
            if line:
                equation: t.Tuple[int, t.List[int]] = (
                    int(line.split(":")[0]),
                    [
                        int(num.replace(" ", ""))
                        for num in line.split(":")[1].split(" ")
                        if len(num.replace(" ", ""))
                    ],
                )
                equations.append(equation)
    return equations


class OperatorsEnum(Enum):
    """Operators enum."""

    ADD = "+"
    MULTIPLY = "*"
    CONCATENATE = "||"


def generate_all_equations(
    numbers: t.List[int], operators: t.List[str]
) -> t.List[str]:
    """Generate all possible equations from a list of numbers.

    Args:
        numbers (t.List[int]): List of numbers.
        operators (t.List[str]): List of operators.

    Returns:
        t.List[str]: List of equations.
    """
    equations: t.List[str] = []
    for ops in product(operators, repeat=len(numbers) - 1):
        equation = "".join(
            str(num) + op for num, op in zip(numbers, ops)
        ) + str(numbers[-1])
        equations.append(equation)
    return equations


def compute_equation(equation: str, operators: t.List[str]) -> int:
    """Compute the result of an equation.

    Args:
        equation (str): Equation to compute.
        operators (t.List[str]): List of operators.

    Returns:
        int: Result of the equation.
    """
    operator_regex: re.Pattern[str] = re.compile(
        "|".join([re.escape(operator) for operator in operators])
    )
    number_regex: re.Pattern[str] = re.compile(r"[0-9]+")
    result: int = 0
    equation = f"+{equation}"
    for operator_match in re.finditer(operator_regex, equation):
        for number_match in re.finditer(
            number_regex, equation[operator_match.end() :]
        ):
            match operator_match.group():
                case OperatorsEnum.ADD.value:
                    result = result + int(number_match.group())
                case OperatorsEnum.MULTIPLY.value:
                    result = result * int(number_match.group())
                case OperatorsEnum.CONCATENATE.value:
                    result = int(str(result) + str(number_match.group()))
            break
    return result


def is_equation_valid(
    expected_result: int,
    numbers: t.List[int],
    operators: t.List[str],
) -> bool:
    """Check if an equation is valid.

    Args:
        expected_result (int): Expected result.
        numbers (t.List[int]): List of numbers to compute.
        operators (t.List[str]): List of available operators.

    Returns:
        bool: True if the equation is valid, False otherwise.
    """
    str_equations = generate_all_equations(numbers, operators)
    for str_equation in str_equations:
        if compute_equation(str_equation, operators) == expected_result:
            return True
    return False
