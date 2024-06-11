from itertools import combinations

from evidence_theory.core.atom import Element


def simple_space(n):
    """
    Generates a set representing a simple space of elements.

    Args:
    - n (int): The number of elements in the simple space.

    Returns:
    - set: A set containing 'n' unique elements, each identified by a consecutive uppercase letter starting from 'A'.
         For instance, if n equals 3, the returned set is {'A', 'B', 'C'}.

    Usage Example:
    >>> simple_space(3)
    {'A', 'B', 'C'}
    """
    return {Element(chr(ord('A') + i)) for i in range(n)}


def powerset(simple_space, allow_empty=False):
    """
    Generates the power set of a given simple space.

    Args:
    - simple_space (set): The input set for which to generate the power set.
    - allow_empty (bool, optional): A flag indicating whether to include the empty set in the power set.
                                  Defaults to False.

    Returns:
    - set: A set of Element instances, each representing a subset of the input simple space.
           The subsets are unordered collections and may include the empty set based on the `allow_empty` parameter.
           Each subset is wrapped within an Element object to potentially carry additional semantic meaning or methods.

    Description:
    This function computes the power set of the provided `simple_space`, which is the set of all possible subsets
    of `simple_space`. If `allow_empty` is True, the power set includes the empty set as well.
    The resulting subsets are encapsulated within Element objects, which could be utilized for further operations
    in the context of evidence theory or other applications where such encapsulation is beneficial.

    Example Usage:
    >>> s = simple_space(3)
    >>> powerset(s, allow_empty=True)
    {Element(set()), Element({'A'}), Element({'B'}), Element({'C'}), Element({'A', 'B'}), ...}
    """
    res = []
    start_index = 0 if allow_empty else 1
    for r in range(start_index, len(simple_space) + 1):
        res.extend(combinations(simple_space, r))
    return {Element(set(element)) for element in res}
