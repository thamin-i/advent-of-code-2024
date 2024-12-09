"""Advent of code - Day 09 - Part 01"""

from advent_of_code_2024.day_09.common import FileSystem


def main() -> None:
    """Main function."""
    file_system: FileSystem = FileSystem("input.txt", __file__)
    file_system.compact_disk_blocks_v1()
    print(file_system.compute_checksum())


if __name__ == "__main__":
    main()
