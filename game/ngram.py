import numpy as np


class Nonogram:
    """Class representing a nonogram.

    :param matr_path: path to matrix to load
    :type matr_path: str
    """
    def __init__(self, matr_path: str) -> None:
        self.correct_matr = np.load(matr_path)
        self.current_matr = self.correct_matr.copy()
        self.current_matr[self.correct_matr < 0] = -3
        self.size = np.count_nonzero(self.correct_matr == -1)

    def change_matr(self, new_matr: np.ndarray) -> None:
        """Replace current matrix with a new one.

        :param new_matr: new matrix
        :type new_matr: np.ndarray
        """
        self.current_matr = new_matr

    def check(self) -> bool:
        """Check if input matrix is correct.

        :param matr: matrix to check
        :type matr: np.ndarray
        :return: True if correct, otherwise False
        :rtype: bool
        """
        return np.equal(self.current_matr == -1, self.correct_matr == -1).all()

    def progress(self) -> float:
        """Get the progress.

        :rtype: float
        """
        match = np.count_nonzero(np.logical_and(self.current_matr == -1, self.correct_matr == -1))
        return match / self.size
