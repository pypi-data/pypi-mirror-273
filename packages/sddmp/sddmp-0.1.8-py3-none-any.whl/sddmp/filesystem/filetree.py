# pylint: disable=too-few-public-methods

"""
This module contains the FileTree class, which is used to represent a directory tree in the file
system. The FileTree class is used to create a tree structure of directories as a string, similar
to the output of the `tree` command in Unix-like operating systems.
"""

import logging
from pathlib import Path

logger = logging.getLogger(__name__)


class FileTree:
    """
    This class represents a directory in the file system, and is used to create a tree structure of
    directories as a string, similar to the output of the `tree` command in Unix-like operating
    systems.
    """

    def __init__(self, directory: Path):
        self.directory = directory

    def as_string(self, level: int = 0) -> str:
        """
        Return the directory tree as a string.

        Args:
            level (int): The level of the directory in the tree.

        Returns:
            str: The directory tree as a string.
        """
        indent = "│   " * (level - 1) + "├── " if level > 0 else ""
        tree = f"{indent}{self.directory.name}\n"
        tree = ""
        children = list(self.directory.iterdir())
        for i, child in enumerate(children):
            if i == len(children) - 1:
                indent = "│   " * level + "└── "
            else:
                indent = "│   " * level + "├── "
            tree += f"{indent}{child.name}\n"
            if child.is_dir():
                child_tree = FileTree(child)
                tree += child_tree.as_string(level + 1)

        if level == 0:
            return self.directory.name + "\n" + tree

        return tree
