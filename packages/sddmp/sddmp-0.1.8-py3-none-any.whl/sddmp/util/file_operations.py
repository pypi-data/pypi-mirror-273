"""
This file contains the FileOperations class, which tracks files to be deleted or created
as a result of the script. Let's us set a "dry_run" parameter, which prevents any actual changes
from being made to the file system. Instead, it logs the changes that would have been made.
"""

from contextlib import contextmanager
from dataclasses import dataclass, field
from io import StringIO, BytesIO
import logging
from pathlib import Path
import shutil
import uuid

logger = logging.getLogger(__name__)


@dataclass
class FileOperations:
    """
    This class is responsible for tracking all files which will be deleted or created by the
    script.
    """

    dry_run: bool = False

    deleted_files: list[str] = field(default_factory=list)
    deleted_directories: list[str] = field(default_factory=list)
    new_files: list[str] = field(default_factory=list)
    new_directories: list[str] = field(default_factory=list)

    target_directory: str = None

    temp_directory: str = field(default=str(uuid.uuid4()))

    def register_deleted_file(self, file: str):
        """
        Regiester a file as to be deleted

        Args:
            file (str): The path to the file to delete.
        """
        self.deleted_files.append(file)

    def register_deleted_directory(self, directory: str):
        """
        Register a directory to be deleted.

        Args:
            directory (str): The path to the directory to delete.
        """
        self.deleted_directories.append(directory)

    @contextmanager
    def new_file(self, path, mode="w", encoding="utf-8"):
        """
        Create a new file object for writing to a file.

        In addition to creating a file, will also log the file path.

        Args:
            path (str): The path to the file to create.
            mode (str): The mode to open the file in.
            encoding (str): The encoding to use when opening the file.

        Yields:
            file: The file object to write to.
        """
        if self.dry_run:
            if "b" in mode:
                yield BytesIO()
            else:
                yield StringIO()
            self.new_files.append(path)
            return

        temp_path = Path(self.temp_directory) / path
        temp_path.parent.mkdir(parents=True, exist_ok=True)

        try:
            # Open the file in binary mode if 'b' is in the mode
            if "b" in mode:
                f = open(temp_path, mode)  # pylint: disable=unspecified-encoding
            else:
                f = open(temp_path, mode, encoding=encoding)
            yield f
        finally:
            f.close()

        self.new_files.append(path)

    def delete_files(self):
        """
        Delete all files that have been registered for deletion.
        """

        logger.info("Deleting %d files", len(self.deleted_files))

        for file in self.deleted_files:
            logger.debug("Deleting file %s", file)
            if not self.dry_run:
                Path(file).unlink()

    def delete_directories(self):
        """
        Delete all directories that have been registered for deletion.
        """

        logger.info("Deleting %d directories", len(self.deleted_directories))

        # Sort the directories so we start at the deepest ones first
        self.deleted_directories.sort(key=lambda x: len(Path(x).parts), reverse=True)

        for directory in self.deleted_directories:
            # Check if the directory is empty
            if not list(directory.iterdir()):
                logger.debug("Deleting directory %s", directory)
                if not self.dry_run:
                    directory.rmdir()
            else:
                logger.error("Directory %s is not empty", directory)
                for file in directory.iterdir():
                    logger.error("Found file '%s'", file)
                raise FileExistsError(f"Directory {directory} is not empty")

    def perform_delete(self):
        """
        Delete all files and directories that have been registered for deletion.
        """
        self.delete_files()
        self.delete_directories()

    def perform_create(self):
        """
        Create all files that have been registered for creation.
        """

        logger.info("Creating %d files", len(self.new_files))

        # Create the target directory if it doesn't exist
        if not self.dry_run:
            Path(self.target_directory).mkdir(parents=True, exist_ok=True)

        # Iterate through the new files and copy them to the target directory
        for new_file in self.new_files:
            source = Path(self.temp_directory) / new_file
            target = Path(self.target_directory) / new_file

            logger.debug("Copying file %s to %s", source, target)
            if not self.dry_run:
                target.parent.mkdir(parents=True, exist_ok=True)
                source.replace(target)

    def perform_cleanup(self):
        """
        Remove any leftover directories and files from the temporary directory.
        """

        logging.debug("Deleting temporary directory %s", self.temp_directory)
        shutil.rmtree(self.temp_directory)
        assert not Path(self.temp_directory).exists()

    def execute(self):
        """
        Perform all of the actions registered to the FileOperations object.

        If the dry_run flag is set, this will log the actions that would have been taken
        without actually performing them.
        """
        if self.dry_run:
            logger.info("Dry run completed successfully")
            logger.info("== Would have deleted %d files ==", len(self.deleted_files))
            for deleted_file in self.deleted_files:
                logger.debug("- FILE TO DELETE: %s", deleted_file)
            logger.info(
                "== Would have deleted %d directories ==", len(self.deleted_directories)
            )
            for deleted_directory in self.deleted_directories:
                logger.debug("- DIRECTORY TO DELETE: %s", deleted_directory)
            logger.info("== Would have created %d files ==", len(self.new_files))
            for new_file in self.new_files:
                logger.debug("- FILE TO CREATE: %s", new_file)
            return

        self.perform_delete()
        self.perform_create()
        self.perform_cleanup()
