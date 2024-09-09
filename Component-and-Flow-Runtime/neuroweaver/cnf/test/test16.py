
with Component(outputs=[A]) as comp_A:
    A = [[1, 2], [3, 4]]

with Component(inputs=[a]) as comp_B:
    print(a)


for i in range(3):
    A = comp_A()
comp_B(A)
