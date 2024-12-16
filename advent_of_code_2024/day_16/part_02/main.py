"""Advent of code - Day 16 - Part 01"""

import heapq
import typing as t

from advent_of_code_2024.day_16.common import (
    DIRECTIONS,
    Node,
    compute_heuristic,
    parse_maze,
)


def a_star_search(
    maze: t.List[t.List[int]],
    start: t.Tuple[int, int],
    end: t.Tuple[int, int],
    direction: int,
) -> int:
    """Use A* search to find the minimum cost to reach the end position.

    Args:
        maze (t.List[t.List[int]]): Maze.
        start (t.Tuple[int, int]): Start position.
        end (t.Tuple[int, int]): End position.
        direction (int): Starting direction.

    Returns:
        int: Count of nodes in the all the best paths.
    """
    open_list: t.List[Node] = []
    closed_list: t.Set[t.Tuple[int, int, int]] = set()

    start_node = Node(
        x=start[0],
        y=start[1],
        direction=direction,
        cost=0,
        heuristic=compute_heuristic(start, end, divider=2),
    )
    heapq.heappush(open_list, start_node)

    minimum_cost: float = float("inf")
    best_nodes: t.Set[t.Tuple[int, int]] = set()

    while open_list:
        current_node: Node = heapq.heappop(open_list)

        if current_node.x == end[0] and current_node.y == end[1]:
            if minimum_cost < current_node.cost:
                return len(best_nodes)
            minimum_cost = current_node.cost
            tmp_node: Node | None = current_node
            while tmp_node is not None:
                best_nodes.add((tmp_node.x, tmp_node.y))
                tmp_node = tmp_node.parent

        closed_list.add(
            (current_node.x, current_node.y, current_node.direction)
        )

        for i in range(4):
            new_direction: int = (current_node.direction + i) % 4
            dx, dy = DIRECTIONS[new_direction]
            new_x: int = current_node.x + dx
            new_y: int = current_node.y + dy

            if (
                0 <= new_x < len(maze)
                and 0 <= new_y < len(maze[0])
                and maze[new_x][new_y] == 0
            ):
                if (new_x, new_y, new_direction) not in closed_list:
                    node_cost: int = current_node.cost + 1
                    if i in [1, 3]:
                        node_cost = current_node.cost + 1001
                    new_cost: int = node_cost
                    new_heuristic: float = compute_heuristic(
                        (new_x, new_y), end, divider=2
                    )
                    new_node = Node(
                        x=new_x,
                        y=new_y,
                        direction=new_direction,
                        cost=new_cost,
                        heuristic=new_heuristic,
                    )
                    new_node.parent = current_node
                    heapq.heappush(open_list, new_node)

    return len(best_nodes)


def main() -> None:
    """Main function."""
    maze, start, end = parse_maze(file_name="input.txt", from_file=__file__)
    best_nodes_count = a_star_search(maze, start, end, direction=1)
    print(best_nodes_count)


if __name__ == "__main__":
    main()
