"""Simple test case which illustrates Component definition and instantiation.
The compiler creates a single Component and serializes it to protobuf.
"""

# Component definition
with Component() as comp_A:
    a = 1 + 2
    b = a + 2
    c = b - 2
    print(c)

# Component instantiation
comp_A()
