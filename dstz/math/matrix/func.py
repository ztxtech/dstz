def get_ones_indices(n):
    """Gets the indices of set bits in the binary representation of an integer.

    This function is used to map an integer to a subset. In the context of
    this library, if a Frame of Discernment has N elements, any integer from
    0 to 2^N - 1 can represent a subset. The indices of the '1's in the
    integer's binary form correspond to the indices of the elements in the
    subset.

    Args:
        n (int): A non-negative integer.

    Returns:
        list: A list of indices where the bits are set to 1.

    Example:
        >>> get_ones_indices(5)  # Binary of 5 is 101
        [0, 2]
        >>> get_ones_indices(10) # Binary of 10 is 1010
        [1, 3]
    """
    indices = []
    index = 0
    while n:
        if n & 1:
            indices.append(index)
        n >>= 1
        index += 1
    return indices