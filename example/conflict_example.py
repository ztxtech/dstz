from dst.core.atom import Element
from dst.core.distribution import Evidence
from dst.evpiece.dual import ds_rule

# Create an instance of Evidence with some predefined elements and their masses
e1 = Evidence()
e1[Element({'A'})] = 0.99
e1[Element({'B'})] = 0.01

# Create another instance of Evidence with some predefined elements and their masses
e2 = Evidence()
e2[Element({'C'})] = 0.99
e2[Element({'B'})] = 0.01

# Apply the Dempster-Shafer rule of combination on e1 and e2
e = ds_rule(e1, e2)

# Print the resulting combined evidence
print(e)
