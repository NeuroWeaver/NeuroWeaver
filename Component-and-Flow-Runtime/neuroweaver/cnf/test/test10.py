import ohai.deep_learning as dnn


with Component(outputs=[A, B]) as comp_A:
    A = [[1, 2], [3, 4]]
    B = [[5, 6], [7, 8]]

with Component(inputs=[a]) as comp_C:
    print(a)


A1, A2 = comp_A()
out = dnn.matmul(A1, A2)
comp_C(out)
