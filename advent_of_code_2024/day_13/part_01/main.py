"""Advent of code - Day 13 - Part 01"""

import typing as t
from itertools import product

from advent_of_code_2024.day_13.common import (
    ClawMachine,
    initialize_claw_machines,
)


def compute_minimum_tokens_for_prize(
    claw_machine: ClawMachine,
    max_presses: int = 100,
) -> int | None:
    """Compute the minimum tokens required to get the prize.

    Args:
        claw_machine (ClawMachine): Instance of the ClawMachine.
        max_presses (int, optional): Maximum number of presses. Defaults to 100.

    Returns:
        int | None: Minimum tokens required to get the prize or None.
    """
    for a_presses, b_presses in product(range(max_presses + 1), repeat=2):
        current_x = (
            a_presses * claw_machine.button_a.x_shift
            + b_presses * claw_machine.button_b.x_shift
        )
        current_y = (
            a_presses * claw_machine.button_a.y_shift
            + b_presses * claw_machine.button_b.y_shift
        )

        if (
            current_x == claw_machine.prize.x
            and current_y == claw_machine.prize.y
        ):
            cost = a_presses * 3 + b_presses * 1
            print(
                a_presses,
                b_presses,
                claw_machine.button_a.x_shift,
                claw_machine.button_a.y_shift,
                claw_machine.button_b.x_shift,
                claw_machine.button_b.y_shift,
                claw_machine.prize.x,
                claw_machine.prize.y,
            )
            return cost

    print(
        None,
        None,
        claw_machine.button_a.x_shift,
        claw_machine.button_a.y_shift,
        claw_machine.button_b.x_shift,
        claw_machine.button_b.y_shift,
        claw_machine.prize.x,
        claw_machine.prize.y,
    )
    return None


def main() -> None:
    """Main function."""
    claw_machines: t.List[ClawMachine] = initialize_claw_machines(
        "input.txt", __file__
    )
    minimum_tokens_count: int = 0
    for claw_machine in claw_machines:
        minimum_tokens_for_prize = compute_minimum_tokens_for_prize(
            claw_machine
        )
        if minimum_tokens_for_prize is not None:
            minimum_tokens_count += minimum_tokens_for_prize
    print(minimum_tokens_count)


if __name__ == "__main__":
    main()
