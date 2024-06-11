from itertools import combinations, permutations

from evidence_theory.core.atom import Element


def permutation_set(simple_space, allow_empty=False):
    """
    Generates all permutations of all possible non-empty subsets from a given simple space.

    Args:
    - simple_space (set): The input set from which permutations of subsets are generated.
    - allow_empty (bool, optional): Determines whether to include permutations of the empty set in the result.
                                  Defaults to False.

    Returns:
    - set: A set of Element instances, each wrapping a tuple that represents a unique permutation of a subset.
           The subsets range from single elements up to the full set, and each subset's permutations are sorted.
           If `allow_empty` is True, the set will also contain a permutation of the empty set.

    Description:
    This function computes all permutations for every non-empty subset within the provided `simple_space`.
    It starts by generating combinations of elements for varying lengths, from 1 up to the size of `simple_space`,
    and then calculates all possible permutations for these combinations. The permutations are sorted to maintain consistency.
    Each permutation is then encapsulated in an Element object, which might be used for further computations or
    to imbue additional meaning in an application context, such as evidence theory.

    Example Usage:
    >>> s = simple_space(3)
    >>> permutation_set(s, allow_empty=False)
    {Element(('A',)), Element(('B',)), Element(('C',)), Element(('A', 'B')), ...}
    """
    res = []
    start_index = 0 if allow_empty else 1
    for r in range(start_index, len(simple_space) + 1):
        for subset in combinations(simple_space, r):
            res.extend(permutations(subset))
    return {Element(element) for element in res}
