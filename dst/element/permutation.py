import itertools
from itertools import combinations, permutations

from dst.core.atom import Element


def permutation_set(simple_space, allow_empty=False):
    """
    Generates all permutations of all possible non-empty subsets from a given simple space.

    Args:
        - simple_space (set): The input set from which permutations of subsets are generated.
        - allow_empty (bool, optional): Determines whether to include permutations of the empty set in the result. Defaults to False.

    Returns:
        set: A set of Element instances, each wrapping a tuple that represents a unique permutation of a subset.
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


def order_code_intersection(a, b):
    """
    Identifies the intersection of two ordered tuples, maintaining the order of elements as they appear in the first tuple (`a`).
    For intersecting elements, their respective indices from both tuples are paired and sorted based on their appearance in `a`.

    Args:
        - a (tuple): The first ordered tuple of elements.
        - b (tuple): The second ordered tuple of elements.

    Returns:
        - list of tuples: Each tuple contains two integers representing the index of an intersecting element in tuples `a` and `b`, respectively.
                          The tuples are ordered by the element's position in `a`.

    Description:
        This function creates a mapping of elements to their indices in tuple `a` and updates it to include indices from tuple `b`.
        It ensures that only elements present in both tuples are considered, and for these elements, it records the maximum index encountered,
        effectively capturing the last occurrence of the element in both tuples if duplicates exist. The mapping is then transformed
        to group indices by their corresponding elements and sorted by the element's natural ordering from `a`.
        Finally, it computes the Cartesian product of the grouped indices, resulting in a list of tuples that represent the intersections.
    """

    def swap_key_value(input_dict):
        """
        Swaps the keys and values of a dictionary where values are hashable and can be lists.
        If multiple keys map to the same value, the new dictionary will have that value mapped to a list of all corresponding keys.

        Args:
            - input_dict (dict): The dictionary to transform, where keys are expected to be unique but values may not be.

        Returns:
            - dict: A new dictionary with original values as keys and lists of original keys as values.
                If a value was unique in the input, its corresponding key is wrapped in a single-element list.

        Description:
            This function iterates over each key-value pair in the `input_dict`. For each pair, it checks if the value already exists
            as a key in the `output_dict`. If not, it creates a new entry with the value as the key and the original key wrapped in a list as the value.
            If the value already exists, it appends the current key to the list of keys associated with that value. This results in a dictionary
            where values from the input dictionary become keys, and each key maps to a list of keys that were associated with the value in the original dictionary.
        """

        output_dict = {}
        for key, value in input_dict.items():
            if value not in output_dict:
                output_dict[value] = [key]
            else:
                output_dict[value].append(key)
        return output_dict

    res = {}

    for idx, sample in enumerate(a):
        if sample not in res:
            res[sample] = [idx]
        else:
            res[sample].append(idx)

    for idx, sample in enumerate(b):
        if sample not in res:
            res[sample] = [idx]
        else:
            res[sample].append(idx)

    for sample in res.keys():
        res[sample] = max(res[sample])

    res = swap_key_value(res)
    res = [res[key] for key in sorted(res.keys())]
    res = [tuple(order) for order in itertools.product(*res)]
    return res
