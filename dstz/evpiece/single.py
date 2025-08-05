from dstz.core.atom import Element
from dstz.core.distribution import Evidence
from dstz.evpiece.dual import disjunctive_rule
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


def shafer_discounting(ev, alpha):
    """Applies Shafer's discounting to an evidence object.

    Discounting reduces the belief assigned to focal sets by a discount rate
    `alpha`. The total discounted mass is then transferred to the entire
    Frame of Discernment, representing an increase in overall uncertainty.

    Args:
        ev (Evidence): The evidence object to be discounted.
        alpha (float): The discount rate, a value between 0 and 1. `alpha`
                       represents the degree of trust in the evidence source.

    Returns:
        Evidence: A new, discounted `Evidence` object.
    """
    ev_tmp = Evidence()
    ev_tmp[Element(set())] = 1 - alpha
    ev_tmp[Element(get_fod(ev))] = alpha
    res = disjunctive_rule(ev, ev_tmp)
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