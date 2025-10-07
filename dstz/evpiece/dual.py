import itertools

from dstz.core.atom import Element
from dstz.core.distribution import Evidence
from dstz.element.permutation import order_code_intersection


def ds_rule(ev1, ev2, curItem=Element):
    """Combines two evidence objects using the Dempster-Shafer rule.

    This function applies the classic Dempster-Shafer (DS) rule of
    combination to merge two mass functions (`ev1` and `ev2`). The rule
    combines belief from two independent sources by intersecting their
    focal elements and multiplying their masses.

    A key feature of the DS rule is its handling of conflict. Any mass
    assigned to the empty set as a result of the combination is used to
    normalize the masses of the remaining non-empty sets.

    Args:
        ev1 (Evidence): The first evidence object.
        ev2 (Evidence): The second evidence object.
        curItem (callable, optional): A factory function to create new item
            instances from the resulting intersections. Defaults to `Element`.

    Returns:
        Evidence: A new `Evidence` object representing the combined evidence.
    """
    res = Evidence()
    for key1, key2 in itertools.product(ev1.keys(), ev2.keys()):
        key = curItem(key1.value.intersection(key2.value))
        if key in res:
            res[key] += ev1[key1] * ev2[key2]
        else:
            res[key] = ev1[key1] * ev2[key2]
    empty_mass = res.pop(curItem(set()), None)
    if empty_mass:
        for key in res.keys():
            res[key] = res[key] / (1 - empty_mass)
    return res


def disjunctive_rule(ev1, ev2, curItem=Element):
    """Combines two evidence objects using the disjunctive rule.

    This rule merges two evidence distributions by calculating the intersection
    of their focal elements. The mass of a new focal element is the product
    of the masses of the original focal elements that form it. Unlike the
    Dempster-Shafer rule, this rule does not normalize for conflict.

    Args:
        ev1 (Evidence): The first evidence distribution.
        ev2 (Evidence): The second evidence distribution.
        curItem (callable, optional): A factory function to create new item
            instances from the resulting intersections. Defaults to `Element`.

    Returns:
        Evidence: A new evidence distribution representing the combined result.
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
    """Combines two evidence objects using the conjunctive rule.

    This rule merges two evidence distributions by calculating the union of
    their focal elements. The mass of a new focal element is the product
    of the masses of the original focal elements that form it.

    Args:
        ev1 (Evidence): The first evidence distribution.
        ev2 (Evidence): The second evidence distribution.
        curItem (callable, optional): A factory function to create new item
            instances from the resulting unions. Defaults to `Element`.

    Returns:
        Evidence: A new evidence distribution representing the combined result.
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
    """Combines two evidences using the Left-Rule for Relative Proof Strength.

    This function applies a specific combination rule where the intersection
    of focal elements is computed while preserving the order and duplicates
    from the first evidence object (`ev1`).

    Args:
        ev1 (Evidence): The first evidence object (the "left" side).
        ev2 (Evidence): The second evidence object.
        curItem (callable, optional): The factory function to create new
            element instances. Defaults to `Element`.

    Returns:
        Evidence: A new `Evidence` instance with the combined result.
    """
    res = Evidence()
    for key1, key2 in itertools.product(ev1.keys(), ev2.keys()):
        def left_intersection(a, b):
            # Computes intersection, preserving duplicates from 'a'.
            res = list(a)
            for i in set(a) - set(b).intersection(set(a)):
                res.remove(i)
            return tuple(res)

        # Create a new key using the special left-intersection.
        key = curItem(left_intersection(key1.value, key2.value))

        # Combine the probabilities for intersecting keys.
        if key in res:
            res[key] += ev1[key1] * ev2[key2]
        else:
            res[key] = ev1[key1] * ev2[key2]

    return res


def wang_orthogonal_rule(ev1, ev2, curItem=Element):
    """Applies the Wang Orthogonal Rule for Random Permutation Sets.

    This advanced combination rule is designed for evidence where the order
    of elements (permutations) is meaningful. It uses the
    `order_code_intersection` function to find intersecting permutations
    between the focal elements of `ev1` and `ev2`.

    The combined belief mass is distributed evenly among all resulting
    intersecting permutations. This method is based on the research paper:
    > Wang, Y., Li, Z., & Deng, Y. (2024). A new orthogonal sum in Random
    Permutation Set. Fuzzy Sets and Systems, 109034.

    Args:
        ev1 (Evidence): The first evidence set, containing ordered elements.
        ev2 (Evidence): The second evidence set, structured similarly to `ev1`.
        curItem (callable, optional): A factory function that creates an
            `Element` from a permutation. Defaults to `Element`.

    Returns:
        Evidence: A new `Evidence` instance representing the combined belief.
    """
    res = Evidence()
    for key1, key2 in itertools.product(ev1.keys(), ev2.keys()):
        cur_keys = [curItem(key) for key in order_code_intersection(key1.value, key2.value)]
        for key in cur_keys:
            if key in res:
                res[key] += ev1[key1] * ev2[key2] / len(cur_keys)
            else:
                res[key] = ev1[key1] * ev2[key2] / len(cur_keys)
    empty_mass = res.pop(curItem(()), None)
    if empty_mass:
        for key in res.keys():
            res[key] = res[key] / (1 - empty_mass)
    return res
