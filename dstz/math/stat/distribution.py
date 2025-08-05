from dstz.core.atom import Element
from dstz.core.distribution import Evidence
from dstz.element.combination import simple_space, powerset
from dstz.element.permutation import permutation_set


def max_entropy_distribution(n, simple_generator, event_generator,
                             component_generator=set, condition_func=None):
    """Computes a maximum entropy distribution over a generated event space.

    This is a generalized function that creates a belief distribution based on
    the principle of maximum entropy. It assigns belief masses to events in a
    way that is as non-committal as possible, given the structure of the event
    space. The belief mass for each event is proportional to the size of its
    corresponding event space.

    Args:
        n (int): A size parameter passed to the `simple_generator`.
        simple_generator (function): A function that takes `n` and returns a
            simple space (a set of basic elements).
        event_generator (function): A function that takes the simple space and
            returns a set of all possible events.
        component_generator (function, optional): A function to create subsets
            of events. Defaults to `set`.
        condition_func (function, optional): A conditional function to apply
            to event generations. Defaults to `None`.

    Returns:
        Evidence: An `Evidence` instance representing the maximum entropy
                  distribution, where masses are normalized to sum to 1.
    """

    res = Evidence()
    ss = simple_generator(n)
    es = event_generator(ss)

    # Compute a weight for each event in the distribution.
    for element in es:
        count = len(condition_func(event_generator(component_generator(element)))) \
            if condition_func else len(event_generator(component_generator(element)))
        res[Element(element)] = float(count)

    # Normalize the weights to create a valid distribution.
    states = sum(res.values())
    for element in es:
        res[Element(element)] /= states

    return res


def max_deng_entropy_distribution(n):
    """Calculates the maximum Deng entropy distribution.

    This function provides a specific implementation of a maximum entropy
    distribution, known as Deng entropy. It is configured to generate events
    as the powerset of a simple space, which is a common scenario in
    evidence theory.

    Args:
        n (int): The size of the simple space (number of singleton elements).

    Returns:
        Evidence: The maximum Deng entropy distribution for the given size.
    """
    return max_entropy_distribution(n, simple_space, powerset)


def max_rps_entropy_distribution(n):
    """Computes the max entropy distribution for Random Permutation Sets (RPS).

    This function calculates a maximum entropy distribution where the events
    are all possible permutations of the elements in a simple space. This is
    useful for scenarios where the order of elements is significant.

    Args:
        n (int): The size of the simple space.

    Returns:
        Evidence: The maximum entropy distribution over all permutations.
    """
    return max_entropy_distribution(n, simple_space, permutation_set)