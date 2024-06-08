from evidence_theory.core.atom import Element
from evidence_theory.core.distribution import Evidence
from evidence_theory.element.combination import simple_space, powerset


def max_deng_entropy_distribution(n):
    """
    Generates an evidence distribution that maximizes Deng entropy for a given number of elements.

    Parameters:
    - n (int): The number of elements in the simple space.

    Returns:
    - Evidence: An evidence distribution maximizing Deng entropy.

    Description:
    This function creates an evidence distribution with the highest possible Deng entropy for a given
    number of elements. It starts by generating a simple space of 'n' elements, then calculates the
    power set of this space to obtain all possible subsets. Each subset in the power set is associated
    with a mass proportional to the number of subsets in its own power set, divided by the total number
    of subsets across all power sets of elements in the original simple space. This ensures that the
    distribution has maximum uncertainty, as measured by Deng entropy.
    """
    # Initialize an empty evidence distribution.
    res = Evidence()

    # Generate a simple space with 'n' elements.
    ss = simple_space(n)

    # Compute the power set of the simple space.
    ps = powerset(ss)

    # Sum the number of subsets in the power sets of all elements in the power set.
    states = sum([len(powerset(element.value)) for element in ps])

    # Assign masses to each subset in the power set of the simple space.
    for element in powerset(ss):
        # Calculate the mass as the ratio of the number of subsets in the power set of the current subset
        # to the total number of subsets across all power sets.
        res[Element(element)] = len(powerset(element.value)) / states

    # Return the constructed evidence distribution.
    return res
