"""Advent of code - Day 12 - Part 01"""

import typing as t
from collections import deque

from advent_of_code_2024.day_12.common import read_garden_map


def compute_area_and_perimeter(
    garden_map: t.List[t.List[str]],
    pos_x: int,
    pos_y: int,
    plant: str,
    visited: t.List[t.List[bool]],
) -> t.Tuple[int, int]:
    """Compute area and perimeter of a plant region.

    Args:
        garden_map (t.List[t.List[str]]): Garden map.
        pos_x (int): Initial position x.
        pos_y (int): Initial position y.
        plant (str): Plant name.
        visited (t.List[t.List[bool]]): List of visited positions.

    Returns:
        t.Tuple[int, int]: Area and perimeter of the plant region.
    """
    rows: int = len(garden_map)
    columns: int = len(garden_map[0])
    area: int = 0
    perimeter: int = 0
    directions: t.List[t.Tuple[int, int]] = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    queue: t.Deque[t.Tuple[int, int]] = deque([(pos_x, pos_y)])
    visited[pos_x][pos_y] = True
    while queue:
        current_x, current_y = queue.popleft()
        area += 1

        for direction_x, direction_y in directions:
            new_x, new_y = current_x + direction_x, current_y + direction_y
            if (
                new_x < 0
                or new_y < 0
                or new_x >= rows
                or new_y >= columns
                or garden_map[new_x][new_y] != plant
            ):
                perimeter += 1
            elif not visited[new_x][new_y]:
                visited[new_x][new_y] = True
                queue.append((new_x, new_y))

    return area, perimeter


def compute_regions(
    garden_map: t.List[t.List[str]],
) -> t.List[t.Tuple[str, int, int]]:
    """Compute regions of plants in the garden.

    Args:
        garden_map (t.List[t.List[str]]): Garden map.

    Returns:
        t.List[t.Tuple[str, int, int]]:
            List of tuples containing the plant, its area and perimeter.
    """
    rows: int = len(garden_map)
    columns: int = len(garden_map[0])
    visited: t.List[t.List[bool]] = [[False] * columns for _ in range(rows)]
    regions: t.List[t.Tuple[str, int, int]] = []

    for pos_x in range(rows):
        for pos_y in range(columns):
            if not visited[pos_x][pos_y]:
                plant = garden_map[pos_x][pos_y]
                area, perimeter = compute_area_and_perimeter(
                    garden_map,
                    pos_x,
                    pos_y,
                    plant,
                    visited,
                )
                regions.append((plant, area, perimeter))

    return regions


def compute_fences_price(regions: t.List[t.Tuple[str, int, int]]) -> int:
    """Compute fences price based on the plants areas and perimeters.

    Args:
        regions (t.List[t.Tuple[str, int, int]]): List of plants regions.

    Returns:
        int: Fences price.
    """
    return sum(area * perimeter for _, area, perimeter in regions)


def main() -> None:
    """Main function."""
    garden_map: t.List[t.List[str]] = read_garden_map("input.txt", __file__)
    regions: t.List[t.Tuple[str, int, int]] = compute_regions(garden_map)
    fences_price: int = compute_fences_price(regions)
    print(fences_price)


if __name__ == "__main__":
    main()
