# Self Documenting Data Management Plan

|         |                                                                                                                                                                                                                                                                                                                                 |
| ------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Build   | [![pipeline status](https://git.rwth-aachen.de/dl/productivity-tools/self-documenting-data-management-plan/badges/main/pipeline.svg)](https://git.rwth-aachen.de/dl/productivity-tools/self-documenting-data-management-plan/-/commits/main)                                                                                    |
| Release | [![RWTH Release](https://git.rwth-aachen.de/dl/productivity-tools/self-documenting-data-management-plan/-/badges/release.svg?key_text=RWTH%20GitLab)](https://git.rwth-aachen.de/dl/productivity-tools/self-documenting-data-management-plan/-/releases) ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/sddmp) |
| Package | [![PyPI Release](https://img.shields.io/pypi/v/sddmp.svg)](https://pypi.org/project/sddmp/)                                                                                                                                                                                                                                     |

- [Self Documenting Data Management Plan](#self-documenting-data-management-plan)
  - [Installation](#installation)
  - [Usage](#usage)
  - [Setup](#setup)
    - [Special Keys](#special-keys)
      - [Include / Exclude / Redact files from a report](#include--exclude--redact-files-from-a-report)
      - [People](#people)
  - [Output](#output)
  - [Demonstration](#demonstration)

## Installation

This package is available on PyPI and can be installed with the following command:

```bash
pip install sddmp
```

If you encounter any issues during the installation, please check the Python documentation on
installing packages.

## Usage

The package includes a script that will generate a simple html report from a directory structure.
To use this script, run the following command:

`python -m sddmp.generate --input "example_project" --output "docs"`

`--output`  is optional. By default, it will create a directory called "docs" in the current
working directory.

## Setup

We expect a directory that contains one or more sub-directories, and one or more files. In the
root directory, place a file called "README.yaml" that contains any common metadata that should
apply to all files in the directory in yaml format.

**The README files are expected to comply with the structures dictated on
[Schema.org](https://schema.org/).**

Example:

```yaml
DigitalDocument:
  name: Self Documenting Data Management Plan
  maintainer:
    - name: <name1>
      email: <email1>
      description: |
        "Responsible for the content and maintenance of the automated data management plan"

ResearchProject:
  name: <title>
  member:
    - name: <name1>
      email: <email1>
      jobTitle: Principal Investigator
    - name: <name2>
      email: <email2>
      jobTitle: Maintainer
  description: "Root folder for Example Project"

Dataset:
  description: |
    This is the readme for the example project and this is the abstract for the dataset.
  conditionsOfAccess: "public"
  license: "CC-BY-4.0"
  version: "1.0"
```

In any subfolder, we can place another file that contains any subset of this information.

Example:

in example_project/20-29 Communication/20 Internal we place a README.yaml that looks like this:
```yaml
Dataset:
  description: This folder contains internal documents.
  conditionsOfAccess: "private"
  maintainer:
    - name: <name3>
      email: <email3>
      description: "Responsible for curating internal documents"
```

When determining metadata for files in this folder, it inherits all of the metadata from the root
file above, adds a new one ("maintainer") and replaces the content of the others ("description"
and "conditionsOfAccess").

### Special Keys

Some keys have special status, and including them will have an effect on the creation of the
report

#### Include / Exclude / Redact files from a report

Including the following under the "Dataset" key in a README will adjust if/how files are included
in the final report:

```
Dataset:
  potentialAction:
    - name: "exclude"
```

- `exclude`: Files in this directory will not be included in the report.
- `redact`: Files will be included, but filenames will be obscured.
- `include`: Files will be included in the report (default).

#### People

When we see one of the following keys, we will check to see if there are additional attributes
for each entry that might indicate that it is a person:
- member
- maintainer
- creator
- contributor
- editor
- reviewer

If we have at least a name, a Card with that person's information will be included on the report.

Example:

```
Dataset:
  maintainer:
    - name: <name1>
      email: <email1>
      jobTitle: Dataset Maintainer
      description: "Responsible for the content and maintenance of the automated data management plan"
```

## Output

The included script will scan the indicated input directory and create a collection of simple html
pages in the output directory. The root page will be an index that links to every other page that
was created. Each page contains a table with metadata for that directory and all directories that
are children of that one.

## Demonstration

A script is included in the package that will generate a sample directory structure on your local
hard drive that you can use to experiment with this concept. To run this script, after installing
the project via pip as indicated above, run `python -m sddmp.demo {arguments}`

*This demonstration script is intended to work with the directory structure format from
[this](https://johnny-decimal-generator.netlify.app/) Johnny.Decimal index generator.*

The command line options for this script are as follows:

- `-o` or `--output`: This option allows you to specify the output directory where the
demonstration mproject will be created. The default value is example_project. For example:
```
python -m sddmp.demo -o my_project
```

- `-i` or `--input`: This option allows you to provide a text file containing a directory structure to
build the demonstration project from. For example:
```
python -m sddmp.demo -i my_directory_structure.txt
```
**The format of the `--input` file is expected to be the output of
[this](https://johnny-decimal-generator.netlify.app/) Johnny.Decimal index generator.**

- `-v` or `--verbose`: This option enables verbose output. When this option is provided, the script
will print detailed output to the console.

- `--dry_run`: This option enables a dry run of the script. When this option is provided, the script
will print the output without actually writing to the file system.

If no file is provided, the option to paste a generated index into the console will be provided.

An example of this input would look like this:
```
10-19 Administration
   11 Meetings
      11.01 Bi-Weekly Jour Fixe Meeting Minutes
      11.02 Weekly AP3&4 Meeting Minutes
   12 Reports
      12.01 Report Due Dates
      12.02 Project Design Report
20-29 Communication
   21 Internal
      21.01 Project Directory
   22 External
```

Note that each level of the directory tree is indicated with a multiple of three spaces.
