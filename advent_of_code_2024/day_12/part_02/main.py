"""Advent of code - Day 12 - Part 02"""

import typing as t
from collections import deque

from advent_of_code_2024.day_12.common import read_garden_map


def has_neighbour(
    point: t.Tuple[int, int],
    area_points: t.List[t.Tuple[int, int]],
    direction: t.Tuple[int, int],
) -> bool:
    """Check if a point has a neighbour in a specific direction.

    Args:
        point (t.Tuple[int, int]):
            Point coordinates.
        area_points (t.List[t.Tuple[int, int]]):
            List of points in the same area.
        direction (t.Tuple[int, int]):
            Direction to check.

    Returns:
        bool: True if the point has a neighbour in the direction.
    """
    nx, ny = point[0] + direction[0], point[1] + direction[1]
    if (nx, ny) in area_points:
        return True
    return False


def count_islands(line: t.List[bool]) -> int:
    """Count islands of booleans in a list of booleans.

    Args:
        line (t.List[bool]): List of booleans.

    Returns:
        int: Number of islands.
    """
    count = 0
    previous = False

    for current in line:
        if current and not previous:
            count += 1
        previous = current
    return count


def compute_sides(
    garden_map: t.List[t.List[str]],
    area_points: t.List[t.Tuple[int, int]],
) -> int:
    """Compute sides of a plant region.

    Args:
        garden_map (t.List[t.List[str]]): Garden map.
        area_points (t.List[t.Tuple[int, int]]): List of points in the area.

    Returns:
        int: Sides of the plant region.
    """
    count = 0

    for pos_x, row in enumerate(garden_map):
        line = []
        for pos_y in range(len(row)):
            line.append(
                (pos_x, pos_y) in area_points
                and not has_neighbour((pos_x, pos_y), area_points, (-1, 0))
            )
        count += count_islands(line)

    for pos_x, row in enumerate(garden_map):
        line = []
        for pos_y in range(len(row)):
            line.append(
                (pos_x, pos_y) in area_points
                and not has_neighbour((pos_x, pos_y), area_points, (1, 0))
            )
        count += count_islands(line)

    for pos_y in range(len(garden_map[0])):
        line = []
        for pos_x in range(len(garden_map)):
            line.append(
                (pos_x, pos_y) in area_points
                and not has_neighbour((pos_x, pos_y), area_points, (0, -1))
            )
        count += count_islands(line)

    for pos_y in range(len(garden_map[0])):
        line = []
        for pos_x in range(len(garden_map)):
            line.append(
                (pos_x, pos_y) in area_points
                and not has_neighbour((pos_x, pos_y), area_points, (0, 1))
            )
        count += count_islands(line)

    return count


def compute_area_and_sides(
    garden_map: t.List[t.List[str]],
    pos_x: int,
    pos_y: int,
    plant: str,
    visited: t.List[t.List[bool]],
) -> t.Tuple[int, int]:
    """Compute area and sides of a plant region.

    Args:
        garden_map (t.List[t.List[str]]): Garden map.
        pos_x (int): Initial position x.
        pos_y (int): Initial position y.
        plant (str): Plant name.
        visited (t.List[t.List[bool]]): List of visited positions.

    Returns:
        t.Tuple[int, int]: Area and sides of the plant region.
    """
    rows: int = len(garden_map)
    columns: int = len(garden_map[0])
    plants_positions: t.List[t.Tuple[int, int]] = []
    directions: t.List[t.Tuple[int, int]] = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    queue: t.Deque[t.Tuple[int, int]] = deque([(pos_x, pos_y)])
    visited[pos_x][pos_y] = True
    while queue:
        current_x, current_y = queue.popleft()
        plants_positions.append((current_x, current_y))

        for direction_x, direction_y in directions:
            new_x, new_y = current_x + direction_x, current_y + direction_y
            if (
                new_x < 0
                or new_y < 0
                or new_x >= rows
                or new_y >= columns
                or garden_map[new_x][new_y] != plant
            ):
                pass
            elif not visited[new_x][new_y]:
                visited[new_x][new_y] = True
                queue.append((new_x, new_y))

    sides = compute_sides(garden_map, plants_positions)
    return len(plants_positions), sides


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
                area, perimeter = compute_area_and_sides(
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
    for region in regions:
        print(f"Plant: {region[0]}, Area: {region[1]}, Perimeter: {region[2]}")
    print()
    price: int = compute_fences_price(regions)
    print(f"Price: {price}")


if __name__ == "__main__":
    main()

# 854887 is too low
