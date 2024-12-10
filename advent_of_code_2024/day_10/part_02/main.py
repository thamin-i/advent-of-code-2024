"""Advent of code - Day 10 - Part 02"""

import typing as t

from advent_of_code_2024.day_10.common import (
    find_trailheads,
    is_valid_position,
    read_topographic_map,
)


def compute_rating(
    topographic_map: t.List[t.List[int]],
    start: t.Tuple[int, int],
    max_height: int = 9,
) -> int:
    """Compute the rating of a trailhead.

    Args:
        topographic_map (t.List[t.List[int]]): Topographic map.
        start (t.Tuple[int, int]): Start position.
        max_height (int, optional): Maximum height. Defaults to 9.

    Returns:
        int: Rating of the trailhead.
    """
    rows_count: int = len(topographic_map)
    columns_count: int = len(topographic_map[0])
    directions: t.List[t.Tuple[int, int]] = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    paths_count: t.List[t.List[int]] = [
        [0] * columns_count for _ in range(rows_count)
    ]
    paths_count[start[0]][start[1]] = 1
    for current_height in range(max_height + 1):
        for row in range(rows_count):
            for column in range(columns_count):
                if (
                    topographic_map[row][column] == current_height
                    and paths_count[row][column] > 0
                ):
                    for row_offset, column_offset in directions:
                        neighbor_row: int = row + row_offset
                        neighbor_column: int = column + column_offset
                        if (
                            is_valid_position(
                                neighbor_row, neighbor_column, topographic_map
                            )
                            and topographic_map[neighbor_row][neighbor_column]
                            == current_height + 1
                        ):
                            paths_count[neighbor_row][
                                neighbor_column
                            ] += paths_count[row][column]

    rating: int = 0
    for row in range(rows_count):
        for column in range(columns_count):
            if topographic_map[row][column] == max_height:
                rating += paths_count[row][column]
    return rating


def main() -> None:
    """Main function."""
    topographic_map: t.List[t.List[int]] = read_topographic_map(
        "input.txt", __file__
    )
    rating = 0
    for trailhead in find_trailheads(topographic_map):
        rating += compute_rating(topographic_map, trailhead)
    print(rating)


if __name__ == "__main__":
    main()
