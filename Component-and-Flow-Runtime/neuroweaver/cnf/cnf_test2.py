

with Component() as Wrapper:
    with Component(outputs=[a]) as C1:
        print('C1')
        a = 5
    a = C1()
    with Component(inputs=[a]) as C2:
        print('C2')
    C2(a)
Wrapper()
