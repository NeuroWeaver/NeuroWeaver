import time
import pickle

import numpy as np


with Component(outputs=[a]) as C1:
    a = np.array([1, 2, 3])
    time.sleep(5)
    with open('a', 'ab') as f:
        pickle.dump(a, f)


with Component(inputs=[b]) as C2:
    time.sleep(5)
    with open('a', 'rb') as f:
        c = pickle.load(f)
        with open('test_C2', 'a') as f2:
            f2.write(str(c))


b = C1()
C2(b)
