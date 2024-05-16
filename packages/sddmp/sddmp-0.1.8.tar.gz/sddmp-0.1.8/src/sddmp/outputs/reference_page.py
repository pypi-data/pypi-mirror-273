# pylint: disable=too-few-public-methods

"""
This file contains the ReferencePage class, which is used to generate an HTML page for the
glossary of terms and special keys used in the project.
"""

from pathlib import Path

from .html_page import HTMLPage


class ReferencePage(HTMLPage):
    """
    This is a class for generating an HTML page for the glossary of terms and special keys used in
    the project. Presents similar information to the project README file, but will be included in
    the output files.
    """

    def __init__(self, input_directory: Path):
        super().__init__("reference.html.j2")
        self.input_directory = input_directory

    def get_relative_path_to_root(self) -> str:
        return ".."

    def get_path(self) -> Path:
        return Path(self.input_directory) / "reference.html"

    def get_depth(self) -> int:
        return 0
