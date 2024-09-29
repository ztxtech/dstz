from dst.core.atom import Item


class Evidence(dict):
    """
    A subclass of dict designed to store evidence data where keys are instances of the Item class,
    and values are floats representing the strength or relevance of the evidence.

    Methods:
        - __init__(\*args, \*\*kwargs): Initializes the Evidence dictionary, validating that keys are
                                   instances of Item and values are floats.

        - __setitem__(key, value): Sets an item in the dictionary, validating that the key is an
                                 instance of Item and the value is a float.

        - __getitem__(item): Retrieves an item from the dictionary, ensuring that the key is an
                           instance of Item.
    """

    def __init__(self, *args, **kwargs):
        """
        Initializes the Evidence dictionary, validating that keys are instances of Item and values
        are floats.

        Raises:
            TypeError: If any key is not an instance of Item or any value is not a float.
        """
        super(Evidence, self).__init__(*args, **kwargs)
        for key, value in self.items():
            if not isinstance(key, Item):
                raise TypeError('Key must be an instance of Item')
            if not isinstance(value, float):
                raise TypeError('Value must be a float')

    def __setitem__(self, key, value):
        """
        Sets an item in the dictionary, validating that the key is an instance of Item and the
        value is a float.

        Args:
            - key: The key to set in the dictionary.
            - value: The value to associate with the key.

        Raises:
            TypeError: If the key is not an instance of Item or the value is not a float.
        """
        if not isinstance(key, Item):
            raise TypeError('Key must be an instance of Item')
        if not isinstance(value, float):
            raise TypeError('Value must be a float')
        super(Evidence, self).__setitem__(key, value)

    def __getitem__(self, item):
        """
        Retrieves an item from the dictionary, ensuring that the key is an instance of Item.

        Args:
            - item: The key whose associated value is to be returned.

        Returns:
            float: The value associated with the given key.

        Raises:
            TypeError: If the key is not an instance of Item.
        """
        if not isinstance(item, Item):
            raise TypeError('Key must be an instance of Item')
        return super(Evidence, self).__getitem__(item)
