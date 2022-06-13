import PlayingWithNonograms.proc
import os
import numpy as np

ngrams_dir = "PlayingWithNonograms/ngrams"
ws = (1920, 1080)
step = 60


def test_init():
    for file in os.listdir(ngrams_dir):
        if file.endswith(".npy"):
            matr = np.load(os.path.join(ngrams_dir, file))
            ngram_shape = (matr.shape[0] * step,
                           matr.shape[1] * step)
            left = ws[0] // 2 - ngram_shape[0] // 2 - 100
            top = ws[1] // 2 - ngram_shape[1] // 2 - 100
            assert PlayingWithNonograms.proc.GameProcessor(matr, left + 100, top + 100, step)


def test_click():
    for file in os.listdir(ngrams_dir):
        if file.endswith(".npy"):
            matr = np.load(os.path.join(ngrams_dir, file))
            ngram_shape = (matr.shape[0] * step,
                           matr.shape[1] * step)
            left = ws[0] // 2 - ngram_shape[0] // 2
            top = ws[1] // 2 - ngram_shape[1] // 2
            gp = PlayingWithNonograms.proc.GameProcessor(matr, left, top, step)
            for i in range(ws[0]):
                for j in range(ws[1]):
                    res = gp.click(i, j)
                    li = (i - left) // step
                    ti = (j - top) // step
                    if li in range(matr.shape[0]) and ti in range(matr.shape[1]):
                        assert res and li == res[0] and ti == res[1]
                    else:
                        assert not res
