from dstz.core.atom import Item


class Evidence(dict):
    """A dictionary subclass for storing evidence data.

    `Evidence` enforces type constraints, requiring that all keys be instances
    of the `Item` class and all values be floats. This structure is fundamental
    for representing belief masses in evidence theory.

    It behaves like a standard dictionary but adds validation during
    initialization and item assignment.
    """

    def __init__(self, *args, **kwargs):
        """Initializes the Evidence dictionary.

        This constructor accepts the same arguments as a standard `dict`.
        After initializing, it validates that all keys are instances of `Item`
        and all values are floats.

        Args:
            *args: Variable length argument list, passed to the `dict` constructor.
            **kwargs: Arbitrary keyword arguments, passed to the `dict` constructor.

        Raises:
            TypeError: If any key is not an `Item` instance or any value is not
                a float.
        """
        super(Evidence, self).__init__(*args, **kwargs)
        for key, value in self.items():
            if not isinstance(key, Item):
                raise TypeError('Key must be an instance of Item')
            if not isinstance(value, float):
                raise TypeError('Value must be a float')

    def __setitem__(self, key, value):
        """Sets a key-value pair in the dictionary with type validation.

        Before adding or updating a key-value pair, this method ensures the
        key is an `Item` instance and the value is a float.

        Args:
            key (Item): The key to set, which must be an instance of `Item`.
            value (float): The value to associate with the key.

        Raises:
            TypeError: If the key is not an `Item` instance or the value is
                not a float.
        """
        if not isinstance(key, Item):
            raise TypeError('Key must be an instance of Item')
        if not isinstance(value, float):
            raise TypeError('Value must be a float')
        super(Evidence, self).__setitem__(key, value)

    def __getitem__(self, item):
        """Retrieves an item from the dictionary.

        This method ensures that the key used for retrieval is an instance of
        `Item` before accessing the value.

        Args:
            item (Item): The key whose associated value is to be returned.

        Returns:
            float: The value associated with the given key.

        Raises:
            TypeError: If the key is not an `Item` instance.
        """
        if not isinstance(item, Item):
            raise TypeError('Key must be an instance of Item')
        return super(Evidence, self).__getitem__(item)