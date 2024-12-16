"""Advent of code - Day 15 - Part 01"""

import os
import typing as t
from enum import Enum


class DirectionEnum(Enum):
    """Direction enum class."""

    UP = "^"
    DOWN = "v"
    LEFT = "<"
    RIGHT = ">"


def compute_gps_coordinate(position: t.Tuple[int, int]) -> int:
    position_x, position_y = position
    return position_y * 100 + position_x


def sum_gps_coordinates(positions: t.List[t.Tuple[int, int]]) -> int:
    return sum([compute_gps_coordinate(position) for position in positions])


def get_new_position(
    position: t.Tuple[int, int],
    direction: DirectionEnum,
) -> t.Tuple[int, int]:
    x, y = position
    match direction:
        case DirectionEnum.UP:
            return (x, y - 1)
        case DirectionEnum.DOWN:
            return (x, y + 1)
        case DirectionEnum.LEFT:
            return (x - 1, y)
        case DirectionEnum.RIGHT:
            return (x + 1, y)
    return position


def print_warehouse(
    warehouse_size: t.Tuple[int, int],
    walls: t.List[t.Tuple[int, int]],
    robot: t.Tuple[int, int],
    boxes: t.List[t.Tuple[int, int]],
) -> None:
    print()
    for y in range(warehouse_size[1]):
        for x in range(warehouse_size[0]):
            match (x, y):
                case (x, y) if (x, y) in walls:
                    print("#", end="")
                case (x, y) if (x, y) == robot:
                    print("@", end="")
                case (x, y) if (x, y) in boxes:
                    print("O", end="")
                case _:
                    print(".", end="")
        print()
    print()


def move(
    warehouse_size: t.Tuple[int, int],
    robot: t.Tuple[int, int],
    boxes: t.List[t.Tuple[int, int]],
    walls: t.List[t.Tuple[int, int]],
    directions: t.List[DirectionEnum],
) -> t.Tuple[t.Tuple[int, int], t.List[t.Tuple[int, int]]]:
    for direction in directions:
        new_robot = get_new_position(robot, direction)

        if new_robot in walls:
            continue  # Wall encountered, do nothing

        # Check for all boxes in a line
        current_position = new_robot
        moving_boxes = []

        while current_position in boxes:
            moving_boxes.append(current_position)
            next_position = get_new_position(current_position, direction)
            if next_position in walls:
                moving_boxes = []
                new_robot = robot
                break
            current_position = next_position

        # Move all boxes if no wall or other boxes was encountered
        for moving_box in moving_boxes:
            boxes.remove(moving_box)
            boxes.append(get_new_position(moving_box, direction))

        robot = new_robot
    print_warehouse(warehouse_size, walls, robot, boxes)
    return robot, boxes


def parse_file(file_name: str, from_file: str) -> t.Tuple[
    t.Tuple[int, int],
    t.Tuple[int, int],
    t.List[t.Tuple[int, int]],
    t.List[t.Tuple[int, int]],
    t.List[DirectionEnum],
]:
    """Initialize robot using configuration from a txt file.

    Args:
        file_name (str): Input file name.
        from_file (str): File from where the method is called.

    Returns:
        t.Tuple[
            int,
            t.Tuple[int, int],
            t.List[t.Tuple[int, int]],
            t.List[t.Tuple[int, int]],
            t.List[DirectionEnum],
        ]: An instantiated robot.
    """
    absolute_path_to_file: str = os.path.realpath(
        os.path.join(os.getcwd(), os.path.dirname(from_file), file_name)
    )

    lines: list[str] = []
    with open(absolute_path_to_file, "r", encoding="utf-8") as file_descriptor:
        lines = [line.strip() for line in file_descriptor.readlines()]

    map_lines = [
        line
        for line in lines
        if ">" not in line
        and "<" not in line
        and "v" not in line
        and "^" not in line
        and len(line)
    ]

    directions: t.List[DirectionEnum] = [
        DirectionEnum(direction)
        for direction in "".join(
            [
                line
                for line in lines
                if ">" in line or "<" in line or "v" in line or "^" in line
            ]
        )
    ]

    warehouse_size: t.Tuple[int, int] = (len(map_lines[0]), len(map_lines))
    robot: t.Tuple[int, int] | None = None
    boxes: t.List[t.Tuple[int, int]] = []
    walls: t.List[t.Tuple[int, int]] = []

    for y, line in enumerate(map_lines):
        for x, char in enumerate(line):
            match char:
                case "#":
                    walls.append((x, y))
                case "@":
                    robot = (x, y)
                case "O":
                    boxes.append((x, y))

    if robot is None:
        raise ValueError("Robot not found in the warehouse.")

    return warehouse_size, robot, boxes, walls, directions


def main() -> None:
    """Main function."""
    warehouse_size, robot, boxes, walls, directions = parse_file(
        file_name="input.txt", from_file=__file__
    )
    robot, boxes = move(warehouse_size, robot, boxes, walls, directions)
    final_gps_count = sum_gps_coordinates(boxes)
    print(final_gps_count)


if __name__ == "__main__":
    main()
