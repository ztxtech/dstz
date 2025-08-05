from itertools import combinations

from dstz.core.atom import Element


def simple_space(n):
    """Generates a simple set of elements.

    Creates a set of 'n' unique `Element` objects, where each element's
    value is a consecutive uppercase letter starting from 'A'.

    Args:
        n (int): The number of elements to generate in the space.

    Returns:
        set: A set containing the generated `Element` objects.

    Example:
        >>> simple_space(3)
        {Element('A'), Element('B'), Element('C')}
    """
    return {Element(chr(ord('A') + i)) for i in range(n)}


def powerset(simple_space, allow_empty=False):
    """Generates the power set from a given set of elements.

    The power set is the set of all possible subsets of the input
    `simple_space`. Each subset is wrapped in an `Element` object.

    Args:
        simple_space (set): The input set of elements for which to generate
            the power set.
        allow_empty (bool, optional): If `True`, the empty set will be
            included in the result. Defaults to `False`.

    Returns:
        set: A set of `Element` instances, where each instance contains a
             subset of the input `simple_space`.

    Example:
        >>> s = {Element('A'), Element('B')}
        >>> powerset(s, allow_empty=True)
        {Element(set()), Element({'A'}), Element({'B'}), Element({'A', 'B'})}
    """
    res = []
    start_index = 0 if allow_empty else 1
    for r in range(start_index, len(simple_space) + 1):
        res.extend(combinations(simple_space, r))
    return {Element(set(element)) for element in res}