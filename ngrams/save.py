import numpy as np

a = np.array([[0, 0, 1, 0, 1],
    [0, 0, 1, 1, 1],
    [1, 1, -1, -2, -1],
    [0, 1, -2, -1, -2],
    [1, 1, -1, -2, -1]])

np.save('./tiny.npy', a)
