# Import necessary classes and functions from the evidence theory package
from dst.core.atom import Element
from dst.core.distribution import Evidence
from dst.evpiece.single import pignistic_probability_transformation, deng_entropy

# Create an instance of Evidence with a single belief assignment over a set of elements {A, B, C}
ev = Evidence()
ev[Element({'A', 'B', 'C'})] = 1.0  # Assign full belief to the set {A, B, C}

# Print the original evidence distribution
print('primary: ', ev)

# Calculate and print the Deng entropy of the original evidence distribution
print('entropy', deng_entropy(ev))

# Transform the original evidence distribution into a probability distribution using Pignistic transformation
bet_ev = pignistic_probability_transformation(ev)

# Print the evidence distribution after Pignistic transformation
print('after ppt: ', bet_ev)

# Calculate and print the Deng entropy of the evidence distribution after Pignistic transformation
print('entropy', deng_entropy(bet_ev))
