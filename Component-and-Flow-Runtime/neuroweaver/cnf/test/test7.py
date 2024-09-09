"""Example of using abstract domain capabilities as components in C&F program.
"""

import ohai.deep_learning as dnn


with Component() as comp_A:
    A = [[1, 2], [3, 4]]
    B = [[5, 6], [7, 8]]
    C = dnn.matmul(A, B)
    print(C)

comp_A()
