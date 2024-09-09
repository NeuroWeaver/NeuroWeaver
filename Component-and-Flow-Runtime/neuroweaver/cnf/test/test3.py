"""Example of subcomponent definition and instantiation.
"""

with Component(outputs=[e]) as comp_A:
    a = 1 + 2
    b = a + 2
    c = b - 2
    with Component(inputs=[a], outputs=[c]) as comp_B:
        b = a + 1
        c = b - 10
        print(c)
    d = comp_B(c)
    e = d + 2
    print(e)

out = comp_A()
print(out)
