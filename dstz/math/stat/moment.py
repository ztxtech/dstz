import math

from dstz.element.combination import powerset


def high_order_moment(ev, func, order, *args):
    """Calculates a high-order moment for an evidence distribution.

    This is a generalized function that computes statistical moments. It applies
    a given function `func` to each element in the evidence distribution,
    raises the result to the specified `order`, weights it by the element's
    mass, and sums the results.

    Args:
        ev (Evidence): The evidence distribution.
        func (callable): A function that takes an element, its mass, and any
            additional arguments, and returns a numerical value.
        order (int): The order of the moment to calculate (e.g., 1 for mean,
            2 for variance if centered).
        *args: Additional arguments to pass to `func`.

    Returns:
        float: The calculated high-order moment.
    """
    res = 0
    for element, mass in ev.items():
        res += (func(element, mass, *args) ** order) * mass
    return res


def deng_entropy(ev):
    """Calculates the Deng entropy of an evidence distribution.

    Deng entropy is a measure of uncertainty in evidence theory. It is
    defined as the first-order moment of the information content across all
    focal elements in the distribution, which is equivalent to the expected
    value of the information content.

    Args:
        ev (Evidence): The evidence distribution.

    Returns:
        float: The Deng entropy of the distribution.
    """
    return high_order_moment(ev, information_content, 1)


def information_var(ev):
    """Calculates the variance of the information content.

    This function measures the spread or dispersion of information content
    across the elements of an evidence distribution. It is calculated as the
    second-order moment of the *central* information content.

    Args:
        ev (Evidence): The evidence distribution.

    Returns:
        float: The variance of the information content.
    """
    return high_order_moment(ev, central_information_content, 2, ev)


def information_content(element, mass, event_generator=powerset,
                        component_generator=set):
    """Calculates the information content of a single focal element.

    Information content quantifies the amount of surprise or information
    conveyed by a piece of evidence. It is calculated based on the belief
    mass of the element and its cardinality (the number of possible outcomes
    it contains).

    Args:
        element (Element): The focal element of interest.
        mass (float): The belief mass associated with the element.
        event_generator (callable, optional): A function to generate events
            from components. Defaults to `powerset`.
        component_generator (callable, optional): A function to generate
            components from an element. Defaults to `set`.

    Returns:
        float: The information content value.
    """
    return -math.log2(mass / len(event_generator(component_generator(element))))


def central_information_content(element, mass, ev):
    """Calculates the central information content of a focal element.

    The central information content measures how much more or less informative
    a specific focal element is compared to the average informativeness of the
    entire evidence distribution. It is calculated by subtracting the mean
    information content (Deng Entropy) from the element's own information
    content.

    Args:
        element (Element): The focal element of interest.
        mass (float): The belief mass associated with the element.
        ev (Evidence): The entire evidence distribution, used to calculate
            the mean information content.

    Returns:
        float: The central information content value.
    """
    center = high_order_moment(ev, information_content, 1)
    return information_content(element, mass) - center