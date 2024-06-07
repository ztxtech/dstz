from abc import ABC, abstractmethod
from typing import Hashable


class Item(ABC):
    """
    Abstract base class for items that can be uniquely identified and hashed based on certain attributes.

    Attributes:
        _value (Any): An internal attribute that may be used by subclasses.

    Methods:
        __init__(): Initializes an instance of the Item class with an internal _value attribute set to None.

        idattr (property): An abstract property that must be implemented by subclasses to specify
                           the attribute(s) that uniquely identify an instance of the class.

        __eq__(other: Any) -> bool: Compares this item with another object for equality based on the
                                    values of the attributes specified in the idattr property.

        __hash__() -> int: Computes a hash value for the item based on the values of the attributes
                           specified in the idattr property. Non-hashable values are converted to
                           a frozenset before hashing.
    """

    def __init__(self):
        """
        Initializes an instance of the Item class with an internal _value attribute set to None.
        """
        self._value = None

    @property
    @abstractmethod
    def idattr(self):
        """
        An abstract property that must be implemented by subclasses to specify the attribute(s)
        that uniquely identify an instance of the class.
        """
        pass

    def __eq__(self, other):
        """
        Compares this item with another object for equality based on the values of the attributes
        specified in the idattr property.

        Args:
            other (Any): The object to compare this item against.

        Returns:
            bool: True if the objects are equal, False otherwise.
        """
        if not isinstance(other, type(self)):
            return False
        return all(getattr(self, attr) == getattr(other, attr) for attr in self.idattr)

    def __hash__(self):
        """
        Computes a hash value for the item based on the values of the attributes specified in the
        idattr property. Non-hashable values are converted to a frozenset before hashing.

        Returns:
            int: The computed hash value.
        """
        attrs = []
        for attr in self.idattr:
            value = getattr(self, attr)
            if not isinstance(value, Hashable):
                value = frozenset(value)
            attrs.append(value)
        return hash(tuple(attrs))
