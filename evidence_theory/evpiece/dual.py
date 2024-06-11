import itertools

from evidence_theory.core.atom import Element
from evidence_theory.core.distribution import Evidence


def ds_rule(ev1, ev2, curItem=Element):
    """
    Applies the Dempster-Shafer rule of combination on two evidences.

    This function combines two evidences (ev1 and ev2) using the Dempster-Shafer rule of combination.
    It computes the combination of mass functions from two different sources of evidence for the same
    hypothesis space defined by 'curItem'. The function returns a new Evidence object that represents
    the combined evidence.

    Args:
        - ev1 (Evidence): The first evidence as an instance of the Evidence class.
        - ev2 (Evidence): The second evidence as an instance of the Evidence class.
        curItem (callable): A callable that takes a set and returns an instance of Item. It defines
                            how to create items from set intersections.

    Returns:
        Evidence: A new instance of Evidence that represents the combined evidence after applying
                  the Dempster-Shafer rule of combination.

    Notes:
        - The Dempster-Shafer rule of combination deals with conflicts between pieces of evidence
          by reducing the mass of the empty set and redistributing it among non-empty sets.
        - If there is a conflict (i.e., the mass of the empty set is not zero), the masses of all
          non-empty sets are adjusted proportionally to account for the conflict.
    """
    res = Evidence()
    for key1, key2 in itertools.product(ev1.keys(), ev2.keys()):
        key = curItem(key1.value.intersection(key2.value))
        if key in res:
            res[key] += ev1[key1] * ev2[key2]
        else:
            res[key] = ev1[key1] * ev2[key2]
    empty_mass = res.pop(curItem(set()))
    if empty_mass:
        for key in res.keys():
            res[key] = res[key] / (1 - empty_mass)
    return res


def disjunctive_rule(ev1, ev2, curItem=Element):
    """
    Combines two evidence distributions using the disjunctive rule of combination.

    Args:
        - ev1 (Evidence): The first evidence distribution as an instance of the Evidence class.
        - ev2 (Evidence): The second evidence distribution as an instance of the Evidence class.
        - curItem (callable, optional): A callable that takes a set and returns an instance of Item.
                                      Defaults to the Element class.

    Returns:
        Evidence: A new evidence distribution representing the combination of ev1 and ev2 using the
                  disjunctive rule of combination.

    Description:
        The disjunctive rule of combination is applied to merge two evidence distributions by
        considering only the intersection of the focal elements of each distribution. The resulting
        distribution assigns a mass to each possible intersection of focal elements from ev1 and ev2.
    """
    res = Evidence()
    for key1, key2 in itertools.product(ev1.keys(), ev2.keys()):
        key = curItem(key1.value.intersection(key2.value))
        if key in res:
            res[key] += ev1[key1] * ev2[key2]
        else:
            res[key] = ev1[key1] * ev2[key2]
    return res


def conjunctive_rule(ev1, ev2, curItem=Element):
    """
    Combines two evidence distributions using the conjunctive rule of combination.

    Args:
        - ev1 (Evidence): The first evidence distribution as an instance of the Evidence class.
        - ev2 (Evidence): The second evidence distribution as an instance of the Evidence class.
        - curItem (callable, optional): A callable that takes a set and returns an instance of Item.
                                      Defaults to the Element class.

    Returns:
        Evidence: A new evidence distribution representing the combination of ev1 and ev2 using the
                  conjunctive rule of combination.

    Description:
        The conjunctive rule of combination is applied to merge two evidence distributions by
        considering the union of the focal elements of each distribution. The resulting distribution
        assigns a mass to each possible union of focal elements from ev1 and ev2.
    """
    res = Evidence()
    for key1, key2 in itertools.product(ev1.keys(), ev2.keys()):
        key = curItem(key1.value.union(key2.value))
        if key in res:
            res[key] += ev1[key1] * ev2[key2]
        else:
            res[key] = ev1[key1] * ev2[key2]
    return res


def rps_left_rule(ev1, ev2, curItem=Element):
    """
    Apply the Left-Rule of combination in the context of Relative Proof Strength (RPS) Theory to combine two pieces of evidence.

    Args:
    - ev1 (Evidence): The first evidence object containing elements (keys) with associated probabilities (values).
    - ev2 (Evidence): The second evidence object to be combined with the first, structured similarly to `ev1`.
    - curItem (class, optional): The class used to instantiate new elements for the resulting evidence set.
                               Defaults to `Element`.

    Returns:
    - Evidence: A new Evidence instance representing the combined evidence after applying the Left-Rule.

    Description:
    This function combines two evidence objects (`ev1` and `ev2`) using the Left-Rule, which involves finding the
    intersection of keys (events) from both evidences and multiplying their corresponding probabilities. The result
    maintains the order and duplicates from `ev1`. The `left_intersection` function is defined locally to compute
    these intersections. The combined evidence values are summed for intersecting keys in the resulting evidence set.

    Example Usage:
    >>> ev1 = Evidence({Element((1,)): 0.6, Element((2,)): 0.4})
    >>> ev2 = Evidence({Element((1,)): 0.7, Element((3,)): 0.3})
    >>> combined_ev = rps_left_rule(ev1, ev2)
    >>> print(combined_ev)
    // Output will reflect the combined evidence based on the Left-Rule.
    """
    res = Evidence()
    for key1, key2 in itertools.product(ev1.keys(), ev2.keys()):
        def left_intersection(a, b):
            # Local function to compute the intersection, preserving duplicates from 'a'
            res = list(a)
            for i in set(a) - set(b).intersection(set(a)):
                res.remove(i)
            return tuple(res)

        # Create a new key using the intersection of values from ev1 and ev2
        key = curItem(left_intersection(key1.value, key2.value))

        # Combine the probabilities for intersecting keys
        if key in res:
            res[key] += ev1[key1] * ev2[key2]
        else:
            res[key] = ev1[key1] * ev2[key2]

    return res
