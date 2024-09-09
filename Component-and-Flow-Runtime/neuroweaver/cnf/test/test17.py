import ohai.deep_learning as dnn


with Component(outputs=[A, B]) as comp_A:
    A = [[1, 2], [3, 4]]
    B = [[5, 6], [7, 8]]

with Component(inputs=[a]) as comp_B:
    print(a)


for i in range(2):
    A, B = comp_A()
    a = dnn.matmul(A, B)
