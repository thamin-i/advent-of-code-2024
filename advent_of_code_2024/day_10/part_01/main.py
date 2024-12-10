"""Advent of code - Day 10 - Part 01"""

import typing as t
from collections import deque

from advent_of_code_2024.day_10.common import (
    find_trailheads,
    is_valid_position,
    read_topographic_map,
)


def compute_score(
    topographic_map: t.List[t.List[int]],
    start: t.Tuple[int, int],
    max_height: int = 9,
) -> int:
    """Compute the score of a trailhead.

    Args:
        topographic_map (t.List[t.List[int]]): Topographic map.
        start (t.Tuple[int, int]): Start position.
        max_height (int, optional): Maximum height. Defaults to 9.

    Returns:
        int: Score of the trailhead.
    """
    bfs_queue: t.Deque[t.Tuple[int, int]] = deque([start])
    visited_positions: t.Set[t.Tuple[int, int]] = set([start])
    reachable_heights: t.Set[t.Tuple[int, int]] = set()
    directions: t.List[t.Tuple[int, int]] = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    while bfs_queue:
        row, column = bfs_queue.popleft()
        for row_offset, column_offset in directions:
            neighbor_row: int = row + row_offset
            neighbor_column: int = column + column_offset
            if (
                is_valid_position(
                    neighbor_row, neighbor_column, topographic_map
                )
                and (neighbor_row, neighbor_column) not in visited_positions
            ):
                if (
                    topographic_map[neighbor_row][neighbor_column]
                    == topographic_map[row][column] + 1
                ):
                    visited_positions.add((neighbor_row, neighbor_column))
                    bfs_queue.append((neighbor_row, neighbor_column))
                    if (
                        topographic_map[neighbor_row][neighbor_column]
                        == max_height
                    ):
                        reachable_heights.add((neighbor_row, neighbor_column))

    return len(reachable_heights)


def main() -> None:
    """Main function."""
    topographic_map: t.List[t.List[int]] = read_topographic_map(
        "input.txt", __file__
    )
    score: int = 0
    for trailhead in find_trailheads(topographic_map):
        score += compute_score(topographic_map, trailhead)
    print(score)


if __name__ == "__main__":
    main()
