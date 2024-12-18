"""Advent of code - Day 18 - Part 01"""

import typing as t

from advent_of_code_2024.day_18.common import (
    BFSSolver,
    corrupt_memory_space,
    generate_memory_space,
    read_bytes_positions,
)


def compute_first_byte_that_prevents_exit(
    start_position: t.Tuple[int, int],
    end_position: t.Tuple[int, int],
    bytes_positions: t.List[t.Tuple[int, int]],
    memory_space: t.List[t.List[str]],
) -> t.Tuple[int, int] | None:
    """Compute the first byte that prevents the exit.

    Args:
        start_position (t.Tuple[int, int]): Start position.
        end_position (t.Tuple[int, int]): End position.
        bytes_positions (t.List[t.Tuple[int, int]]): Bytes positions.
        memory_space (t.List[t.List[str]]): Memory space.

    Returns:
        t.Tuple[int, int] | None: First byte that prevents the exit.
    """
    bfs_solver = BFSSolver(maze=memory_space)
    shortest_path: t.List[t.Tuple[int, int]] | None = None
    idx: int = 0

    while (
        shortest_path := bfs_solver.compute_shortest_path(
            start_position=start_position,
            end_position=end_position,
        )
    ) is not None:
        while bytes_positions[idx] not in shortest_path:
            bfs_solver.maze = corrupt_memory_space(
                memory_space=memory_space,
                bytes_positions=[bytes_positions[idx]],
            )
            idx += 1
        bfs_solver.maze = corrupt_memory_space(
            memory_space=memory_space,
            bytes_positions=[bytes_positions[idx]],
        )
    return bytes_positions[idx] if idx < len(bytes_positions) else None


def main(
    start_position: t.Tuple[int, int],
    end_position: t.Tuple[int, int],
    memory_space_width: int,
    memory_space_height: int,
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
    """
    bytes_positions: t.List[t.Tuple[int, int]] = read_bytes_positions(
        file_name="input.txt",
        from_file=__file__,
    )
    memory_space: t.List[t.List[str]] = generate_memory_space(
        width=memory_space_width,
        height=memory_space_height,
    )
    bad_byte: t.Tuple[int, int] | None = compute_first_byte_that_prevents_exit(
        start_position=start_position,
        end_position=end_position,
        bytes_positions=bytes_positions,
        memory_space=memory_space,
    )
    print(bad_byte)


if __name__ == "__main__":
    main(
        start_position=(0, 0),
        end_position=(70, 70),
        memory_space_width=70,
        memory_space_height=70,
    )
