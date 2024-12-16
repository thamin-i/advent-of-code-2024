"""Advent of code - Day 15 - Part 02"""

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
    """Compute GPS coordinate.

    Args:
        position (t.Tuple[int, int]):
            Position used to compute the GPS coordinate.

    Returns:
        int: GPS coordinate.
    """
    position_x, position_y = position
    return position_y * 100 + position_x


def sum_gps_coordinates(positions: t.List[t.Tuple[int, int]]) -> int:
    """Sum GPS coordinates of all positions.

    Args:
        positions (t.List[t.Tuple[int, int]]): List of positions.

    Returns:
        int: Sum of GPS coordinates.
    """
    return sum([compute_gps_coordinate(position) for position in positions])


def get_new_position(
    position: t.Tuple[int, int], direction: DirectionEnum
) -> t.Tuple[int, int]:
    """Get new position based on current position and direction.


    Args:
        position (t.Tuple[int, int]): Initial position.
        direction (DirectionEnum): Direction to move to.

    Returns:
        t.Tuple[int, int]: New position.
    """
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
    boxes: t.Dict[t.Tuple[int, int], t.Tuple[int, int]],
) -> None:
    """Print warehouse.

    Args:
        warehouse_size (t.Tuple[int, int]):
            Warehouse size (width, height).
        walls (t.List[t.Tuple[int, int]]):
            List of walls.
        robot (t.Tuple[int, int]):
            Robot position.
        boxes (t.Dict[t.Tuple[int, int], t.Tuple[int, int]]):
            Dictionary of boxes.
    """
    left_boxes: t.List[t.Tuple[int, int]] = list(boxes.keys())
    right_boxes: t.List[t.Tuple[int, int]] = list(boxes.values())
    for y in range(warehouse_size[1]):
        for x in range(warehouse_size[0]):
            pos = (x, y)
            match pos:
                case pos if pos in walls:
                    print("#", end="")
                case pos if pos == robot:
                    print("@", end="")
                case pos if pos in left_boxes:
                    print("[", end="")
                case pos if pos in right_boxes:
                    print("]", end="")
                case _:
                    print(".", end="")
        print()
    print()


def rec_compute_moving_boxes(
    current_position: t.Tuple[int, int],
    direction: DirectionEnum,
    left_boxes_dict: t.Dict[t.Tuple[int, int], t.Tuple[int, int]],
    right_boxes_dict: t.Dict[t.Tuple[int, int], t.Tuple[int, int]],
    walls: t.List[t.Tuple[int, int]],
    visited: t.List[t.Tuple[int, int]],
) -> t.List[t.Tuple[int, int]]:
    """Recursively compute moving boxes.

    Args:
        current_position (t.Tuple[int, int]):
            Current position.
        direction (DirectionEnum):
            Direction to move to.
        left_boxes_dict (t.Dict[t.Tuple[int, int], t.Tuple[int, int]]):
            Dictionary of left boxes.
        right_boxes_dict (t.Dict[t.Tuple[int, int], t.Tuple[int, int]]):
            Dictionary of right boxes.
        walls (t.List[t.Tuple[int, int]]):
            List of walls.
        visited (t.List[t.Tuple[int, int]]):
            List of visited positions.

    Returns:
        t.List[t.Tuple[int, int]]: List of boxes that needs to move.
    """
    if current_position in visited:
        return []

    if current_position in walls:
        raise ValueError("Wall encountered")

    visited.append(current_position)

    position_1 = None
    position_2 = None
    if current_position in left_boxes_dict.keys():
        position_1 = current_position
        position_2 = left_boxes_dict.get(current_position)
    elif current_position in right_boxes_dict.keys():
        position_1 = right_boxes_dict.get(current_position)
        position_2 = current_position

    if position_1 is not None and position_2 is not None:
        new_position_1 = get_new_position(position_1, direction)
        new_position_2 = get_new_position(position_2, direction)
        return (
            rec_compute_moving_boxes(
                new_position_1,
                direction,
                left_boxes_dict,
                right_boxes_dict,
                walls,
                visited,
            )
            + rec_compute_moving_boxes(
                new_position_2,
                direction,
                left_boxes_dict,
                right_boxes_dict,
                walls,
                visited,
            )
            + [position_1]
        )

    return []


