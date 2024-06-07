import math

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


def deng_entropy(ev, base=2):
    """
    Calculates the Deng entropy of an evidence distribution.

    Args:
        - ev (Evidence): An evidence distribution as an instance of the Evidence class.
        - base (int, optional): The logarithmic base to use for entropy calculation. Defaults to 2.

    Returns:
        float: The Deng entropy of the evidence distribution.

    Description:
        This function calculates the Deng entropy of an evidence distribution, which is a measure
        of uncertainty or randomness within the distribution. The Deng entropy is calculated by
        summing the negative log (to the specified base) of the ratio of each BBA mass to the total
        number of possible combinations minus one, weighted by the BBA mass itself.
    """
    res = 0
    for key in ev:
        inf_content = -ev[key] * math.log(ev[key] / (2 ** len(key) - 1), base)
        res += inf_content
    return res
