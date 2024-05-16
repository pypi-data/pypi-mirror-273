"""
This file contains the Person class, which is used to represent a person from the metadata.
"""

from dataclasses import dataclass, field
import logging


logger = logging.getLogger(__name__)

PERSON_KEYS = ["member", "maintainer", "creator", "contributor", "editor", "reviewer"]


def find_people_in_dict(d: dict) -> list["Person"]:
    """
    Given a dictionary, find all people in the dictionary and return them as a list of Person
    objects.

    Args:
        d (dict): The dictionary to search for people in.

    Returns:
        list[Person]: A list of Person objects found in the dictionary.
    """

    def _create_person(person_dict: dict) -> "Person":
        # remove the @type key if it exists
        person_dict.pop("@type", None)

        try:
            return Person(**person_dict)
        except TypeError as e:
            logger.debug("Could not create person from dictionary: %s", e)
            return None

    people = []
    for key, value in d.items():
        if isinstance(key, str) and key.lower() in PERSON_KEYS:
            if isinstance(value, list):
                for person in value:
                    if isinstance(person, dict):
                        people.append(_create_person(person))
            elif isinstance(value, dict):
                if isinstance(person, dict):
                    people.append(_create_person(person))

        if isinstance(value, dict):
            people.extend(find_people_in_dict(value))

        if isinstance(value, list):
            for item in value:
                people.extend(find_people_in_dict(item))

    return [person for person in people if person is not None]


@dataclass
class Person:
    """
    A Dataclass for representing a person from the metadata.
    """

    # We are ignoring the C103 rule for the following fields because these names are taken
    # from the schema.org Person class, and we want to keep the same names for consistency.

    name: str = field(default=None)
    givenName: str = field(default=None)  # pylint: disable=invalid-name
    familyName: str = field(default=None)  # pylint: disable=invalid-name
    email: str = field(default=None)
    jobTitle: str = field(default=None)  # pylint: disable=invalid-name
    description: str = field(default=None, repr=False)
    memberOf: str = field(default=None, repr=False)  # pylint: disable=invalid-name

    @property
    def full_name(self) -> str:
        """
        Return the full name of the person.

        If the name is set, it will be returned. If not, the givenName and familyName will be
        combined to form the full name. If neither the name nor the givenName and familyName are
        set, None will be returned.
        """
        if self.name:
            return self.name

        if self.givenName or self.familyName:
            return f"{self.givenName} {self.familyName}"

        return None

    def as_dict(self) -> dict:
        """
        Return a dictionary representation of the person.
        """
        return_dict = {"Name": self.full_name}
        if self.email:
            return_dict["Email"] = self.email
        if self.jobTitle:
            return_dict["Job Title"] = self.jobTitle
        if self.description:
            return_dict["Description"] = self.description
        if self.memberOf:
            return_dict["Member Of"] = self.memberOf
        return return_dict
