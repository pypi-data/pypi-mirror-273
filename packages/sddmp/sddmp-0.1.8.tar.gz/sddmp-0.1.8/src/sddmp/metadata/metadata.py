"""
This file contains the Metadata class, which is used to represent metadata for a file or directory.
"""

import yaml

from .thing import Thing
from .person import Person, find_people_in_dict

# from .schema_org_validator import SchemaOrgValidator


def all_keys(d) -> list[str]:
    """
    Iterates over all keys in the provided dictionary, including nested keys.

    Args:
        d (dict): The dictionary to iterate over.

    Returns:
        list[str]: A list of all keys in the dictionary.
    """
    keys = []
    for key, value in d.items():
        keys.append(key)
        if isinstance(value, dict):
            keys.extend(all_keys(value))
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    keys.extend(all_keys(item))
    return list(set(keys))


def dict_supplement(dict1, dict2) -> dict:
    """
    Supplements the content of dict1 with the content of dict2.

    Includes nested dictionaries, lists and values recursively.

    Args:
        dict1 (dict): The dictionary to supplement.
        dict2 (dict): The dictionary to supplement with.

    Returns:
        dict: The supplemented dictionary.
    """
    for key, value in dict2.items():
        if key not in dict1:
            dict1[key] = value
        elif isinstance(dict1[key], dict) and isinstance(value, dict):
            dict1[key] = dict_supplement(dict1[key], value)
    return dict1


class Metadata(dict):
    """
    A class for representing metadata for a file or directory.

    Class Methods:
        load: Loads metadata from a file.

    Properties:
        flat: A flattened version of the metadata.

    Methods:
        supplement: Supplements the content of the metadata with the content of another metadata
            object.
        get_base_objects: Returns a list of Thing objects representing the base objects in the
            metadata.
        all_keys: Iterates over all keys in the metadata object, including nested keys.
        validate_keys: Validates the keys in the metadata object against the schema.org vocabulary.
        flatten: Flattens the metadata object into a dictionary.
    """

    @property
    def flat(self) -> dict:
        """
        Get a flattened version of the metadata.

        Returns:
            dict: The flattened metadata.
        """
        if self._flat_metadata is None:
            self._flat_metadata = self.flatten()
        return self._flat_metadata

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.schema_org_validator = None  # SchemaOrgValidator()
        self._flat_metadata = None

    def __getattr__(self, item):
        try:
            return self[item]
        except KeyError:
            return None

    @classmethod
    def load(cls, file_path: str) -> "Metadata":
        """
        Load metadata from a file.

        Args:
            file_path (str): The file path of the metadata file.

        Returns:
            Metadata: The metadata object.
        """
        with open(file_path, "r", encoding="utf-8") as file:
            data = yaml.safe_load(file)
            return cls(data)

    @property
    def is_valid(self) -> bool:
        """
        Determines whether the metadata is valid based on the schema.org vocabulary.

        Returns:
            bool: True if the metadata is valid, otherwise False.
        """
        return all(value["valid"] for value in self.validate_keys().values())

    def supplement(self, other: "Metadata") -> None:
        """
        Supplements the content of the metadata with the content of another metadata object.

        Args:
            other (Metadata): The metadata object to supplement with.

        Returns:
            None
        """
        self.update(dict_supplement(self, other))

    def get_base_objects(self) -> list[Thing]:
        """
        Get a list of Thing objects representing the base objects in the metadata.

        Returns:
            list[Thing]: A list of Thing objects representing the base objects in the metadata.
        """

        objects = []
        for key, value in self.items():
            objects.append(Thing(type=key, content=value))
        return objects

    def get_people(self) -> list[Person]:
        """
        Get a list of Person objects found in the metadata.

        Returns:
            list[Person]: A list of Person objects found in the metadata.
        """
        return find_people_in_dict(self)

    def all_keys(self) -> list[str]:
        """
        Iterates over all keys in the metadata object, including nested keys.

        Returns:
            list[str]: A list of all keys in the metadata object.
        """
        # Initialize an empty list to store the keys
        return all_keys(self)

    def validate_keys(self) -> dict[str, bool]:
        """
        Validates the keys in the metadata object against the schema.org vocabulary.

        Returns:
            dict[str, bool]: A dictionary of keys and their validation status.
        """
        return {
            key: {
                **{"valid": self.schema_org_validator.term_exists(key)},
                **self.schema_org_validator.get_term_details(key),
            }
            for key in self.all_keys()
        }

    def flatten(self, parent_key="", sep="_") -> dict:
        """
        Flatten the metadata object into a dictionary.

        Args:
            parent_key (str): The parent key to use when flattening nested dictionaries.
            sep (str): The separator to use when concatenating keys.

        Returns:
            dict: The flattened metadata.
        """
        # Create an empty list to store the flattened key-value pairs
        items = []

        # Iterate over each key-value pair in the Metadata object
        for key, value in self.items():
            # Create a new key by concatenating the parent key and the current key, separated by
            # the provided separator
            new_key = f"{parent_key}{sep}{key}" if parent_key else key

            # If the value is a dictionary, recursively call this method on the value
            if isinstance(value, dict):
                items.extend(
                    Metadata(value).flatten(parent_key=new_key, sep=sep).items()
                )

            # If the value is a list of dictionaries, iterate over each element and recursively
            # call this method on each element
            elif isinstance(value, list) and all(isinstance(i, dict) for i in value):
                for i, elem in enumerate(value):
                    items.extend(
                        Metadata(elem)
                        .flatten(parent_key=f"{new_key}{sep}{i}", sep=sep)
                        .items()
                    )

            # If the value is neither a dictionary nor a list of dictionaries, add the key-value
            # pair to the items list
            else:
                items.append((new_key, value))

        # Convert the list of key-value pairs to a dictionary and return it
        return dict(items)
