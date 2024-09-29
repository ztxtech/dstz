from dst.core.atom import Element
from dst.core.distribution import Evidence
from dst.math.stat.moment import deng_entropy, information_var

# Define an evidence distribution with assigned masses for each piece of evidence.
ev = {
    Element({'a'}): 1 / 7,
    Element({'b'}): 1 / 7,
    Element({'c'}): 1 / 7,
    Element({'a', 'b'}): 1 / 7,
    Element({'a', 'c'}): 1 / 7,
    Element({'b', 'c'}): 1 / 7,
    Element({'a', 'b', 'c'}): 1 / 7
}

# Wrap the distribution in an Evidence object for further processing.
ev = Evidence(ev)

# Calculate Deng entropy and information variance for the distribution.
d_entropy = deng_entropy(ev)
d_var = information_var(ev)

# Display the results.
print('entropy', d_entropy)
print('var', d_var)
