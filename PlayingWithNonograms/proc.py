"""Module for GameProcessor class."""
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
        """Initialize."""
        self.matr = matrix.copy()
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
        if i in range(self.matr.shape[0]) and j in range(self.matr.shape[1]):
            return i, j
        return None
