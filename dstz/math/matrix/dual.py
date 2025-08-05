import numpy as np

from dstz.core.atom import Element
from dstz.core.distribution import Evidence
from dstz.evpiece.single import get_fod
from dstz.math.matrix.const import get_qfrm, get_bfrm
from dstz.math.matrix.func import get_ones_indices


def matrix_rule(ev1, ev2, matrix, fod, mul=True, curItem=Element):
    """Combines two evidence objects using a generic matrix-based rule.

    This function provides a framework for evidence combination using linear
    algebra. It transforms evidence mass functions into another domain (e.g.,
    belief or commonality space) using a transformation matrix, combines them
    in that domain, and then transforms the result back into a mass function.

    Args:
        ev1 (Evidence): The first evidence object.
        ev2 (Evidence): The second evidence object.
        matrix (np.ndarray): The transformation matrix (e.g., BFRM or QFRM).
        fod (list): An ordered list of the singleton elements forming the
                    Frame of Discernment.
        mul (bool, optional): If `True`, the transformed vectors are combined
                              by element-wise multiplication. If `False`, they
                              are combined by division. Defaults to `True`.
        curItem (callable, optional): A factory function to create new item
            instances. Defaults to `Element`.

    Returns:
        Evidence: A new `Evidence` object representing the combined evidence.
    """
    ev = Evidence()
    events = []
    # Create vector representations of the mass functions
    ev1_m = np.zeros(2 ** len(fod))
    ev2_m = np.zeros(2 ** len(fod))
    for i in range(2 ** len(fod)):
        event = set()
        event_index = get_ones_indices(i)
        if event_index:
            for j in get_ones_indices(i):
                event.add(fod[j])
        element = Element(event)
        events.append(element)
        if element in ev1:
            ev1_m[i] = ev1[element]
        if element in ev2:
            ev2_m[i] = ev2[element]

    # Transform, combine, and inverse-transform
    ev1_q = np.dot(matrix, ev1_m)
    ev2_q = np.dot(matrix, ev2_m)
    if mul:
        ev_q = ev1_q * ev2_q
    else:
        ev_q = ev1_q / ev2_q
    matrix_inv = np.linalg.inv(matrix)
    ev_m = np.dot(matrix_inv, ev_q)

    # Convert the resulting vector back to an Evidence object
    for i in range(len(events)):
        if ev_m[i] > 0:
            ev[events[i]] = ev_m[i]
    return ev


def conjunctive_rule(ev1, ev2, curItem=Element):
    """Performs conjunctive combination using the matrix method.

    This function uses the Commonality Function Relation Matrix (QFRM) to
    perform the conjunctive rule of combination.

    Args:
        ev1 (Evidence): The first evidence object.
        ev2 (Evidence): The second evidence object.
        curItem (callable, optional): Factory function for new elements.
                                   Defaults to `Element`.

    Returns:
        Evidence: The combined evidence.
    """
    fod = list(get_fod(ev1).union(get_fod(ev2)))
    return matrix_rule(ev1, ev2, get_qfrm(len(fod)), fod)


def de_conjunctive_rule(ev1, ev2, curItem=Element):
    """Performs the inverse conjunctive combination using the matrix method.

    This can be used to "un-combine" evidence, effectively performing a
    division in the commonality space.

    Args:
        ev1 (Evidence): The evidence to be divided.
        ev2 (Evidence): The evidence to divide by.
        curItem (callable, optional): Factory function for new elements.
                                   Defaults to `Element`.

    Returns:
        Evidence: The resulting evidence.
    """
    fod = list(get_fod(ev1).union(get_fod(ev2)))
    return matrix_rule(ev1, ev2, get_qfrm(len(fod)), fod, False)


def disjunctive_rule(ev1, ev2, curItem=Element):
    """Performs disjunctive combination using the matrix method.

    This function uses the Belief Function Relation Matrix (BFRM) to
    perform the disjunctive rule of combination.

    Args:
        ev1 (Evidence): The first evidence object.
        ev2 (Evidence): The second evidence object.
        curItem (callable, optional): Factory function for new elements.
                                   Defaults to `Element`.

    Returns:
        Evidence: The combined evidence.
    """
    fod = list(get_fod(ev1).union(get_fod(ev2)))
    return matrix_rule(ev1, ev2, get_bfrm(len(fod)), fod)


def de_disjunctive_rule(ev1, ev2, curItem=Element):
    """Performs the inverse disjunctive combination using the matrix method.

    This can be used to "un-combine" evidence, effectively performing a
    division in the belief space.

    Args:
        ev1 (Evidence): The evidence to be divided.
        ev2 (Evidence): The evidence to divide by.
        curItem (callable, optional): Factory function for new elements.
                                   Defaults to `Element`.

    Returns:
        Evidence: The resulting evidence.
    """
    fod = list(get_fod(ev1).union(get_fod(ev2)))
    return matrix_rule(ev1, ev2, get_bfrm(len(fod)), fod, False)