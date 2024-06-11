from evidence_theory.core.atom import Element
from evidence_theory.core.distribution import Evidence


def pignistic_probability_transformation(ev):
    """
    Transforms an evidence distribution into a probability distribution using the Pignistic transformation.

    Args:
        - ev (Evidence): An evidence distribution as an instance of the Evidence class.

    Returns:
        Evidence: A new evidence distribution transformed into a probability distribution.

    Description:
        This function implements the Pignistic transformation, which converts an evidence distribution
        into a probability distribution. Each basic belief assignment (BBA) in the input evidence is
        distributed uniformly across its focal elements. The result is a probability distribution
        where each single-element set has a probability equal to the sum of the masses of all BBAs
        that contain that element divided by the number of elements in those BBAs.
    """
    res = Evidence()
    for key in ev:
        for simple in key.value:
            s_item = Element(simple)
            if s_item in res:
                res[Element({s_item})] += ev[key] / len(key.value)
            else:
                res[Element({s_item})] = ev[key] / len(key.value)
    return res
