"""Advent of code - Day 13 - Part 02"""

import typing as t

from advent_of_code_2024.day_13.common import (
    ClawMachine,
    initialize_claw_machines,
)


def round_press_count(press_count: float, fraction: float = 0.05) -> int:
    """Round the press count.

    Args:
        press_count (float): Press count.
        fraction (float, optional): Fraction. Defaults to 0.05.

    Returns:
        int: Rounded press count.
    """
    fractional_part = abs(press_count) % 1
    if fractional_part < fraction or fractional_part > 1 - fraction:
        return round(press_count)
    return -1


def compute_minimum_tokens_for_prize(claw_machine: ClawMachine) -> int:
    """Compute the minimum tokens required to get the prize.

    ## Equations
    X = ax*A + bx*B
    Y = ay*A + by*B

    ## E-1
    X = ax*A + bx*B
    A = (X - bx*B)/ax

    ## E-2
    Y = ay*A + by*B
    Y = ay*(X - bx*B)/ax + by*B
    Y = ay*X/ax - ay*bx*B/ax + by*B
    B*(by - ay*bx/ax) = Y - ay*X/ax
    B = (Y - ay*X/ax)/(by - ay*bx/ax)


    ## Result
    B = (Y - ay*X/ax)/(by - ay*bx/ax)
    A = (X - bx*B)/ax

    Args:
        claw_machine (ClawMachine): Instance of the ClawMachine.

    Returns:
        int: Minimum tokens required to get the prize.
    """
    b_presses: int = round_press_count(
        (
            claw_machine.prize.y
            - claw_machine.button_a.y_shift
            * claw_machine.prize.x
            / claw_machine.button_a.x_shift
        )
        / (
            claw_machine.button_b.y_shift
            - claw_machine.button_a.y_shift
            * claw_machine.button_b.x_shift
            / claw_machine.button_a.x_shift
        )
    )
    a_presses: int = round_press_count(
        (claw_machine.prize.x - claw_machine.button_b.x_shift * b_presses)
        / claw_machine.button_a.x_shift
    )
    if a_presses < 0 or b_presses < 0:
        return 0
    return a_presses * 3 + b_presses * 1


def main() -> None:
    """Main function."""
    claw_machines: t.List[ClawMachine] = initialize_claw_machines(
        "input.txt",
        __file__,
        prize_shift=10000000000000,
    )
    minimum_tokens_count: int = sum(
        compute_minimum_tokens_for_prize(claw_machine)
        for claw_machine in claw_machines
    )
    print(minimum_tokens_count)


if __name__ == "__main__":
    main()
