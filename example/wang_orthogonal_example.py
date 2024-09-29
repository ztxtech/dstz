from dstz.core.atom import Element
from dstz.core.distribution import Evidence
# Import the Wang Orthogonal Rule function for combining dual evidence pieces in evidence theory
from dstz.evpiece.dual import wang_orthogonal_rule

# Initialize the first piece of evidence
ev1 = Evidence({
    # Define an evidence item where the key is an ordered set of elements ('a', 'b', 'c', 'd', 'e'),
    # and the value is its associated belief degree (confidence) of 1.0
    Element(('a', 'b', 'c', 'd', 'e')): 1.0
})

# Initialize the second piece of evidence
ev2 = Evidence({
    # Similarly, define another evidence item with a different ordered set ('b', 'c', 'd', 'e', 'a'),
    # also with a belief degree of 1.0
    Element(('b', 'c', 'd', 'e', 'a')): 1.0
})

# Apply the Wang Orthogonal Rule to combine the two pieces of evidence
# This rule is specifically designed to handle ordered permutations within the evidence sets
ev = wang_orthogonal_rule(ev1, ev2)

# Output the combined evidence to observe the result of the orthogonal combination
print(ev)
