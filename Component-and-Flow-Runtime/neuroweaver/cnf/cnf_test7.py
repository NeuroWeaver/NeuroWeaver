import time


with Component() as main:
    with Component(outputs=[a]) as C1:
        a = 5
        print(f'C1: {a}')
        time.sleep(1)
    a = C1()
    with Component(inputs=[a], outputs=[b]) as C2:
        b = a + 2
        print(f'C2: {b}')
        time.sleep(1)
    b = C2(a)
    with Component(inputs=[a], outputs=[c]) as C3:
        c = a + 3
        print(f'C3: {c}')
        time.sleep(3)
    b = C3(a)
    with Component(inputs=[d]) as C4:
        print(f'C4: {d}')
        time.sleep(1)
    C4(b)
main()
