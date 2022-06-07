import PlayingWithNonograms.ngram
import os
import numpy as np


def test_init():
    for file in os.listdir("ngrams"):
        if file.endswith(".npy"):
            assert PlayingWithNonograms.ngram.Nonogram("ngrams/" + file)


def test_change_matr():
    for file in os.listdir("ngrams"):
        if file.endswith(".npy"):
            ng = PlayingWithNonograms.ngram.Nonogram("ngrams/" + file)
            matr = ng.current_matr.copy()
            for i in range(0, matr.shape[0]):
                for j in range(0, matr.shape[1]):
                    ng.change_matr(i, j, 3)
                    ng.change_matr(i, j, 3)
                    ng.change_matr(i, j, 1)
                    ng.change_matr(i, j, 1)
                    assert matr[i][j] >= 0 or ng.current_matr[i][j] <= 0


def test_autofill():
    for file in os.listdir("ngrams"):
        if file.endswith(".npy"):
            ng = PlayingWithNonograms.ngram.Nonogram("ngrams/" + file)
            matr = ng.correct_matr
            ids = np.transpose(np.nonzero(matr == -1))
            for id in ids:
                ng.change_matr(*id, 1)
            assert np.equal(np.nonzero(ng.correct_matr == -2),
                            np.nonzero(ng.current_matr == -2)).all()


def test_check():
    for file in os.listdir("ngrams"):
        if file.endswith(".npy"):
            ng = PlayingWithNonograms.ngram.Nonogram("ngrams/" + file)
            matr = ng.correct_matr
            ids = np.transpose(np.nonzero(matr == -1))
            for id in ids:
                ng.change_matr(*id, 1)
                assert (not ng.check()) if (id != ids[-1]).any() else ng.check()


def test_progress():
    for file in os.listdir("ngrams"):
        if file.endswith(".npy"):
            ng = PlayingWithNonograms.ngram.Nonogram("ngrams/" + file)
            matr = ng.correct_matr
            ids = np.transpose(np.nonzero(matr == -1))
            cnt = 0
            for id in ids:
                ng.change_matr(*id, 1)
                cnt += 1
                assert ng.progress() == cnt / len(ids)
