import ohai.deep_learning as dnn


with Component(outputs=[C]) as comp_A:
    A = [[1, 2], [3, 4]]
    B = [[5, 6], [7, 8]]
    C = dnn.matmul(A, B)

with Component(inputs=[a]) as comp_B:
    print(a)

comp_A_out = comp_A()
comp_B(comp_A_out)
