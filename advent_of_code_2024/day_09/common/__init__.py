"""Common methods for the Day 09"""

import os
import typing as t


class FileSystem:
    """File system class."""

    disk_map: t.List[int]
    disk_blocks: t.List[int | None]

    def __init__(
        self,
        file_name: str,
        from_file: str,
    ):
        self.disk_map = []
        self.disk_blocks = []
        self.__read_disk_map(file_name, from_file)
        self.__generate_disk_blocks()

    def __read_disk_map(
        self,
        file_name: str,
        from_file: str,
    ) -> None:
        """Read disk map from a txt file.

        Args:
            file_name (str): Input file name.
            from_file (str): File from where the method is called.
        """
        absolute_path_to_file: str = os.path.realpath(
            os.path.join(os.getcwd(), os.path.dirname(from_file), file_name)
        )

        with open(
            absolute_path_to_file, "r", encoding="utf-8"
        ) as file_descriptor:
            self.disk_map = [int(char) for char in file_descriptor.readline()]

    def __generate_disk_blocks(self) -> None:
        """Generate disk blocks from disk map."""
        id_number: int = 0
        is_free: bool = False
        for block in self.disk_map:
            if not is_free:
                for _ in range(block):
                    self.disk_blocks.append(id_number)
                id_number += 1
            else:
                for _ in range(block):
                    self.disk_blocks.append(None)
            is_free = not is_free

    def __is_block_free(self, block: int | None) -> bool:
        """Check if block is free.

        Args:
            block_id (int | None): Block to check.

        Returns:
            bool: True if block is free, False otherwise.
        """
        return block is None

    def __get_last_used_block(self) -> int | None:
        """Get last used block ID.

        Returns:
            int | None: Last used block ID.
        """
        for i in range(1, len(self.disk_blocks) + 1):
            if not self.__is_block_free(self.disk_blocks[-i]):
                return self.disk_blocks[-i]
        raise ValueError("No used block found.")

    def __free_last_used_block(self) -> None:
        """Free last used block."""
        for i in range(1, len(self.disk_blocks) + 1):
            if not self.__is_block_free(self.disk_blocks[-i]):
                self.disk_blocks[-i] = None
                return

    def compact_disk_blocks_v1(self) -> None:
        """Compact disk blocks."""
        compacted_blocks: bool = True
        while compacted_blocks:
            compacted_blocks = False
            for i, block in enumerate(self.disk_blocks):
                if self.__is_block_free(block) and any(
                    not self.__is_block_free(remaining_block)
                    for remaining_block in self.disk_blocks[i + 1 :]
                ):
                    self.disk_blocks = (
                        self.disk_blocks[0:i]
                        + [self.__get_last_used_block()]  # noqa: W503
                        + self.disk_blocks[i + 1 :]  # noqa: W503
                    )
                    self.__free_last_used_block()
                    compacted_blocks = True
                    break

    def __compute_block_size(
        self, start_idx: int, reverse: bool = False
    ) -> int:
        """Compute block size.

        Args:
            start_idx (int): Start index of the block.
            reverse (bool): Reverse the block. Defaults to False.

        Returns:
            int: Block size.
        """
        block_size: int = 0
        block_id: int | None = self.disk_blocks[start_idx]
        if not reverse:
            for i in range(start_idx, len(self.disk_blocks)):
                if block_id == self.disk_blocks[i]:
                    block_size += 1
                else:
                    break
        else:
            j: int = start_idx
            while abs(j) < len(self.disk_blocks) + 1:
                if block_id == self.disk_blocks[j]:
                    block_size += 1
                else:
                    break
                j -= 1
        return block_size

    def __move_block(
        self, block_id: int | None, block_start: int, block_size: int
    ) -> bool:
        i: int = 0
        while i < block_start:
            current_size: int = self.__compute_block_size(i)
            if current_size >= block_size and self.__is_block_free(
                self.disk_blocks[i]
            ):
                for j in range(block_start + 1 - block_size, block_start + 1):
                    self.disk_blocks[j] = None
                self.disk_blocks = (
                    self.disk_blocks[0:i]
                    + [block_id] * block_size  # noqa: W503
                    + self.disk_blocks[i + block_size :]  # noqa: W503
                )
                return True
            i += current_size
        return False

    def compact_disk_blocks_v2(self) -> None:
        """Compact disk blocks."""
        compacted_blocks: bool = True
        start: int = len(self.disk_blocks) - 1
        while compacted_blocks:
            compacted_blocks = False
            i: int = start
            while i >= 0:
                block_id: int | None = self.disk_blocks[i]
                block_size: int = self.__compute_block_size(i, reverse=True)
                if not self.__is_block_free(block_id) and any(
                    self.__is_block_free(remaining_block)
                    for remaining_block in self.disk_blocks[:i]
                ):
                    if self.__move_block(
                        block_id=block_id,
                        block_start=i,
                        block_size=block_size,
                    ):
                        compacted_blocks = True
                        start = i
                        break
                    else:
                        i -= block_size
                else:
                    i -= block_size

    def compute_checksum(self) -> int:
        """Compute checksum of the disk blocks.

        Returns:
            int: Checksum of the disk blocks.
        """
        return sum(
            i * block
            for i, block in enumerate(self.disk_blocks)
            if block is not None
        )
