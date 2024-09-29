import numpy as np

from evidence_theory.core.atom import Element
from evidence_theory.core.distribution import Evidence
from evidence_theory.evpiece.single import get_fod
from evidence_theory.math.matrix.const import get_qfrm, get_bfrm
from evidence_theory.math.matrix.func import get_ones_indices


def matrix_rule(ev1, ev2, matrix, fod, mul=True, curItem=Element):
    ev = Evidence()
    events = []
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

    ev1_q = np.dot(matrix, ev1_m)
    ev2_q = np.dot(matrix, ev2_m)
    if mul:
        ev_q = ev1_q * ev2_q
    else:
        ev_q = ev1_q / ev2_q
    matrix_inv = np.linalg.inv(matrix)
    ev_m = np.dot(matrix_inv, ev_q)
    for i in range(len(events)):
        if ev_m[i] > 0:
            ev[events[i]] = ev_m[i]
    return ev


def conjunctive_rule(ev1, ev2, curItem=Element):
    fod = list(get_fod(ev1).union(get_fod(ev2)))
    return matrix_rule(ev1, ev2, get_qfrm(len(fod)), fod)


def de_conjunctive_rule(ev1, ev2, curItem=Element):
    fod = list(get_fod(ev1).union(get_fod(ev2)))
    return matrix_rule(ev1, ev2, get_qfrm(len(fod)), fod, False)


def disjunctive_rule(ev1, ev2, curItem=Element):
    fod = list(get_fod(ev1).union(get_fod(ev2)))
    return matrix_rule(ev1, ev2, get_bfrm(len(fod)), fod)


def de_disjunctive_rule(ev1, ev2, curItem=Element):
    fod = list(get_fod(ev1).union(get_fod(ev2)))
    return matrix_rule(ev1, ev2, get_bfrm(len(fod)), fod, False)
