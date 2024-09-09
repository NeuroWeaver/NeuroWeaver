"""Example of using imported modules in Components.
"""

import numpy as np

def myfunc(a, b):
    return a + b


with Component(outputs=[d]) as comp_A:
    a = [1, 2, 3]
    b = [4, 5, 6]
    c = np.dot(a, b)
    d = myfunc(10, c)

with Component(inputs=[f], outputs=[g]) as comp_B:
    g = f + 10

comp_A_out = comp_A()
comp_B_out = comp_B(comp_A_out)
comp_B_out2 = comp_B(comp_B_out)
