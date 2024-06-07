from evidence.core.atom import Item
from evidence.core.distribution import Evidence
from evidence.evipiece.dual import ds_rule


# Define a new class Element inheriting from Item
class Element(Item):
    """
    A class representing an element with a specific value.

    Attributes:
        value (Any): The value of the element.

    Methods:
        __init__(self, value=None): Constructor for the Element class.
        idattr (property): Property specifying the identifier attribute of the Element.
        __str__(self): Returns a string representation of the Element.
        __repr__(self): Returns a string representation of the Element.
    """

    def __init__(self, value=None):
        """
        Initialize an Element instance with a given value.

        Args:
            value (Any, optional): The initial value of the Element. Defaults to None.
        """
        super(Element, self).__init__()
        self.value = value

    @property
    def idattr(self):
        """
        Property specifying the identifier attribute of the Element.

        Returns:
            list: A list containing the name of the identifier attribute ('value').
        """
        return ['value']

    def __str__(self):
        """
        Return a string representation of the Element.

        Returns:
            str: String representation of the Element's value.
        """
        return str(self.value)

    def __repr__(self):
        """
        Return a string representation of the Element suitable for debugging.

        Returns:
            str: String representation of the Element's value.
        """
        return self.__str__()


# Create an instance of Evidence with some predefined elements and their masses
e1 = Evidence()
e1[Element({'A'})] = 0.99
e1[Element({'B'})] = 0.01

# Create another instance of Evidence with some predefined elements and their masses
e2 = Evidence()
e2[Element({'C'})] = 0.99
e2[Element({'B'})] = 0.01

# Apply the Dempster-Shafer rule of combination on e1 and e2
e = ds_rule(e1, e2, Element)

# Print the resulting combined evidence
print(e)
