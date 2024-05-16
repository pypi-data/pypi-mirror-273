"""
This Script is used to generate a demo project directory structure for testing the Self Documenting
Data Management Plan (SDDMP) tool. The script takes a directory structure as input and creates
the directories and subdirectories in the output directory. The input can be provided as a text file
or as a string pasted into the terminal. The output directory is created if it does not exist.

The script can be run from the command line using the following command:
```
python -m sddmp.demo -o example_project -i example_structure.txt
```
"""

import logging
from pathlib import Path
import shutil
import sys

from .common import _common_cli, _logging_setup

logger = logging.getLogger(__name__)


def cli():
    """
    Create a CLI for the demo script.
    """

    parser = _common_cli(
        "Create a demonstration project directory structure for testing."
    )
    parser.add_argument(
        "--dry_run",
        action="store_true",
        help="Print the output without writing to the file system.",
    )
    return parser.parse_args()


def create_directory_structure(base_path, structure_string: str, dry_run=False):
    """
    Create a directory structure from a string representation.

    Args:
        base_path (str): The base path to create the directory structure in.
        structure_string (str): A string representation of the directory structure to create.
        dry_run (bool): If True, the directory structure will not be created.

    Returns:
        None
    """
    lines = structure_string.split("\n")
    path_stack = []
    for line in lines:
        if line.strip() == "":
            continue
        depth = line.index(line.lstrip()) // 3
        name = line.lstrip()
        while len(path_stack) > depth:
            path_stack.pop()
        path_stack.append(name)
        path = Path(base_path, *path_stack)
        log_func = logger.info if dry_run else logger.debug
        log_func("Creating %s", path)
        if not dry_run:
            path.mkdir(parents=True, exist_ok=True)


def get_structure(file_path: str) -> str:
    """
    Get the structure from the user.

    Args:
        file_path (str): The path to the file to load the directory structure from.

    Returns:
        str: The directory structure as a string.
    """
    if file_path:
        with open(file_path, encoding="utf-8") as f:
            return f.read()
    else:
        print(
            "Please paste a directory structure into the terminal here (Press Enter to finish):"
        )
        user_input = ""
        while True:
            text = input()
            if text == "":
                break
            user_input += text + "\n"
        return user_input


if __name__ == "__main__":
    args = cli()

    # Set up logging.
    _logging_setup(args.verbose)

    print(f"Creating example project at {args.output}")

    structure = get_structure(args.input)

    # Let the user see the structure that will be created.
    print("The following directory structure will be created:")
    print(structure)
    if input("Is this correct? (y/n): ").lower() != "y":
        print("Exiting.")
        sys.exit()

    create_directory_structure(args.output, structure, args.dry_run)

    if not args.dry_run:
        # Drop a copy of the example README in the output directory.
        readme = Path(__file__).parent / "resources/README_example.yaml"
        readme_path = Path(args.output, "README.yaml")
        shutil.copy(readme, readme_path)

    print("Done!")
