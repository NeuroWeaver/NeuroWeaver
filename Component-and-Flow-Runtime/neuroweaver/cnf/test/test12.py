import ohai.deep_learning as dnn


with Component(outputs=[A, B]) as comp_A:
    A = [[1, 2], [3, 4]]
    B = [[5, 6], [7, 8]]

with Component(inputs=[a]) as comp_B:
    print(a)



A, B = comp_A()
a = dnn.matmul(A, B)
comp_B(a)
