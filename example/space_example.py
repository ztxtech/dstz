from dstz.element.combination import simple_space, powerset
from dstz.element.permutation import permutation_set
from dstz.math.stat.distribution import max_deng_entropy_distribution, max_rps_entropy_distribution

# Generates a simple space of unique elements of specified length.
ss = simple_space(2)
print('simple space of length=2: ', ss)

# Generates the power set of a given set.
ps = powerset(ss)
print('powerset of above set: ', ps)

# Calculates the evidence distribution with maximum Deng entropy for a given number of elements.
max_distributions = max_deng_entropy_distribution(2)
print('maximum deng entropy distribution of length 2: ', max_distributions)

# Generate the permutation set for the simple space 'ss' and print it
per_s = permutation_set(ss)
print('Permutation set of the above set:', per_s)

# Generate the power set for the same simple space 'ss' and print it
ps = powerset(ss)  # Assuming powerset is a defined function similar to 'permutation_set'
print('Power set of the above set:', ps)

# Calculate the maximum relative proof strength (RPS) entropy distribution for a set of length 2
# and print the resulting distribution. This assumes 'max_rps_entropy_distribution' is a defined function.
max_distributions = max_rps_entropy_distribution(2)
print('Maximum RPS entropy distribution of length 2:', max_distributions)
