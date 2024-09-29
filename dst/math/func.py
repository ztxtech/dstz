def pl(element, ev):
    """
    Calculates the plausibility function value for a given element in an evidence distribution.

    Args:
        - element (Element): An instance of the Element class representing the element of interest.
        - ev (Evidence): An instance of the Evidence class representing the evidence distribution.

    Returns:
        float: The plausibility function value for the given element in the evidence distribution.

    Description:
        The plausibility function, denoted as Pl(A), measures the degree of support for the proposition
        that the actual state of affairs is included in set A. It is calculated as the sum of the masses
        assigned to all sets that intersect with A.
    """
    res = 0
    for key in ev:
        if element.value.intersection(key.value):
            res += ev[key]
    return res


def q(element, ev):
    """
    Calculates the commonality function value for a given element in an evidence distribution.

    Args:
        - element (Element): An instance of the Element class representing the element of interest.
        - ev (Evidence): An instance of the Evidence class representing the evidence distribution.

    Returns:
        float: The commonality function value for the given element in the evidence distribution.

    Description:
        The commonality function, denoted as Q(A), measures the degree of support for the proposition
        that the actual state of affairs includes set A. It is calculated as the sum of the masses
        assigned to all sets that contain A.
    """
    res = 0
    for key in ev:
        if key.value and element.value.issubset(key.value):
            res += ev[key]
    return res


def bel(element, ev):
    """
    Calculates the belief function value for a given element in an evidence distribution.

    Args:
        - element (Element): An instance of the Element class representing the element of interest.
        - ev (Evidence): An instance of the Evidence class representing the evidence distribution.

    Returns:
        float: The belief function value for the given element in the evidence distribution.

    Description:
        The belief function, denoted as Bel(A), measures the degree of support for the proposition
        that the actual state of affairs is contained in set A. It is calculated as the sum of the masses
        assigned to all sets that are subsets of A.
    """
    res = 0
    for key in ev:
        if key.value and key.value.issubset(element.value):
            res += ev[key]
    return res
