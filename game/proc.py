import numpy as np
from typing import Tuple


class GameProcessor():
    """
    Class responsible for converting user clicks to changed cells on a nonogram grid.

    :param matrix: Initial matrix that represents a nonogram
    :type matrix: np.ndarray
    :param left: left indent of the nonogram rectangle on the screen
    :type left: int
    :param top: top indent of the nonogram rectangle on the screen
    :type top: int
    :param step: one cell width
    :type step: int
    """
    def __init__(self, matrix: np.ndarray, left: int, top: int, step: int) -> None:
        """
        Constructor.
        """
        self.matr = matrix.copy()
        i, j = np.where(matrix < 0)
        i, j = i[0], j[0]
        self.x_idx = range(i, matrix.shape[0])
        self.y_idx = range(j, matrix.shape[1])
        self.step = step
        self.left = left
        self.top = top

    def click(self, x: int, y: int) -> Tuple[int, int] or None:
        """
        If clicked on a cell return its indices, else return None.

        :param x: x coordinate of a mouseclick
        :type x: int
        :param y: y coordinate of a mouseclick
        :type y: int
        :return: Tuple of cell indicies if clicked on a cell, else return None
        :rtype: Tuple[int, int] or None
        """
        i = (x - self.left) // self.step
        j = (y - self.top) // self.step
        if i in self.x_idx and j in self.y_idx:
            return i, j
        return None
