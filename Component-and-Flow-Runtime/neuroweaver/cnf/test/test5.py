""" This import should be ignored
import garbage"""
import numpy as np

def myfunc(a, b):
    return a + b


with Component('main') as main:
    with Component('comp_B', outputs=[d]) as comp_B:
        a = [1, 2, 3]
        b = [4, 5, 6]
        c = np.dot(a, b)
        d = myfunc(10, c)
    d = comp_B()
    with Component('comp_C', inputs=[f], outputs=[e]) as comp_C:
        g = f + 1
        e = g - 10
    i = comp_C(d)
    with Component('comp_D', inputs=[i], outputs=[h]) as comp_D:
        h = i + 2
    h = comp_D(i)
    with Component('comp_E', inputs=[h]) as comp_E:
        j = h - 2
    comp_E(h)

main()
