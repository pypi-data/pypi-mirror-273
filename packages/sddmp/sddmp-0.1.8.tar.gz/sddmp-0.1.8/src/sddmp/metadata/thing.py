"""
This file contains the Thing class, which is used to represent a thing with type and content.

A thing is anything that is defined in the schema.org vocabulary. It is represented as a
dictionary, with keys corresponding to the names of the attributes of the thing. Accessing an
attribute of the thing returns the value of the corresponding key in the content dictionary.
"""

from dataclasses import dataclass, field
import logging

logger = logging.getLogger(__name__)


@dataclass
class Thing(dict):
    """
    Represents a thing with type and content.

    Content is stored as a dictionary, with keys corresponding to the names of the attributes of
    the thing. Accessing an attribute of the thing returns the value of the corresponding key in
    the content dictionary.

    Attributes:
        type (str): The type of the thing.
        content (dict): The content of the thing.

    Methods:
        children: Returns a list of child things.
        supplement: Supplements the content of the thing with the content of another thing.
    """

    type: str = field(default="Thing")
    content: dict = field(default_factory=dict)

    def __post_init__(self):
        for key, value in self.content.items():
            setattr(self, key.replace(" ", "_"), value)

    def __getitem__(self, __key):
        if __key == "type":
            return self.type
        return self.content[__key]

    def children(self, recursive=False) -> list["Thing"]:
        """
        Returns a list of child things. If recursive is True, also includes nested children.

        If the content of the thing contains a key with @type, the value of that key is used as the
        type of the child thing. Otherwise, the type of the child thing is set to "Thing".

        Args:
            recursive (bool): Whether to include nested children.

        Returns:
            list[Thing]: A list of child things.
        """
        children = [
            Thing(type=item.get("@type", "Thing"), content=item)
            for value in self.content.values()
            if isinstance(value, list)
            for item in value
        ]

        if recursive:
            for child in children.copy():
                children.extend(child.children(recursive=True))

        return children

    def supplement(self, other: "Thing") -> None:
        """
        Supplements the content of the thing with the content of another thing.

        Will not overwrite existing keys, but will add new keys that do not exist in this thing.
        Will also check all nested children and supplement them recursively.

        Args:
            other (Thing): The other thing.
        """
        logger.debug("Supplementing with other thing: %s", other)

        for key, value in other.content.items():
            if key not in self.content:
                logger.debug("Adding key: %s, value: %s", key, value)
                self.content[key] = value
            elif isinstance(value, list):
                logger.debug("Extending self.content[%s] with %s", key, value)
                self.content[key].extend(value)
            elif isinstance(value, dict):
                for child in self.content[key]:
                    child.supplement(Thing(content=value))
        logger.info("Finished supplementing, self.content is now: %s", self.content)
