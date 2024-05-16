"""
This file contains the BasePlot class, which is the base class for all the plots in the package.
"""

import json

import plotly

from .palette import Palette


class BasePlot:
    """
    The BasePlot class is the base class for all the plots in the package. It contains the basic
    attributes and methods that are common to all the plots.

    Attributes:
        title (str): The title of the plot.
        title_font (dict): The font of the title of the plot.
            (default: {"family": "Arial", "size": 24})
        xaxis_title (str): The title of the x-axis of the plot. (default: None)
        yaxis_title (str): The title of the y-axis of the plot. (default: None)

    Properties:
        plot_bgcolor (str): The background color of the plot.
            (default: Palette.COSCINE_LIGHT_BLUE2)
        paper_bgcolor (str): The background color of the paper.
            (default: Palette.COSCINE_WHITE)

    Methods:
        get: Returns the plot as a plotly.graph_objects.Figure object.
        as_json: Returns the plot as a dictionary that can be written to a JSON file.
    """

    def __init__(
        self,
        title: str,
        title_font: dict = None,
        xaxis_title: str = None,
        yaxis_title: str = None,
    ):
        self._figure = plotly.graph_objects.Figure()
        self.title = title

        self.title_font = title_font
        if self.title_font is None:
            self.title_font = {"family": "Arial", "size": 24}

        self.xaxis_title = xaxis_title
        self.yaxis_title = yaxis_title
        self.plot_bgcolor = str(Palette.COSCINE_LIGHT_BLUE2)
        self.paper_bgcolor = str(Palette.COSCINE_WHITE)

    def get(self) -> plotly.graph_objects.Figure:
        """
        Get the plot as a plotly.graph_objects.Figure object.

        Returns:
            plotly.graph_objects.Figure: The plot as a plotly.graph_objects.Figure object.
        """
        return self._figure.update_layout(
            title=self.title,
            title_font=self.title_font,
            xaxis_title=self.xaxis_title,
            yaxis_title=self.yaxis_title,
            plot_bgcolor=self.plot_bgcolor,
            paper_bgcolor=self.paper_bgcolor,
        )

    def as_json(self) -> dict:
        """
        Get the plot as a dictionary that can be written to a JSON file.

        Returns:
            dict: The plot as a dictionary that can be written to a JSON file.
        """
        return json.dumps(self.get(), cls=plotly.utils.PlotlyJSONEncoder)
