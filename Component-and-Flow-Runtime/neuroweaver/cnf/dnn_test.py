import numpy as np

import ohai.deep_learning as dnn


with Component(outputs=[i, weights, biases]) as datagen:
    i = np.random.randn(1, 32, 32, 3)
    weights = np.random.randn(128, 3, 3, 3)
    biases = np.random.randn(128)

i, weights, biases = datagen()
conv = dnn.conv2d(i, weights, biases)
pool = dnn.max_pool(conv)