def move(
    warehouse_size: t.Tuple[int, int],
    robot: t.Tuple[int, int],
    boxes: t.Dict[tuple[int, int], tuple[int, int]],
    walls: t.List[t.Tuple[int, int]],
    directions: t.List[DirectionEnum],
) -> t.Tuple[t.Tuple[int, int], t.Dict[t.Tuple[int, int], t.Tuple[int, int]]]:
    """Move robot and boxes.

    Args:
        warehouse_size (t.Tuple[int, int]):
            Warehouse size (width, height).
        robot (t.Tuple[int, int]):
            Robot position.
        boxes (t.Dict[tuple[int, int], tuple[int, int]]):
            List of boxes.
        walls (t.List[t.Tuple[int, int]]):
            List of walls.
        directions (t.List[DirectionEnum]):
            List of directions.

    Returns:
        t.Tuple[
            t.Tuple[int, int],
            t.Dict[t.Tuple[int, int], t.Tuple[int, int]]
        ]:
            New robot position and new boxes positions.
    """
    for direction in directions:
        new_robot = get_new_position(robot, direction)

        if new_robot in walls:
            # Robot would encounter a wall, stop here.
            continue

        current_position = new_robot
        moving_boxes: t.Set[t.Tuple[int, int]] = set()

        left_boxes_dict: t.Dict[tuple[int, int], tuple[int, int]] = boxes
        right_boxes_dict = {
            right: left for left, right in left_boxes_dict.items()
        }
        try:
            moving_boxes = set(
                rec_compute_moving_boxes(
                    current_position,
                    direction,
                    boxes,
                    right_boxes_dict,
                    walls,
                    [],
                )
            )
        except ValueError:
            # Boxes would encounter at least a wall, stop here.
            continue

        for moving_box in sorted(
            moving_boxes,
            key=lambda x: (
                x[1]
                if direction in [DirectionEnum.UP, DirectionEnum.DOWN]
                else x[0]
            ),
            reverse=direction in [DirectionEnum.DOWN, DirectionEnum.RIGHT],
        ):
            del boxes[moving_box]
            new_position = get_new_position(moving_box, direction)
            boxes[new_position] = new_position[0] + 1, new_position[1]

        robot = new_robot
    return robot, boxes


def parse_file(file_name: str, from_file: str) -> t.Tuple[
    t.Tuple[int, int],
    t.Tuple[int, int],
    t.Dict[t.Tuple[int, int], t.Tuple[int, int]],
    t.List[t.Tuple[int, int]],
    t.List[DirectionEnum],
]:
    """Initialize robot using configuration from a txt file.

    Args:
        file_name (str): Input file name.
        from_file (str): File from where the method is called.

    Returns:
        t.Tuple[
        t.Tuple[int, int],
        t.Tuple[int, int],
        t.List[t.Tuple[int, int]],
        t.List[DirectionEnum]
    ]: Lot of things
    """
    absolute_path_to_file = os.path.realpath(
        os.path.join(os.getcwd(), os.path.dirname(from_file), file_name)
    )

    lines = []
    with open(absolute_path_to_file, "r", encoding="utf-8") as file_descriptor:
        lines = [line.strip() for line in file_descriptor.readlines()]

    map_lines = [
        line.replace("#", "##")
        .replace("O", "[]")
        .replace(".", "..")
        .replace("@", "@.")
        for line in lines
        if not any(dir_char in line for dir_char in ["^", "v", "<", ">"])
        and len(line)
    ]

    directions = [
        DirectionEnum(direction)
        for direction in "".join(
            [
                line
                for line in lines
                if any(dir_char in line for dir_char in ["^", "v", "<", ">"])
            ]
        )
    ]

    warehouse_size = (len(map_lines[0]), len(map_lines))
    robot = None
    boxes = {}
    walls = []

    for y, line in enumerate(map_lines):
        for x, char in enumerate(line):
            match char:
                case "#":
                    walls.append((x, y))
                case "@":
                    robot = (x, y)
                case "[":
                    boxes[(x, y)] = (x + 1, y)

    if robot is None:
        raise ValueError("Robot not found in the warehouse")
    return warehouse_size, robot, boxes, walls, directions


def main() -> None:
    """Main function."""
    warehouse_size, robot, boxes, walls, directions = parse_file(
        file_name="input.txt",
        from_file=__file__,
    )
    robot, boxes = move(warehouse_size, robot, boxes, walls, directions)
    final_gps_count = sum_gps_coordinates([left for left in boxes.keys()])
    print(final_gps_count)


if __name__ == "__main__":
    main()
