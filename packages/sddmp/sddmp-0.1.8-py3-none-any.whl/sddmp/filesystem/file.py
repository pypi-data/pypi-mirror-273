"""
This file contains the File class, which is used to represent a file in the file system.
"""

from dataclasses import dataclass, field
import datetime
import logging
from pathlib import Path
import re
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .directory import Directory

logger = logging.getLogger(__name__)


@dataclass
class File:
    """
    A File object represents a file in the file system.

    Attributes:
        path (Path): The path to the file.
        parent (Directory): The parent directory of the file.

    Properties:
        file_metadata (dict): The metadata of the file.
        name (str): The name of the file.
        extension (str): The extension of the file.
        size (int): The size of the file in bytes.
        created (datetime): The date and time the file was created.
        modified (datetime): The date and time the file was last modified.

    Methods:
        get_file_metadata: Returns the metadata of the file.
        as_record: Returns the file metadata as a record.
    """

    DATE_FORMAT = "%d %B, %Y %H:%M"

    path: Path
    parent: "Directory" = field(default=None, repr=False)

    def __post_init__(self):
        self._metadata = None
        logger.debug("Created file object '%s'", self.path)

    @property
    def file_metadata(self) -> dict:
        """
        The metadata of the file as a dictionary.

        Returns:
            dict: The metadata of the file.
        """
        if self._metadata is None:
            self._metadata = self.get_file_metadata()
        return self._metadata

    @property
    def name(self) -> str:
        """
        The name of the file.

        Returns:
            str: The name of the file.
        """
        return self.path.name

    @property
    def extension(self) -> str:
        """
        The extension of the file.

        Returns:
            str: The extension of the file.
        """
        return self.path.suffix

    @property
    def size(self) -> int:
        """
        The size of the file in bytes.

        Returns:
            int: The size of the file in bytes.
        """
        return self.path.stat().st_size

    @property
    def created(self) -> datetime.datetime:
        """
        The date and time the file was created.

        Returns:
            datetime.datetime: The date and time the file was created.
        """
        return datetime.datetime.fromtimestamp(self.path.stat().st_ctime)

    @property
    def modified(self) -> datetime.datetime:
        """
        The date and time the file was last modified.

        Returns:
            datetime.datetime: The date and time the file was last modified.
        """
        return datetime.datetime.fromtimestamp(self.path.stat().st_mtime)

    @property
    def is_redacted(self) -> bool:
        """
        Whether the file is redacted.

        Returns:
            bool: Whether the file is redacted.
        """
        return self.parent.dataset_action["action"] == "redact" and re.search(
            self.parent.dataset_action["pattern"], self.name
        )

    @property
    def action(self) -> str:
        """
        The action to take on the file.

        Returns:
            str: The action to take on the file.
        """
        if self.is_excluded:
            return "exclude"
        if self.is_redacted:
            return "redact"
        return "include"

    @property
    def is_excluded(self) -> bool:
        """
        Whether the file is excluded.

        Returns:
            bool: Whether the file is excluded.
        """

        return bool(
            self.parent.dataset_action["action"] == "exclude"
            and re.search(self.parent.dataset_action["pattern"], self.name)
        )

    def get_file_metadata(self) -> dict:
        """
        Returns the metadata of the file.

        Returns:
            dict: The metadata of the file.
        """
        file_name = (
            f"XXXXXXXX{Path(self.name).suffix}" if self.is_redacted else self.name
        )

        return {
            "File Name": file_name,
            "Parent Directory": self.parent.name,
            "Extension": self.extension,
            "Action": self.action,
            "File Size (bytes)": self.size,
            "Date Created": self.created.strftime(self.DATE_FORMAT),
            "Last Modified": self.modified.strftime(self.DATE_FORMAT),
        }

    def as_record(self) -> dict:
        """
        Returns the file metadata as a dictionary record intended for creating a pandas
        DataFrame record. The record contains the metadata of the file and the metadata of its
        parent directory, flattened into a single dictionary.

        Returns:
            dict: The file metadata as a record.
        """
        logger.debug("Creating record for file '%s", self.path)
        return {**self.parent.metadata.flat, **self.file_metadata}
