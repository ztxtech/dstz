import math

from dstz.core.atom import Element
from dstz.core.distribution import Evidence
from dstz.math.func import pl


def pignistic_probability_transformation(ev):
    """Transforms a belief distribution into a pignistic probability distribution.

    This transformation, often called BetP, converts a belief mass assignment
    into a classical probability distribution. It does this by distributing the
    mass of each focal element equally among all the individual (singleton)
    elements it contains.

    Args:
        ev (Evidence): An evidence distribution (mass function).

    Returns:
        Evidence: A new `Evidence` object representing the transformed
                  probability distribution.
    """
    res = Evidence()
    for key in ev:
        for simple in key.value:
            s_item = Element(simple)
            if s_item in res:
                res[s_item] += ev[key] / len(key.value)
            else:
                res[s_item] = ev[key] / len(key.value)
    return res


def get_fod(ev):
    """Computes the Frame of Discernment (FoD) for an evidence object.

    The Frame of Discernment is the set of all possible outcomes, which is
    constructed here by collecting all unique singleton elements from all
    focal sets within the given evidence.

    Args:
        ev (Evidence): The evidence object.

    Returns:
        set: A set containing all unique singleton elements in the evidence.
    """
    res = set()
    for ele in ev.keys():
        for item in ele.value:
            res.add(item)
    return res


def shafer_discounting(ev, alpha, fod=None):
    """Applies Shafer's discounting to an evidence object.

    Shafer discounting models partial reliability of an information source by
    transferring a portion of belief mass from each focal element to the
    entire Frame of Discernment (representing uncertainty).

    Where alpha represents the degree of trust (1 = fully trusted, 0 = not trusted at all).

    Args:
        ev (Evidence): The evidence object to be discounted.
        alpha (float): The discount factor, a value between 0 and 1 representing
                       the degree of trust in the evidence source.
        fod (set, optional): Precomputed frame of discernment. If None, will be computed.

    Returns:
        Evidence: A new, discounted `Evidence` object where belief masses have
                  been adjusted according to the discounting factor.
    """

    res = Evidence()
    # Get Frame of Discernment
    if not fod:
        fod = get_fod(ev)
    fod_element = Element(fod)

    # Apply discounting to each focal element: multiply by trust factor alpha
    for key, value in ev.items():
        res[key] = alpha * value

    # Transfer the untrusted portion (1-alpha) to the universal set
    if fod_element in res:
        res[fod_element] += (1 - alpha)
    else:
        res[fod_element] = (1 - alpha)

    return res


def contour_transformation(ev):
    """Transforms a belief distribution into a contour function.

    This transformation calculates the plausibility of each individual
    (singleton) element in the Frame of Discernment. The resulting
    distribution assigns each singleton element a mass equal to its
    plausibility value.

    Args:
        ev (Evidence): The evidence distribution.

    Returns:
        Evidence: A new `Evidence` object representing the contour function.
    """
    fod = get_fod(ev)
    res = Evidence()
    for event in fod:
        res[Element({event})] = pl(Element({event}), ev)
    return res


def temperature_transformation(ev, t):
    """
    Apply temperature-based transformation to evidence values.
    
    This function performs a temperature scaling operation on evidence values.
    
    Args:
        ev (Evidence): Input evidence object containing key-value pairs where
                      values represent belief masses for corresponding keys.
        t (float): Temperature parameter.
    
    Returns:
        Evidence: A new Evidence object with temperature-transformed and
                 normalized values.
    """
    res = Evidence()
    for key, value in ev.items():
        # Apply temperature scaling: scale each value by its normalized position
        # The denominator (2^len(key) - 1) represents the maximum possible value for this key
        res[key] = math.pow(value / (2 ** len(key) - 1), t) * (2 ** len(key) - 1)

    # Normalize the transformed values to ensure they sum to 1.0
    norm_factor = sum(res.values())
    for key, value in res.items():
        res[key] = value / norm_factor

    return res
