import itertools
from itertools import combinations, permutations

from dstz.core.atom import Element


def permutation_set(simple_space, allow_empty=False):
    """Generates all permutations of all subsets from a given space.

    This function first finds all subsets of `simple_space` (similar to a
    powerset) and then generates all possible orderings (permutations) for
    each of these subsets. Each unique permutation is wrapped in an `Element`
    object.

    Args:
        simple_space (set): The input set from which to generate permutations.
        allow_empty (bool, optional): If `True`, includes a representation for
            the empty set. Defaults to `False`.

    Returns:
        set: A set of `Element` instances, where each instance contains a
             tuple representing a unique permutation.

    Example:
        >>> s = {Element('A'), Element('B')}
        >>> permutation_set(s)
        {Element(('A',)), Element(('B',)), Element(('A', 'B')), Element(('B', 'A'))}
    """
    res = []
    start_index = 0 if allow_empty else 1
    for r in range(start_index, len(simple_space) + 1):
        for subset in combinations(simple_space, r):
            res.extend(permutations(subset))
    return {Element(element) for element in res}


def order_code_intersection(a, b):
    """Finds the ordered intersection of two tuples.

    This function identifies elements that are common to both input tuples,
    `a` and `b`. It returns a list of tuples, where each inner tuple
    represents a valid sequence of indices corresponding to the common
    elements. The indices are determined by taking the maximum index for each
    common element from both tuples, and the final result is sorted based on
    these indices to maintain a combined ordering from both input sequences.

    Args:
        a (tuple): The first ordered tuple.
        b (tuple): The second ordered tuple.

    Returns:
        list: A list of tuples, where each inner tuple contains the indices
              of an intersecting element from `a` and `b` respectively. The
              list is ordered based on the combined index values from both
              input tuples.
    """

    def swap_key_value(input_dict):
        """Swaps the keys and values of a dictionary.

        If multiple keys in the input dictionary share the same value, the new
        dictionary will map that value to a list of all corresponding keys.

        Args:
            input_dict (dict): The dictionary to be inverted.

        Returns:
            dict: A new dictionary with original values as keys and lists of
                  original keys as values.
        """
        output_dict = {}
        for key, value in input_dict.items():
            if value not in output_dict:
                output_dict[value] = [key]
            else:
                output_dict[value].append(key)
        return output_dict

    res = {}
    excluded_samples = set(a).union(set(b)) - set(a).intersection(set(b))

    # Map each element in 'a' to a list of its indices
    for idx, sample in enumerate(a):
        if sample not in res:
            res[sample] = [idx]
        else:
            res[sample].append(idx)

    # Append indices from 'b' for common elements
    for idx, sample in enumerate(b):
        if sample not in res:
            res[sample] = [idx]
        else:
            res[sample].append(idx)

    # For each element, keep only the maximum index
    for sample in res.keys():
        res[sample] = max(res[sample])

    for sample in excluded_samples:
        if sample in res:
            res.pop(sample)

    # Invert the dictionary to group elements by index
    res = swap_key_value(res)
    # Sort groups by index to maintain order from 'a'
    res = [res[key] for key in sorted(res.keys())]
    # Compute the Cartesian product to get all valid intersection paths
    res = [tuple(order) for order in itertools.product(*res)]
    return res
