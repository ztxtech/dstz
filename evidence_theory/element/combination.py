from itertools import chain, combinations

from evidence_theory.core.atom import Element


def powerset(simple_space, allow_empty=False):
    """
    Generates a power set of a given set, optionally excluding the empty set.

    Parameters:
    - simple_space (set): The input set to generate the power set from.
    - allow_empty (bool, optional): Determines whether to include the empty set in the result.
                                   Default is False.

    Returns:
    set: A set of Element instances, each representing a subset of the input set.

    Description:
    This function computes the power set of the provided set `simple_space`. The power set consists
    of all possible subsets of `simple_space`, including the empty set and the set itself.
    By default, the empty set is not included in the result unless `allow_empty` is set to True.
    Each subset is encapsulated in an `Element` instance before being added to the result set.
    """
    if isinstance(simple_space, set):
        if allow_empty:
            # Include the empty set in the result
            res = chain.from_iterable(combinations(simple_space, r) for r in range(len(simple_space) + 1))
        else:
            # Exclude the empty set from the result
            res = chain.from_iterable(combinations(simple_space, r) for r in range(1, len(simple_space) + 1))
        # Convert each subset tuple from the combinations to an Element and add to the result set
        return {Element(set(element)) for element in res}


def simple_space(n):
    """
    Generates a set representing a simple space of elements.

    Parameters:
    - n (int): The number of elements in the simple space.

    Returns:
    - set: A set containing 'n' elements, where each element is a character starting from 'A'.
         For example, if n is 3, the returned set will be {'A', 'B', 'C'}.

    Usage Example:
    >>> simple_space(3)
    {'A', 'B', 'C'}
    """
    return {chr(ord('A') + i) for i in range(n)}
