

with Component() as Wrapper:
    with Component(outputs=[a]) as C1:
        print('C1')
        a = 5
        b = 3
        with open('test', 'a') as f:
            f.write(str(b))
    a = C1()
    with Component(inputs=[a], outputs=[b]) as C2:
        print('C2')
        b = a + 2
        with open('test', 'r') as f:
            c = f.read()
            print(c)
    b = C2(a)
Wrapper()


with Component(inputs=[b]) as Outer:
    c = b + 2
    print(c)


Outer(b)
