"""Advent of code - Day 17 - Part 02"""

from advent_of_code_2024.day_17.common import Computer, initialize_computer


def main() -> None:
    """Main function."""
    computer: Computer = initialize_computer(
        file_name="input.txt", from_file=__file__
    )
    print(computer)
    register_a: int = computer.fix_register_a()
    print(register_a)


if __name__ == "__main__":
    main()
