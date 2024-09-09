import numpy as np

def myfunc(a, b):
    return a + b


with Component('comp_A') as comp_A:
    a = [1, 2, 3]
    b = [4, 5, 6]
    c = np.dot(a, b)
    d = myfunc(10, c)
    print(d)
    with Component('comp_B', inputs=[f], outputs=[e]) as comp_B:
        g = f + 1
        e = g - 10
        print(e)
    i = comp_B(d)
    h = i + 2
    with Component('comp_C', inputs=[h]) as comp_C:
        j = h - 2
        print(j)
    comp_C(h)

comp_A()
