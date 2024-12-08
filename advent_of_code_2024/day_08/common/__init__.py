"""Common methods for the Day 08"""

import os
import string
import typing as t


class Position:
    """Position class."""

    x: int
    y: int

    def __init__(self, pos_x: int, pos_y: int):
        self.x = pos_x
        self.y = pos_y

    def __repr__(self) -> str:
        """Representation method.

        Returns:
            str: Representation string.
        """
        return f"Position({self.x}, {self.y})"

    def __eq__(self, other: t.Any) -> bool:
        """Equality operator.

        Args:
            other (t.Any): Other object to compare.

        Returns:
            bool: True if the objects are equal, False otherwise.
        """
        if isinstance(other, Position):
            return self.x == other.x and self.y == other.y
        if isinstance(other, tuple) and len(other) == 2:
            return (self.x, self.y) == other
        return False

    def __hash__(self) -> int:
        """Hash method.

        Returns:
            int: Hash value.
        """
        return hash((self.x, self.y))


class Board:
    """Board class."""

    size_x: int
    size_y: int
    antennas: t.Dict[str, t.List[Position]]

    def __init__(self, size_x: int | None = None, size_y: int | None = None):
        if size_x is not None:
            self.size_x = size_x
        if size_y is not None:
            self.size_y = size_y
        self.antennas = {}

    def register_antenna(self, antenna: str, pos_x: int, pos_y: int) -> None:
        """Register an antenna in the board.

        Args:
            antenna (str): Antenna name.
            pos_x (int): Antenna position x.
            pos_y (int): Antenna position y.
        """
        if self.antennas.get(antenna) is None:
            self.antennas[antenna] = []
        self.antennas[antenna].append(Position(pos_x, pos_y))

    def is_out_of_board(self, position: Position) -> bool:
        """Check if a position is out of the board.

        Args:
            position (Position): Position to check.

        Returns:
            bool: True if the position is out of the board, False otherwise.
        """
        if position.x < 0 or position.x > self.size_x:
            return True
        if position.y < 0 or position.y > self.size_y:
            return True
        return False

    def __compute_antinodes_positions_v1(self, antenna: str) -> t.Set[Position]:
        """Compute antinodes positions for a specific antenna name.

        Args:
            antenna (str): Antenna name.

        Returns:
            t.Set[Position]: Set of antinodes positions.
        """
        antinodes_positions: t.Set[Position] = set()

        for i, position_1 in enumerate(self.antennas[antenna]):
            for j, position_2 in enumerate(self.antennas[antenna]):
                if i != j:
                    dx = position_2.x - position_1.x
                    dy = position_2.y - position_1.y

                    new_position = Position(
                        pos_x=position_2.x + dx,
                        pos_y=position_2.y + dy,
                    )

                    if new_position not in self.antennas[antenna]:
                        if not self.is_out_of_board(new_position):
                            antinodes_positions.add(new_position)

        return antinodes_positions

    def compute_all_antinodes_positions_v1(self) -> t.Set[Position]:
        """Compute all antinodes positions.

        Returns:
            t.Set[Position]: Set of antinodes positions.
        """
        antinodes_positions: t.Set[Position] = set()
        for antenna in self.antennas:
            antinodes_positions.update(
                self.__compute_antinodes_positions_v1(antenna)
            )
        return antinodes_positions

    def __compute_antinodes_positions_v2(self, antenna: str) -> t.Set[Position]:
        """Compute antinodes positions for a specific antenna name.

        Args:
            antenna (str): Antenna name.

        Returns:
            t.Set[Position]: Set of antinodes positions.
        """
        antinodes_positions: t.Set[Position] = set()

        for i, position_1 in enumerate(self.antennas[antenna]):
            for j, position_2 in enumerate(self.antennas[antenna]):
                if i != j:
                    dx = position_2.x - position_1.x
                    dy = position_2.y - position_1.y

                    new_pos_position: Position = Position(
                        pos_x=position_2.x + dx,
                        pos_y=position_2.y + dy,
                    )
                    while not self.is_out_of_board(new_pos_position):
                        antinodes_positions.add(new_pos_position)
                        new_pos_position = Position(
                            pos_x=new_pos_position.x + dx,
                            pos_y=new_pos_position.y + dy,
                        )

                    new_neg_position: Position = Position(
                        pos_x=position_1.x + dx,
                        pos_y=position_1.y + dy,
                    )
                    while not self.is_out_of_board(new_neg_position):
                        antinodes_positions.add(new_neg_position)
                        new_neg_position = Position(
                            pos_x=new_neg_position.x - dx,
                            pos_y=new_neg_position.y - dy,
                        )

        return antinodes_positions

    def compute_all_antinodes_positions_v2(self) -> t.Set[Position]:
        """Compute all antinodes positions.

        Returns:
            t.Set[Position]: Set of antinodes positions.
        """
        antinodes_positions: t.Set[Position] = set()
        for antenna in self.antennas:
            antinodes_positions.update(
                self.__compute_antinodes_positions_v2(antenna)
            )
        return antinodes_positions

    def print_board(self, antinodes: t.Set[Position] = set()) -> None:
        """Print the board.

        Args:
            antinodes (t.Set[Position], optional):
                Antinodes positions.
                Defaults to None.
        """
        for pos_x in range(self.size_x + 1):
            for pos_y in range(self.size_y + 1):
                if any(
                    Position(pos_x, pos_y) in positions
                    for positions in self.antennas.values()
                ):
                    for name, positions in self.antennas.items():
                        if Position(pos_x, pos_y) in positions:
                            print(name, end="")
                            break

                elif Position(pos_x, pos_y) in antinodes:
                    print("#", end="")

                else:
                    print(".", end="")

            print("")


def read_antennas_positions(
    file_name: str,
    from_file: str,
) -> Board:
    """Read antennas positions from a txt file.

    Args:
        file_name (str): Input file name.
        from_file (str): File from where the method is called.

    Returns:
        Board: The board with the antennas positions.
    """
    absolute_path_to_file: str = os.path.realpath(
        os.path.join(os.getcwd(), os.path.dirname(from_file), file_name)
    )

    antennas_chars: t.List[str] = list(
        string.ascii_uppercase + string.ascii_lowercase + string.digits
    )
    board: Board = Board()
    lines: t.List[str] = []
    with open(absolute_path_to_file, "r", encoding="utf-8") as file_descriptor:
        lines = file_descriptor.readlines()

    board.size_x = len(lines) - 1
    board.size_y = len(lines[0].strip()) - 1
    for pos_x, line in enumerate(lines):
        for pos_y, char in enumerate(line):
            if char in antennas_chars:
                board.register_antenna(char, pos_x, pos_y)

    return board
