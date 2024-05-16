"""
This file represents the file system. It contains the FileSystem class, which is used to read a
directory and create a tree of Directory and File objects.
"""

import logging
from pathlib import Path
import re

from .directory import Directory
from .file import File
from ..config import Config

logger = logging.getLogger(__name__)


class FileSystem:
    """
    A class for representing the file system.

    Attributes:
        maximum_search_depth (int): The maximum depth to read the directory tree.

    Methods:
        read_directory: Reads a directory and creates a tree of Directory and File objects.
    """

    def __init__(self, config: Config):
        self.maximum_search_depth = config.maximum_search_depth
        self.ignore_pattern = config.ignore_pattern

    def read_directory(self, path: Path, parent: Directory = None) -> Directory:
        """
        Reads a directory and creates a tree of Directory and File objects.

        Applies recursively to all subdirectories, resulting in a tree of Directory and File
        objects.

        Args:
            path (Path): The path to the directory to read.
            parent (Directory): The parent directory of the directory to read.

        Returns:
            Directory: The directory object representing the directory and its contents.
        """
        # In case the path is provided as a string, convert it to a Path object.
        if not isinstance(path, Path):
            path = Path(path)

        directory = Directory(path=path, parent=parent)

        # Return early if the path depth exceeds the maximum search depth.
        if directory.path_depth >= self.maximum_search_depth:
            logging.debug(
                "Skipping %s because it exceeds the maximum depth.", directory.path
            )
            return directory

        # Iterate over the contents of the directory and add all files and subdirectories.
        for child in path.iterdir():
            # If the file or directory matches the ignore pattern, skip it.
            if re.match(self.ignore_pattern, child.name):
                logging.debug(
                    "Ignoring %s because it matches the ignore pattern.", child.name
                )
                continue

            if child.is_file():
                directory.files.append(File(path=child, parent=directory))
            elif child.is_dir():
                directory.children.append(self.read_directory(child, directory))
        return directory

    def get_directory(self, path: Path) -> Directory:
        """
        Returns a Directory object representing the directory and its contents.

        Args:
            path (Path): The path to the directory.

        Returns:
            Directory: The directory object representing the directory and its contents.
        """
        return self.read_directory(path)

    def get_file(self, path: Path) -> File:
        """
        Returns a File object representing the file.

        Args:
            path (Path): The path to the file.

        Returns:
            File: The file object representing the file.
        """
        return File(path=path, parent=Directory(path.parent))

    def get_directory_structure(
        self,
        directory: Directory,
    ) -> dict:
        """
        Get a nested list of all directories in the file system.

        Args:
            directory (Directory): The root directory to start from.

        Returns:
            dict: A dictionary representing the directory structure.
        """
        sorted_children = sorted(directory.children, key=lambda child: child.path.name)

        if self.maximum_search_depth:
            # Remove any children that hve a path_depth larger than the maximum depth.
            sorted_children = [
                child
                for child in sorted_children
                if child.path_depth <= self.maximum_search_depth
            ]

        structure = {
            "name": directory.path.name,
            "children": [
                self.get_directory_structure(child) for child in sorted_children
            ],
        }
        return structure
