"""
This module contains the Directory class, which is used to represent a directory in the file
system. The Directory class is used to create a tree structure of directories and files, and to
create a dataframe of all files in the directory tree.
"""

from dataclasses import dataclass, field
import logging
from pathlib import Path

import pandas as pd
import yaml

from .file import File
from .filetree import FileTree
from ..metadata import Metadata

logger = logging.getLogger(__name__)


@dataclass
class Directory:
    """
    Represents a directory in the file system.

    Attributes:
        path (Path): The path to the directory.
        parent (Directory): The parent directory of this directory.
        children (list[Directory]): The child directories of this directory.
        files (list[File]): The files in this directory.
        metadata_filename (str): The name of the metadata file in this directory.

    Properties:
        name (str): The name of the directory.
        metadata (Metadata): The metadata of the directory.
        all_descendants (list[Directory]): All descendant directories of this directory.

    Methods:
        get_metadata: Load the metadata file in this directory, or create a new metadata object.
        as_dataframe: Create a dataframe of all files in the directory tree.
    """

    path: Path
    parent: "Directory" = None
    children: list["Directory"] = field(default_factory=list, repr=False)
    files: list[File] = field(default_factory=list, repr=False)
    metadata_filename = "README.yaml"

    _filetree: FileTree = field(default=None, repr=False)

    @property
    def name(self):
        """
        The name of the directory.
        """
        return self.path.name

    @property
    def metadata(self):
        """
        The metadata of the directory.
        """
        if self._metadata is None:
            self._metadata = self.get_metadata()
        return self._metadata

    @property
    def self_and_descendants(self):
        """
        All descendant directories of this directory.
        """
        descendants = [self]
        for child in self.children:
            descendants.extend(child.self_and_descendants)
        return descendants

    @property
    def filetree(self) -> str:
        """
        Get the filetree of the directory as a string.
        """
        return self._filetree.as_string()

    @property
    def dataset_action(self) -> dict[str, str]:
        """
        There is a very specific metadata attribute we can look for that the user can update to
        specify what action should be taken on the data in this directory.

        Will be one of:
        - "include"
        - "exclude"
        - "redact"

        The reuturned dictionary will be in the form:
        {
            "action": "include" | "exclude" | "redact",
            "pattern": "regex pattern to match files to apply action to" | None
        }

        Returns:
            dict[str, str]: The action to take on the dataset in the directory.
        """
        if (
            "Dataset" not in self.metadata
            or "potentialAction" not in self.metadata["Dataset"]
        ):
            return {
                "action": "include",
                "pattern": ".*",
            }

        action = self.metadata["Dataset"].get("potentialAction", [{"name": "include"}])
        return {
            "action": action[0]["name"],
            "pattern": action[0].get("pattern", ".*"),
        }

    @property
    def path_depth(self) -> int:
        """
        Get the number of folders that appear above this one in the directory tree.
        """
        if self.parent == self:
            return 0

        return self.parent.path_depth + 1

    def __post_init__(self):
        # If the directory has no parent, it is the root directory.
        if self.parent is None:
            self.parent = self

        # If the directory has no children, it is a leaf directory.
        if self.children is None:
            self.children = []

        # If the directory has no files, it is an empty directory.
        if self.files is None:
            self.files = []

        self._metadata = None

        self._filetree = FileTree(self.path)

        logger.debug("Created directory object %s", self.path)

    @property
    def file_dataframe(self) -> pd.DataFrame:
        """
        Get a dataframe of all files in the directory tree.

        Returns:
            pd.DataFrame: A dataframe of all files in the directory tree.
        """
        df = pd.DataFrame([file.get_file_metadata() for file in self.files])
        full_df = pd.concat([df] + [child.file_dataframe for child in self.children])
        return full_df

    @property
    def num_excluded_files(self) -> int:
        """
        Get the number of files in the directory tree that are excluded.

        Returns:
            int: The number of files in the directory tree that are excluded.
        """
        if "Action" not in self.file_dataframe:
            return 0

        return sum(self.file_dataframe["Action"] == "exclude")

    def get_metadata(self) -> Metadata:
        """
        Get the metadata of the directory.

        If the metadata file exists, load it. Otherwise, create a new metadata object. If this
        directory is not the root directory, supplement the metadata with the metadata of the
        parent directory.

        Returns:
            Metadata: The metadata of the directory.
        """
        # Create a path to the metadata file in this directory.
        metadata_path = self.path / self.metadata_filename

        # Load the metadata file if it exists, otherwise create a new metadata object.
        my_metadata = (
            Metadata.load(metadata_path) if metadata_path.exists() else Metadata()
        )

        # If this directory is not the root directory, supplement the metadata with the
        if self.parent != self:
            my_metadata.supplement(self.parent.metadata)

        return my_metadata

    def as_dataframe(self) -> pd.DataFrame:
        """
        Create a dataframe of all files in the directory tree.

        Returns:
            pd.DataFrame: A dataframe of all files in the directory tree.
        """
        logger.debug("Creating dataframe for directory %s", self.path)
        # Create a dataframe by collecting all files in this directory as records.
        df = pd.DataFrame([file.as_record() for file in self.files])

        # Extend the dataframe by collecting all files in the child directories as records.
        df = pd.concat([df] + [child.as_dataframe() for child in self.children])

        return df

    def metadata_as_plaintext(self) -> dict[str, str]:
        """
        Create a dictionary of the directory tree in plaintext.

        Keys are the root items in the metadata

        Returns:
            dict[str, str]: A dictionary of the directory tree in plaintext.
        """
        logger.debug("Creating plaintext for directory %s", self.path)

        return_dict = {}
        for key, value in self.get_metadata().items():
            return_dict[key] = yaml.dump(value, default_flow_style=False)

        return return_dict

    def file_records_dataframe(self) -> pd.DataFrame:
        """
        Create a dataframe of all files in the directory tree.

        Returns:
            pd.DataFrame: A dataframe of all files in the directory tree.
        """
        full_df = self.file_dataframe.copy()

        # Strip out any records where the Action is "exclude"
        if "Action" in full_df.columns:
            full_df = full_df[full_df["Action"] != "exclude"]

        return full_df
