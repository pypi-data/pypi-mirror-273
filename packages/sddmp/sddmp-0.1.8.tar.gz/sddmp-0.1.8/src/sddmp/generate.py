"""
This file is used to create static html files for displaying in GitHub Pages.

Usage:
    python create_html_files.py -i data -o docs
"""

import shutil

from importlib import resources
import logging
from pathlib import Path
import re
import sys

from sddmp.filesystem import FileSystem
from sddmp.outputs import DirectoryPage, ReferencePage
from sddmp.util.file_operations import FileOperations

from .common import _common_cli, _logging_setup
from .config import load_config

logger = logging.getLogger(__name__)


def cli():
    """
    Create a CLI for the generate script.
    """
    parser = _common_cli("Create static html files for displaying in GitHub Pages.")
    parser.add_argument(
        "--source_prefix",
        default="",
        help="The prefix to add to the source path when loading the static files",
    )
    return parser.parse_args()


def clear_output_directory(file_operations, output):
    """
    Clear the output directory of a previous run of this script.

    Args:
        file_operations (FileOperations):
            The file operations object to use for deleting the files.
        output (str):
            The output directory to clear.
    """

    created_files = [
        ".*index.html$",
        rf"^{output}\\.*\\reference.html$",
        rf"^{output}\\static\\js\\jquery-ui.min.js$",
        rf"^{output}\\static\\js\\script.js$",
        rf"^{output}\\static\\styles\\custom.css$",
        rf"^{output}\\static\\styles\\styles.css$",
    ]

    for path in Path(output).rglob("*"):
        if path.is_file():
            if any(re.match(pattern, str(path)) for pattern in created_files):
                file_operations.register_deleted_file(path)
            else:
                logger.error(
                    (
                        "File %s was not created by a previous run of this script. "
                        "Please check that the output directory does not contain any "
                        "files not created by this script."
                    ),
                    path,
                )
                sys.exit(1)
        elif path.is_dir():
            file_operations.register_deleted_directory(path)


def move_static_files(file_operations, output):
    """
    Move Static files from the sddmp package to the output directory.

    Args:
        file_operations (FileOperations):
            The file operations object to use for moving the static files.
        output (str):
            The output directory to move the static files to.
    """
    source_dir = resources.files("sddmp") / "outputs/static"
    logger.info("Copying static files from %s to %s/static", source_dir, output)

    # Iterate over all of the files in the static folder and add them to the operations
    for file in source_dir.rglob("*"):
        if file.is_file():
            with open(file, "rb") as source:
                target_path = Path("static") / file.relative_to(source_dir)
                with file_operations.new_file(target_path, "wb") as f:
                    shutil.copyfileobj(source, f)


if __name__ == "__main__":
    args = cli()

    # Set up logging.
    _logging_setup(args.verbose)

    config = load_config()
    if args.output:
        config.set_output_directory(args.output)

    operations = FileOperations(
        dry_run=args.dry_run, target_directory=config.output_directory
    )
    if args.clean:
        clear_output_directory(operations, config.output_directory)

    fs = FileSystem(config)
    root = fs.read_directory(args.input)

    DirectoryPage.directory_structure = fs.get_directory_structure(root)["children"]
    ReferencePage.directory_structure = fs.get_directory_structure(root)["children"]

    # Delete the output directory if it exists.

    # Move the static directory to the output directory.
    move_static_files(operations, output=config.output_directory)

    # Create a reference page
    reference = ReferencePage(args.input)
    reference.generate(operations)

    # Start with the root and iterate recursively through all directories.
    # For each directory, create an html file.
    for directory in root.self_and_descendants:
        page = DirectoryPage(directory)
        page.generate(operations)

    operations.execute()
