"""Example where output of one leaf Component is input to another leaf Component.
"""

# Component definition
with Component(outputs=[c]) as comp_A:
    a = 1 + 2
    b = a + 2
    c = b - 2

# Component definition
with Component(inputs=[a]) as comp_B:
    b = a + 1
    c = b - 10
    print(c)

# Component instantiation
comp_A_out = comp_A()
comp_B(comp_A_out)
