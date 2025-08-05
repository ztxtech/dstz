from abc import ABC, abstractmethod
from typing import Hashable

class Item(ABC):
    """Abstract base class for items that can be uniquely identified and hashed.

    This class provides a foundation for creating objects that need to be
    distinguishable based on specific attributes. Subclasses are required to
    implement the `idattr` property, which specifies which attributes are used
    for identification, equality checks, and hashing.

    Attributes:
        _value (Any): An internal attribute for use by subclasses.
    """

    def __init__(self):
        """Initializes the Item instance.

        Sets the internal `_value` attribute to `None`.
        """
        self._value = None

    @property
    @abstractmethod
    def idattr(self):
        """Specifies the unique identifying attributes for an instance.

        This abstract property must be implemented by any subclass. It should
        return a list or tuple of strings, where each string is the name of an

        attribute that uniquely identifies the object.

        Returns:
            A list or tuple of attribute names.
        """
        pass

    def __eq__(self, other):
        """Compares this item with another for equality.

        Two items are considered equal if they are of the same type and the
        values of their identifying attributes (specified by `idattr`) are
        all equal.

        Args:
            other (Any): The object to compare against.

        Returns:
            bool: `True` if the objects are equal, `False` otherwise.
        """
        if not isinstance(other, type(self)):
            return False
        return all(getattr(self, attr) == getattr(other, attr) for attr in self.idattr)

    def __hash__(self):
        """Computes a hash value for the item.

        The hash is based on the values of the identifying attributes
        (specified by `idattr`). If an attribute's value is not hashable
        (e.g., a list or set), it is converted to a `frozenset` before hashing.

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


class Element(Item):
    """A concrete class representing a basic element with a specific value.

    This class inherits from `Item` and is used to wrap a single value. The
    identity of an `Element` is determined solely by its `value` attribute.

    Attributes:
        value (Any): The value of the element.
    """

    def __init__(self, value=None):
        """Initializes an Element instance.

        Args:
            value (Any, optional): The initial value of the Element.
                Defaults to `None`.
        """
        super(Element, self).__init__()
        self.value = value

    @property
    def idattr(self):
        """Specifies the identifier attribute for the Element.

        Returns:
            list: A list containing the name of the identifier attribute, `['value']`.
        """
        return ['value']

    def __str__(self):
        """Returns a human-readable string representation of the Element.

        Returns:
            str: The string representation of the Element's value.
        """
        return str(self.value)

    def __repr__(self):
        """Returns a developer-friendly string representation of the Element.

        Returns:
            str: The string representation of the Element's value, suitable
                 for debugging.
        """
        return self.__str__()

    def __len__(self):
        """Returns the length of the Element's value.

        This method allows the `len()` function to be called on an `Element`
        instance, provided its `value` has a defined length (e.g., a list,
        tuple, or string).

        Returns:
            int: The length of the `value` attribute.
        """
        return len(self.value)

    def __iter__(self):
        """Makes the Element iterable.

        If the Element's `value` is iterable (and not a string), this method
        yields its items one by one. This allows iterating directly over an
        `Element` instance.

        Yields:
            Any: The next item from the `value` attribute.
        """
        if hasattr(self.value, '__iter__') and not isinstance(self.value, str):
            yield from self.value