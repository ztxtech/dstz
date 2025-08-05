def pl(element, ev):
    """Calculates the plausibility of an element.

    The plausibility function (Pl) measures the total belief that can possibly
    be attributed to a hypothesis (represented by `element`). It is calculated
    as the sum of the masses of all focal sets that have a non-empty
    intersection with the element's value set.

    Args:
        element (Element): The element representing the hypothesis of interest.
        ev (Evidence): The evidence distribution (mass function).

    Returns:
        float: The plausibility value for the given element.
    """
    res = 0
    for key in ev:
        if element.value.intersection(key.value):
            res += ev[key]
    return res


def q(element, ev):
    """Calculates the commonality function for an element.

    The commonality function (Q) measures the total belief that is committed
    to a body of evidence that contains the hypothesis (`element`) as a subset.
    It is calculated as the sum of the masses of all focal sets that are
    supersets of the element's value set.

    Args:
        element (Element): The element representing the hypothesis of interest.
        ev (Evidence): The evidence distribution (mass function).

    Returns:
        float: The commonality value for the given element.
    """
    res = 0
    for key in ev:
        if key.value and element.value.issubset(key.value):
            res += ev[key]
    return res


def bel(element, ev):
    """Calculates the belief function for an element.

    The belief function (Bel) measures the total belief that is directly
    committed to a hypothesis (represented by `element`). It is calculated
    as the sum of the masses of all focal sets that are subsets of the
    element's value set.

    Args:
        element (Element): The element representing the hypothesis of interest.
        ev (Evidence): The evidence distribution (mass function).

    Returns:
        float: The belief value for the given element.
    """
    res = 0
    for key in ev:
        if key.value and key.value.issubset(element.value):
            res += ev[key]
    return res