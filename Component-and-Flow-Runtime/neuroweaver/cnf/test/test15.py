import ohai.deep_learning as dnn
from time import sleep


with Component(outputs=[A, B]) as comp_A:
    A = [[1, 2], [3, 4]]
    B = [[5, 6], [7, 8]]

with Component(inputs=[a, b], outputs=[c]) as comp_B:
    sleep(20)
    c = a + b

with Component(inputs=[a, b]) as comp_C:
    print(a)
    print(b)



A, B = comp_A()
b = comp_B(A, B)
a = dnn.matmul(A, B)
comp_C(a, b)
