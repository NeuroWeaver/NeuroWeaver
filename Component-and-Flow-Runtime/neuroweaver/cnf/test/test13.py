import numpy as np

import ohai.analytics as analytics


with Component(outputs=[x, y]) as comp_A:
    x = np.arange(10).reshape(-1, 1)
    y = np.array([0, 0, 0, 0, 1, 1, 1, 1, 1, 1])

with Component(inputs=[a]) as comp_B:
    print(a)


x, y = comp_A()
out = analytics.logistic_regression(x, y)
comp_B(out)
