# pylint: disable=too-many-arguments

"""
This file contains the PiePlot class, which is used to create a pie plot using the Plotly library.
"""

import plotly.graph_objects as go

from .base_plot import BasePlot


class PiePlot(BasePlot):
    """
    Represents a pie plot using the Plotly library.

    Attributes:
        title (str): The title of the plot.
        labels (list[str]): The labels of the pie plot.
        values (list[float]): The values of the pie plot.

    Methods:
        get: Get the pie plot as a Plotly graph object figure.
    """

    def __init__(
        self,
        title,
        labels,
        values,
        text=None,
        hovertemplate="%{label}: %{value} (%{percent})<extra></extra>",
    ):
        super().__init__(title=title)
        self.labels = labels
        self.values = values
        self.text = text
        self.hovertemplate = (
            hovertemplate if text is None else hovertemplate + "<br>%{text}"
        )

    def get(self) -> go.Figure:
        fig = (
            super()
            .get()
            .add_trace(
                go.Pie(
                    labels=self.labels,
                    values=self.values,
                    text=self.text,
                    hovertemplate=self.hovertemplate,
                )
            )
        )
        fig.update_traces(textposition="inside")
        fig.update_layout(uniformtext_minsize=12, uniformtext_mode="hide")
        return fig
