"""
This file contains the DirectoryPage class, which is used to generate an HTML page for a directory
in the file system.
"""

from pathlib import Path

from ..filesystem import Directory
from .html_page import HTMLPage
from .plots.plot_generator import PlotGenerator
from ..util.file_operations import FileOperations


class DirectoryPage(HTMLPage):
    """
    Represents an HTML page for a directory in the file system.

    Attributes:
        directory (Directory): The directory for which the HTML page is to be generated.
        output_directory (Path): The directory in which the HTML page is to be saved.

    Methods:
        generate: Generates the HTML page for the directory.
        generate_pie_plot: Generates a pie plot for a column in the dataframe.
    """

    def __init__(self, directory: Directory):
        super().__init__("directory.html.j2")
        self.directory = directory

    def get_relative_path_to_root(self) -> str:
        """
        Returns the relative path from the output directory to the root directory.
        """
        num_path_parts = self.directory.path_depth + 1
        if num_path_parts == 1:
            return ".."

        return "../" * (num_path_parts)

    def get_path(self) -> Path:
        """
        Returns the path to the HTML file.
        """
        return self.directory.path / "index.html"

    def get_depth(self) -> int:
        """
        Returns the depth of the page in the directory structure.
        """
        return len(self.directory.path.parts)

    def generate(self, operations: FileOperations, **kwargs) -> None:
        """
        Generates the HTML page for the directory and saves it in the output directory.
        """
        file_records_df = self.directory.file_records_dataframe()

        plot_generator = PlotGenerator(file_records_df)

        # Render the template with the dataframe.
        super().generate(
            operations=operations,
            project_title=self.directory.metadata["ResearchProject"]["name"],
            my_path=self.directory.path.as_posix(),
            num_files=len(file_records_df),
            num_excluded_files=self.directory.num_excluded_files,
            num_directories=len(self.directory.self_and_descendants) + 1,
            people=self.directory.metadata.get_people(),
            filetree=self.directory.filetree,
            plots={
                name: plot.as_json()
                for name, plot in plot_generator.all_plots().items()
            },
            metadata=self.directory.metadata_as_plaintext(),
            file_records_df=file_records_df,
            **kwargs,
        )
