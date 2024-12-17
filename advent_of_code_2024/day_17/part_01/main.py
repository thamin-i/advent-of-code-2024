"""Advent of code - Day 17 - Part 01"""

from advent_of_code_2024.day_17.common import Computer, initialize_computer


def main() -> None:
    """Main function."""
    computer: Computer = initialize_computer(
        file_name="input.txt", from_file=__file__
    )
    print(computer)
    output: str = computer.run()
    print(output)


if __name__ == "__main__":
    main()
