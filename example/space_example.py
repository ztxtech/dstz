from evidence_theory.element.combination import simple_space, powerset
from evidence_theory.math.stat.distribution import max_deng_entropy_distribution

# Generates a simple space of unique elements of specified length.
ss = simple_space(2)
print('simple space of length=2: ', ss)

# Generates the power set of a given set.
ps = powerset(ss)
print('powerset of above set: ', ps)

# Calculates the evidence distribution with maximum Deng entropy for a given number of elements.
max_distributions = max_deng_entropy_distribution(2)
print('maximum deng entropy distribution of length 2: ', max_distributions)
