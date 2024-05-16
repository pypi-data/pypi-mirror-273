"""
This file contains the Palette class, which is used to define the color palette used in the plots.
"""

from enum import Enum


class Palette(Enum):
    """
    Represents the color palette used in the plots.
    """

    COSCINE_BLACK = "#212529"
    COSCINE_GREY = "#646567"
    COSCINE_WHITE = "#ffffff"
    COSCINE_DARK_BLUE = "#00549F"
    COSCINE_LIGHT_BLUE = "#8EBAE6"
    COSCINE_LIGHT_BLUE2 = "#e8f1fa"

    def __str__(self):
        return self.value
