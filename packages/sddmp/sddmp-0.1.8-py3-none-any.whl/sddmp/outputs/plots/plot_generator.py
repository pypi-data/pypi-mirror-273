"""
This file contains the PlotGenerator class, which is used to generate plots from a dataframe for
use in the HTML page.
"""

import logging

from .pie_plot import PiePlot

logger = logging.getLogger(__name__)


class PlotGenerator:
    """
    Class for generating plots from a dataframe for use in the HTML page.
    """

    def __init__(self, df):
        self.df = df

    def generate_pie_plot(self, column: str) -> PiePlot:
        """
        Generates a pie plot for a column in the dataframe.

        Args:
            df (pd.DataFrame): The dataframe.
            column (str): The name of the column in the dataframe.

        Returns:
            PiePlot: The pie plot.
        """
        # Make a copy of the dataframe
        df = self.df.copy()

        # Create a dataframe that counts the number of files with each extension.
        df = df[column].value_counts().reset_index()

        # Rename the columns.
        df.columns = [column, "count"]

        # Create a pie plot.
        plot = PiePlot(
            title=f"Number of files by {column}".replace("-", " ").title(),
            labels=df[column],
            values=df["count"],
        )

        return plot

    def all_plots(self) -> dict:
        """
        Generates all of the pie plots used in the HTML page.

        returns:
            dict: A dictionary of the pie plots.
        """
        # If we have a 0 length dataframe, return an empty dictionary.
        if len(self.df) == 0:
            return {}

        plots = {}

        # Generate pie plots for the file extensions
        file_extension_counts = self.df["Extension"].value_counts()
        plots["file_extension"] = PiePlot(
            "File Extensions",
            file_extension_counts.index,
            file_extension_counts.values,
            text=[
                f"{count} {extension_name} files"
                for extension_name, count in file_extension_counts.items()
            ],
        )

        size_by_extension = self.df.groupby("Extension")["File Size (bytes)"].sum()
        if len(size_by_extension) > 0:
            text = [
                f"{extension_name}: {size / 1024**2:.2f} MB"
                for extension_name, size in size_by_extension.items()
            ]

            plots["file_size_by_extension"] = PiePlot(
                "File Size by Extension",
                size_by_extension.index,
                size_by_extension.values,
                text=text,
                hovertemplate="%{value} Bytes (%{percent})<extra></extra>",
            )

        size_by_directory = self.df.groupby("Parent Directory")[
            "File Size (bytes)"
        ].sum()
        if len(size_by_directory) > 0:
            text = [
                f"{size / 1024**2:.2f} MB"
                for extension_name, size in size_by_directory.items()
            ]

            plots["file_size_by_directory"] = PiePlot(
                "File Size by Directory",
                size_by_directory.index,
                size_by_directory.values,
                text=text,
            )

        return plots
