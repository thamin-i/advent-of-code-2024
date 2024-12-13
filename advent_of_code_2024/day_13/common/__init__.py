"""Common methods for the Day 13"""

import math
import os
import re
import typing as t


class Position:
    """Position class."""

    x: int
    y: int

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __repr__(self) -> str:
        return f"""Position(X: {self.x}, Y: {self.y})"""


class Button:
    """Button class."""

    x_shift: int
    y_shift: int

    def __init__(self, x_shift: int, y_shift: int):
        self.x_shift = x_shift
        self.y_shift = y_shift

    def __repr__(self) -> str:
        return f"""Button(Shift X: {self.x_shift}, Shift Y: {self.y_shift})"""


class ClawMachine:
    """ClawMachine class."""

    button_a: Button
    button_b: Button
    prize: Position

    def __init__(self, button_a: Button, button_b: Button, prize: Position):
        self.button_a = button_a
        self.button_b = button_b
        self.prize = prize

    def __repr__(self) -> str:
        return f"""ClawMachine(
    Button A: {self.button_a},
    Button B: {self.button_b},
    Prize: {self.prize},
)"""


def is_prize_accessible(machine: ClawMachine) -> bool:
    """Check if the prize is accessible.

    Args:
        machine (ClawMachine): Instance of the ClawMachine.

    Returns:
        bool: True if the prize is accessible, False otherwise.
    """
    gcd_x = math.gcd(machine.button_a.x_shift, machine.button_b.x_shift)
    gcd_y = math.gcd(machine.button_a.y_shift, machine.button_b.y_shift)

    if machine.prize.x % gcd_x != 0:
        return False

    if machine.prize.y % gcd_y != 0:
        return False

    return True


def extract_values(text: str, pattern: str) -> t.Tuple[int, int]:
    """Extract values from a text using a pattern.

    Args:
        text (str): Raw text.
        pattern (str): Regular expression pattern.

    Returns:
        t.Tuple[int, int]: Tuple of two integers.
    """
    match = re.search(pattern, text)
    if match is None:
        raise ValueError(f"Pattern {pattern} not found in text {text}")
    return int(match.group(1)), int(match.group(2))


def initialize_claw_machines(
    file_name: str,
    from_file: str,
    prize_shift: int = 0,
) -> t.List[ClawMachine]:
    """Initialize claw machines using configuration from a txt file.

    Args:
        file_name (str): Input file name.
        from_file (str): File from where the method is called.
        prize_shift (int, optional): Prize shift. Defaults to 0.

    Returns:
        t.List[ClawMachine]: List of claw machines.
    """
    absolute_path_to_file: str = os.path.realpath(
        os.path.join(os.getcwd(), os.path.dirname(from_file), file_name)
    )

    claw_machines: t.List[ClawMachine] = []
    button_a, button_b, prize = None, None, None
    with open(absolute_path_to_file, "r", encoding="utf-8") as file_descriptor:
        for line in file_descriptor.readlines():
            if "Button A" in line:
                x, y = extract_values(line, r"X\+(\d+), Y\+(\d+)")
                button_a = Button(x, y)
            elif "Button B" in line:
                x, y = extract_values(line, r"X\+(\d+), Y\+(\d+)")
                button_b = Button(x, y)
            elif "Prize" in line:
                x, y = extract_values(line, r"X=(\d+), Y=(\d+)")
                prize = Position(x + prize_shift, y + prize_shift)
            if button_a and button_b and prize:
                claw_machines.append(ClawMachine(button_a, button_b, prize))
                button_a, button_b, prize = None, None, None
    return claw_machines
