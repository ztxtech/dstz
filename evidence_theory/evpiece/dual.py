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
