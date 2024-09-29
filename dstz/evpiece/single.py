from dstz.core.atom import Element
from dstz.core.distribution import Evidence
from dstz.evpiece.dual import disjunctive_rule
from dstz.math.func import pl


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


def get_fod(ev):
    res = set()
    for ele in ev.keys():
        for item in ele.value:
            res.add(item)
    return res


def shafer_discounting(ev, alpha):
    ev_tmp = Evidence()
    ev_tmp[Element(set())] = 1 - alpha
    ev_tmp[Element(get_fod(ev))] = alpha
    res = disjunctive_rule(ev, ev_tmp)
    return res


def contour_transformation(ev):
    fod = get_fod(ev)
    res = Evidence()
    for event in fod:
        res[Element({event})] = pl(Element({event}), ev)
    return res


ev = Evidence()
ev[Element({'a', 'b', 'c'})] = 0.5
ev[Element({'b', 'c'})] = 0.3
ev[Element({'a'})] = 0.2
print(contour_transformation(ev))
