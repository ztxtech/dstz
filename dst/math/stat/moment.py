import math

from evidence_theory.element.combination import powerset


def high_order_moment(ev, func, order, *args):
    """
    Calculates the high-order moment of a given function applied to each element-mass pair in an evidence distribution.

    Args:
        - ev (Evidence): An instance of the Evidence class representing the evidence distribution.
        - func (callable): A function that takes an element and its mass (and possibly additional arguments) and returns a numerical value.
        - order (int): The order of the moment to calculate.
        - \*args: Additional arguments to pass to the function `func`.

    Returns:
        float: The high-order moment of the given function applied to the evidence distribution.

    Description:
        High-order moments are statistical measures that capture the shape of the distribution of a function applied
        to each element-mass pair in an evidence distribution. The `high_order_moment` function computes this statistic
        by applying the given function `func` to each element in the distribution, raising the result to the power of `order`,
        multiplying by the corresponding mass, and summing these values across all elements in the distribution.
    """
    res = 0
    for element, mass in ev.items():
        res += (func(element, mass, *args) ** order) * mass
    return res


def deng_entropy(ev):
    """
    Calculates the Deng entropy of an evidence distribution.

    Args:
        - ev (Evidence): An instance of the Evidence class representing the evidence distribution.

    Returns:
        float: The Deng entropy of the evidence distribution.

    Description:
        Deng entropy is a measure of uncertainty in an evidence distribution. It is calculated as the high-order moment
        of order 1 of the information content function applied to the distribution. This function serves as a specific
        application of the `high_order_moment` function to calculate entropy.
    """
    return high_order_moment(ev, information_content, 1)


def information_var(ev):
    """
    Calculates the variance of the central information content in an evidence distribution.

    Args:
        - ev (Evidence): An instance of the Evidence class representing the evidence distribution.

    Returns:
        float: The variance of the central information content in the evidence distribution.

    Description:
        The information variance measures the spread of the central information content across the elements of an evidence
        distribution. It is calculated as the high-order moment of order 2 of the central information content function
        applied to the distribution. This function also leverages the `high_order_moment` function to compute the variance.
    """
    return high_order_moment(ev, central_information_content, 2, ev)


def information_content(element, mass, event_generator=powerset,
                        component_generator=set):
    """
    Calculates the information content associated with an element and its mass in an evidence distribution.

    Args:
        - element (Element): An instance of the Element class representing the element of interest.
        - mass (float): The mass associated with the given element in the evidence distribution.

    Returns:
        float: The information content of the given element and mass.

    Description:
        Information content quantifies the amount of information conveyed by an element with a given mass.
        It is calculated as the negative logarithm (base 2) of the ratio of the mass to the total number
        of possible combinations minus one. This measure is often used in information theory to assess
        the informativeness of a particular piece of evidence.
    """
    return -math.log2(mass / len(event_generator(component_generator(element))))


def central_information_content(element, mass, ev):
    """
    Calculates the central information content associated with an element and its mass in an evidence distribution.

    Args:
        - element (Element): An instance of the Element class representing the element of interest.
        - mass (float): The mass associated with the given element in the evidence distribution.
        - ev (Evidence): An instance of the Evidence class representing the evidence distribution.

    Returns:
        float: The central information content of the given element and mass.

    Description:
        Central information content adjusts the information content by subtracting the mean information content
        of the evidence distribution. This measure provides insight into how much more or less informative
        a particular piece of evidence is compared to the average informativeness of the entire distribution.
        It uses the high-order moment function to compute the mean information content of the distribution.
    """
    center = high_order_moment(ev, information_content, 1)
    return information_content(element, mass) - center
