import numpy as np
import ohai.computer_vision as cv


with Component(outputs=[A, B]) as comp_A:
    A = np.ones((8, 8))
    B = np.ones((8, 8))

with Component(inputs=[a], outputs=[b]) as comp_B:
    b = np.array(a) * 4

with Component(inputs=[a, b]) as comp_C:
    print(a)
    print(b)


A_out1, A_out2 = comp_A()
B_out = comp_B(A_out1)
C_out = cv.doublify(A_out2)
comp_C(B_out, C_out)
