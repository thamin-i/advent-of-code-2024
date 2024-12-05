"""Common methods for the Day 05"""

import os
import typing as t


def read_input_file(
    file_name: str,
    from_file: str,
) -> t.Tuple[t.Dict[int, t.List[int]], t.List[t.List[int]]]:
    """Read the input file and return the page ordering rules and updates.

    Args:
        file_name (str): Input file name.
        from_file (str): File from where the method is called.

    Returns:
        t.Tuple[t.Dict[int, t.List[int]], t.List[t.List[int]]]:
            Page ordering rules and updates.
    """
    absolute_path_to_file: str = os.path.realpath(
        os.path.join(os.getcwd(), os.path.dirname(from_file), file_name)
    )

    page_ordering_rules: t.Dict[int, t.List[int]] = {}
    updates: t.List[t.List[int]] = []
    with open(absolute_path_to_file, "r", encoding="utf-8") as file_descriptor:
        for line in file_descriptor.readlines():
            if "|" in line:
                if page_ordering_rules.get(int(line.split("|")[0])) is None:
                    page_ordering_rules[int(line.split("|")[0])] = []
                page_ordering_rules[int(line.split("|")[0])].append(
                    int(line.split("|")[1])
                )
            elif len(line.replace("\n", "")) > 0:
                updates.append(
                    [int(num) for num in line.split(",") if num != "\n"]
                )

    return page_ordering_rules, updates


def is_valid_update(
    page_ordering_rules: t.Dict[int, t.List[int]],
    update: t.List[int],
) -> bool:
    """Check if an update is valid or not.

    Args:
        page_ordering_rules (t.Dict[int, t.List[int]]): Page ordering rules.
        update (t.List[int]): Update to check.

    Returns:
        bool: Whether the update is valid or not.
    """
    for i, num in enumerate(update):
        for j in range(i, len(update)):
            if num in page_ordering_rules.get(update[j], []):
                return False
    return True
