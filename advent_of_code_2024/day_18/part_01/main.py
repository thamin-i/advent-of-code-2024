"""Advent of code - Day 18 - Part 01"""

import typing as t

from advent_of_code_2024.day_18.common import (
    BFSSolver,
    corrupt_memory_space,
    generate_memory_space,
    read_bytes_positions,
)


def main(
    start_position: t.Tuple[int, int],
    end_position: t.Tuple[int, int],
    memory_space_width: int,
    memory_space_height: int,
    max_corrupted_bytes: int,
) -> None:
    """Main function.

    Args:
        start_position (t.Tuple[int, int]):
            Start position in the memory space.
        end_position (t.Tuple[int, int]):
            End position in the memory space.
        memory_space_width (int):
            Memory space width.
        memory_space_height (int):
            Memory space height.
        max_corrupted_bytes (int):
            Maximum number of corrupted bytes in the memory space.
    """
    bytes_positions: t.List[t.Tuple[int, int]] = read_bytes_positions(
        file_name="input.txt",
        from_file=__file__,
    )
    memory_space: t.List[t.List[str]] = generate_memory_space(
        width=memory_space_width,
        height=memory_space_height,
    )
    corrupted_memory_space: t.List[t.List[str]] = corrupt_memory_space(
        memory_space=memory_space,
        bytes_positions=bytes_positions,
        max_bytes=max_corrupted_bytes,
    )
    steps_count: int = BFSSolver(
        maze=corrupted_memory_space
    ).compute_minimum_steps(
        start_position=start_position,
        end_position=end_position,
        print_maze=True,
    )
    print(steps_count)


if __name__ == "__main__":
    main(
        start_position=(0, 0),
        end_position=(70, 70),
        memory_space_width=70,
        memory_space_height=70,
        max_corrupted_bytes=1024,
    )
