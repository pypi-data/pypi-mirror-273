"""
This file handles loading the configuration from a TOML file for the application.

We define a default configuration, and then attempt to load the configuration from a TOML file.
If the file doesn't exist, we return the default configuration. If the file exists, we update the
default configuration with the values from the TOML file.
"""

from dataclasses import dataclass
import logging
import os
from pathlib import Path
import re
import sys

import toml

logger = logging.getLogger(__name__)

DEFAULT_SETTINGS = {
    "maximum_search_depth": 3,
    "metadata_filename": "README.yaml",
    "allowed_list": [],
    "ignored_list": ["^\\..*"],
    "output_directory": "sddmp",
}


@dataclass
class Config:
    """
    A simple class to hold the application configuration settings as attributes.
    """

    maximum_search_depth: int
    metadata_filename: str
    allowed_list: list[str]
    ignored_list: list[str]
    output_directory: str

    @property
    def ignore_pattern(self) -> str:
        """
        Returns a regex pattern for files and directories to ignore.
        """
        return "|".join(self.ignored_list)

    def set_output_directory(self, output_directory: str):
        """
        Set the output directory for the application.

        Let's us set the directory from the command line, while still raising a warning if the
        directory isn't empty.

        Args:
            output_directory (str): The path to the output directory.
        """
        self.output_directory = output_directory
        self._warn_on_existing_output_directory()

    def _warn_on_existing_output_directory(self):
        """
        Warn the user if the output directory already exists.
        """
        if os.path.exists(self.output_directory):
            logger.warning(
                "The output directory '%s' already exists. Files may be overwritten.",
                self.output_directory,
            )
            if input("Do you want to continue? (y/n): ").lower() != "y":
                sys.exit(0)

    def __post_init__(self):
        """
        Validate the configuration settings after they have been loaded.
        """
        if self.maximum_search_depth < 0:
            raise ValueError("`maximum_search_depth` must be a positive integer.")
        if not isinstance(self.metadata_filename, str):
            raise ValueError("`metadata_filename` must be a string.")
        if not isinstance(self.allowed_list, list):
            raise ValueError("`allowed_list` must be a list.")
        if not isinstance(self.ignored_list, list):
            raise ValueError("`ignored_list` must be a list.")

        self._warn_on_existing_output_directory()

        for pattern in self.ignored_list:
            try:
                re.compile(pattern)
            except re.error as e:
                raise ValueError(f"Invalid regex pattern in `ignored_list`: {e}") from e


def load_config() -> Config:
    """
    Load the application configuration from a TOML file.

    Returns:
        A dictionary containing the application settings.

    Raises:
        toml.TomlDecodeError: If there is an error parsing the TOML file.
    """

    # Create a copy of the default settings
    settings = DEFAULT_SETTINGS.copy()

    # Path to the configuration file
    config_file = os.getcwd() / Path("config.toml")

    # If the file doesn't exist, return the default settings
    if not config_file.exists():
        logger.info("No configuration file found. Using default settings.")
        return Config(**settings)

    # Load the configuration file
    try:
        with open(config_file, "r", encoding="utf-8") as file:
            config = toml.load(file)

            # Update the settings with the configuration file
            settings.update(config)
    except toml.TomlDecodeError as e:
        logger.error("Error parsing configuration file: %s", e)
        raise

    logger.info("Loaded configuration file. Using custom settings: %s", settings)

    try:
        my_config = Config(**settings)
        return my_config
    except (TypeError, ValueError) as e:
        logger.error("Error parsing configuration file: %s", e)
        raise
