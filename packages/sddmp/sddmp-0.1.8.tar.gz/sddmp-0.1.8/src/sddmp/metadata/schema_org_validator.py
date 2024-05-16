"""
This file contains the SchemaOrgValidator class, which is used to validate terms against the
schema.org vocabulary.
"""

import tempfile
import logging
from pathlib import Path
import time

import rdflib
import requests

logger = logging.getLogger(__name__)


class Singleton(type):
    """
    This class is a metaclass for creating singleton classes. It ensures that only one instance of
    the class is created.

    Attributes:
        _instances (dict): A dictionary of instances of the class.

    Methods:
        __call__: Returns the instance of the class if it already exists, otherwise creates a new
            instance and returns it.
    """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            logger.debug("Initializing SchemaOrgValidator object")
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class SchemaOrgValidator(metaclass=Singleton):
    """
    This class is used to validate terms against the schema.org vocabulary.

    Attributes:
        GITHUB_URL (str): The URL of the schema.org file on GitHub.
        SUBDIRECTORY (str): The subdirectory in the cache directory where the schema.org file is
            stored.
        FILE_NAME (str): The name of the schema.org file.

    Properties:
        cache_file_path (Path): The file path of the cache file.
        all_terms (set): A set of all the terms in the schema.org file.

    Methods:
        __init__: Initializes the SchemaOrgValidator object.
        _check_and_download: Checks if the schema.org file exists in the cache directory and
            downloads it if not.
        get_term_details: Returns the details of a term in the schema.org file.
        term_exists: Checks if a given term exists in the graph.
    """

    _instance = None

    GITHUB_URL = (
        "https://github.com/schemaorg/schemaorg/raw/main/data/releases/23.0/"
        "schemaorg-all-http.rdf"
    )
    SUBDIRECTORY = "sddmp"
    FILE_NAME = "schemaorg-all-http.rdf"

    @property
    def cache_file_path(self):
        """
        Returns the file path of the cache file.

        Returns:
            pathlib.Path: The file path of the cache file.
        """
        return self.temp_dir.joinpath(self.SUBDIRECTORY, self.FILE_NAME)

    @property
    def all_terms(self) -> set:
        """
        Gets a set of all the terms in the schema.org file.

        Returns:
            set: A set of all the terms in the schema.org file.
        """
        if self._all_terms is None:
            self._all_terms = set()
            for _, _, object_ in self.g:
                # Only add terms that are not single words and are not part of a URL
                clean_object = str(object_).replace(r"http://schema.org/", "")

                if len(str(clean_object).split(" ")) == 1:
                    self._all_terms.add(str(clean_object))
        return self._all_terms

    def __init__(self, temp_dir: Path = None):
        logger.debug("Initializing SchemaOrgValidator object")
        self.temp_dir = (
            Path(tempfile.gettempdir()) if temp_dir is None else Path(temp_dir)
        )
        self.cache_file_path.parent.mkdir(exist_ok=True)
        self._check_and_download()
        self.g = rdflib.Graph()
        self.g.parse(self.cache_file_path)

        self._all_terms = None
        logger.debug("Initialized SchemaOrgValidator object")
        self._initialized = True

    def _check_and_download(self):
        """
        Checks if the schema.org file exists in the cache directory and downloads it if not.

        Raises:
            requests.exceptions.RequestException: If there is an error while downloading the
            schema.org file.
        """
        if not self.cache_file_path.exists():
            start = time.time()
            logger.info("Downloading schema.org file...")
            try:
                response = requests.get(self.GITHUB_URL, timeout=20)
                response.raise_for_status()
                with open(self.cache_file_path, "wb") as f:
                    f.write(response.content)
                logger.info(
                    "Downloaded schema.org file in %.2f seconds", time.time() - start
                )
            except requests.exceptions.RequestException as err:
                logger.error("Failed to download schema.org file: %s", err)
                raise err

    def get_term_details(self, term: str) -> dict:
        """
        Get the details of a term in the schema.org file.

        Args:
            term (str): The term to get the details of.

        Returns:
            dict: The details of the term in the schema.org file.
        """
        logger.debug("Getting details for term '%s'", term)
        for subject, predicate, object_ in self.g:
            if term in [str(subject), str(predicate), str(object_)]:
                logger.debug("Found details for term '%s'", term)
                return {
                    "subject": subject,
                    "predicate": predicate,
                    "object": object_,
                }
        logger.debug("Did not find details for term '%s'", term)
        return {}

    def term_exists(self, term: str) -> True:
        """
        Checks if a given term exists in the graph.

        Args:
            term (str): The term to check.

        Returns:
            bool: True if the term exists in the graph, False otherwise.
        """
        return term in self.all_terms
