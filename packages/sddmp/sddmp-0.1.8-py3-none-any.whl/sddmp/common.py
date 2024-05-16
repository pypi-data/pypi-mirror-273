"""
Provides a common base for parsing command line arguments.
"""

import argparse
import logging


def _common_cli(description: str) -> argparse.ArgumentParser:
    """
    Generate a command line argument parser with common arguments.

    Args:
        description (str): The description to display when the help message is printed.

    Returns:
        argparse.ArgumentParser: The command line argument parser.
    """
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument(
        "-i",
        "--input",
        type=str,
        required=True,
        help="The input directory to create html files for.",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        help="The output directory for the html files.",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Print verbose output.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the output without writing to the file system.",
    )
    parser.add_argument(
        "--clean",
        action="store_true",
        help="Clear the output directory before writing files.",
    )
    return parser


def _logging_setup(verbose):
    if verbose:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)
