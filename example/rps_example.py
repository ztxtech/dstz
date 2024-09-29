from dst.core.atom import Element
from dst.core.distribution import Evidence
from dst.evpiece.dual import rps_left_rule

# Create the first evidence instance with a single element and full belief
ev1 = Evidence({Element((1, 3, 2)): 1.0})
# This represents a scenario where there is absolute belief in the event containing elements 1, 3, and 2.

# Create the second evidence instance with another single element and full belief
ev2 = Evidence({Element((2, 3)): 1.0})
# This represents a scenario with absolute belief in the event containing elements 2 and 3.

# Apply the RPS Left-Rule to combine the two evidence instances
combined_ev = rps_left_rule(ev1, ev2)
# The RPS Left-Rule combines the evidence by computing intersections of events (as per the RPS theory)
# and updating the belief accordingly, respecting the principles of evidence combination.

# Print the resulting combined evidence distribution
print(combined_ev)
# The output will show the new Evidence object after the combination, reflecting how the beliefs
# about the events have been updated given the information from both ev1 and ev2.
