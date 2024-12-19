"""Advent of code - Day 19 - Part 02"""

from advent_of_code_2024.day_19.common import (
    count_possible_solutions,
    parse_input_file,
)


def main() -> None:
    """Main function."""
    towels, designs = parse_input_file(
        file_name="input.txt",
        from_file=__file__,
    )
    possible_solutions_count: int = sum(
        count_possible_solutions(design, towels) for design in designs
    )
    print(possible_solutions_count)


if __name__ == "__main__":
    main()
