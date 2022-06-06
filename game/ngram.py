"""Module with nonogram class controlling the statuses of the cells."""
import numpy as np


class Nonogram:
    """Class representing a nonogram.

    :param matr_path: path to matrix to load
    :type matr_path: str
    """

    def __init__(self, matr_path: str) -> None:
        """Initialize."""
        self.correct_matr = np.load(matr_path)

        i, j = np.where(self.correct_matr < 0)
        i, j = i[0], j[0]
        self.ngram_idx = (i, j)
        self.x_idx = range(i, self.correct_matr.shape[0])
        self.y_idx = range(j, self.correct_matr.shape[1])

        self.current_matr = self.correct_matr.copy()
        self.current_matr[self.correct_matr < 0] = -3
        self.size = np.count_nonzero(self.correct_matr == -1)

    def change_matr(self, i: int, j: int, button: int) -> None:
        """Change cell depending on button.

        :param i: i index of the cell to change
        :type i: int
        :param j: j index of the cell to change
        :type j: int
        :param button: mouse button type
        :type button: int
        """
        if not self.check():
            if i in self.x_idx and j in self.y_idx:
                if button == 1:  # left click
                    if self.current_matr[i][j] == -1:
                        self.current_matr[i][j] = -3
                    else:
                        self.current_matr[i][j] = -1
                elif button == 3:  # right click
                    if self.current_matr[i][j] == -2:
                        self.current_matr[i][j] = -3
                    else:
                        self.current_matr[i][j] = -2
            else:
                self.current_matr[i][j] = - self.current_matr[i][j]

    def check(self) -> bool:
        """Check if input matrix is correct.

        :param matr: matrix to check
        :type matr: np.ndarray
        :return: True if correct, otherwise False
        :rtype: bool
        """
        i, j = self.ngram_idx
        return np.equal(self.current_matr[i:, j:] == -1, self.correct_matr[i:, j:] == -1).all()

    def progress(self) -> float:
        """Get the progress.

        :rtype: float
        """
        i, j = self.ngram_idx
        match = np.count_nonzero(self.current_matr[i:, j:] == -1)
        return match / self.size
