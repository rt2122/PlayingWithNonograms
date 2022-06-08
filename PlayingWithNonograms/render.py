"""Module for Renderer class."""
import pygame
import pygame_gui
import numpy as np
from typing import Tuple


class Renderer:
    """
    Class that renders given nonogram matrix.

    :param surface: Where to render.
    :type surface: pygame.Surface
    :param bkg_rect: Rectangle, in which matrix will be inscribed.
    :type bkg_rect: pygame.Rect
    :param matr_shape: Shape of the nonogram matrix (including hints).
    :type matr_shape: Tuple[int]
    :param manager: Manager (to get colours).
    :type manager: pygame_gui.UIManager
    :param ngram_idx: Indexes of left upper corner of nonogram in the matrix.
    :type ngram_idx: Tuple[int]
    """

    def __init__(self, surface: pygame.Surface, bkg_rect: pygame.Rect, matr_shape: Tuple[int],
                 manager: pygame_gui.UIManager, ngram_idx: Tuple[int]):
        """Initialize."""
        self.surface = surface
        theme = manager.get_theme()
        colour_types = ["bkg_color", "field_color", "line_color", "dark_square_color", "x_color"]
        for ctype in colour_types:
            self.__setattr__(ctype, theme.get_colour(ctype, ["renderer", "colours"]))
        self.bkg_rect = bkg_rect
        self.matr_shape = matr_shape

        self.x_step = bkg_rect.width // matr_shape[0]
        self.y_step = bkg_rect.height // matr_shape[1]

        pygame.font.init()
        self.printer = pygame.font.SysFont('Comic Sans MS', self.y_step)

        self.line_width = int(theme.get_misc_data("line_width", ["renderer"]))
        self.active = True
        self.ngram_idx = ngram_idx

    def hide(self):
        """Make renderer inactive."""
        self.active = False

    def show(self):
        """Make renderer active."""
        self.active = True

    def get_cell_rect(self, i: int, j: int) -> pygame.Rect:
        """Get rectangle for cell by its coordinates.

        :param i: Row index.
        :type i: int
        :param j: Columns index.
        :type j: int
        :rtype: pygame.Rect
        """
        left = self.bkg_rect.left + i * self.x_step
        top = self.bkg_rect.top + j * self.y_step
        return pygame.Rect(left, top, self.x_step, self.y_step)

    def render(self, matr: np.ndarray) -> None:
        """Render matrix.

        If number is < 0, then it means:

        - -1 Black square
        - -2 X
        - -3 White square

        :param matr: Given matrix.
        :type matr: np.ndarray
        :rtype: None
        """
        # Draw background
        pygame.draw.rect(self.surface, self.bkg_color, self.bkg_rect)
        # Draw field
        ngram_i, ngram_j = self.ngram_idx
        left = self.bkg_rect.left + ngram_i * self.x_step
        top = self.bkg_rect.top + ngram_j * self.y_step
        width = self.bkg_rect.width - ngram_i * self.x_step
        height = self.bkg_rect.height - ngram_j * self.y_step
        field_rect = pygame.Rect(left, top, width, height)
        pygame.draw.rect(self.surface, self.field_color, field_rect)

        corner_rect = pygame.Rect(self.bkg_rect.left, self.bkg_rect.top,
                                  ngram_i * self.x_step, ngram_j * self.y_step)
        pygame.draw.rect(self.surface, self.x_color, corner_rect)

        # Draw numbers, squares and x's
        for i in range(self.matr_shape[0]):
            for j in range(self.matr_shape[1]):
                cell = self.get_cell_rect(i, j)
                val = matr[i, j]
                crossed = False
                if (i < ngram_i or j < ngram_j) and val != 0:  # Number
                    crossed = val < 0
                    val = abs(val)
                    text = self.printer.render(str(val), True, self.line_color)
                    center = (cell.left + cell.right) / 2, (cell.top + cell.bottom) / 2
                    coords = text.get_rect(center=center)
                    self.surface.blit(text, coords)
                elif val == -1:  # Black square
                    pygame.draw.rect(self.surface, self.dark_square_color, cell)

                if val == -2 or crossed:  # X
                    pygame.draw.line(self.surface, self.x_color,
                                     (cell.left, cell.top), (cell.right, cell.bottom),
                                     width=self.line_width)
                    pygame.draw.line(self.surface, self.x_color,
                                     (cell.left, cell.bottom), (cell.right, cell.top),
                                     width=self.line_width)

        # Draw grid
        # Vertical lines
        for i in range(self.matr_shape[1] + 1):
            start_cell = self.get_cell_rect(0, i)
            end_cell = self.get_cell_rect(self.matr_shape[0], i)
            start = (start_cell.left, start_cell.top)
            end = (end_cell.left, end_cell.top)
            pygame.draw.line(self.surface, self.line_color, start, end, width=self.line_width)
        # Horizontal lines
        for i in range(self.matr_shape[0] + 1):
            start_cell = self.get_cell_rect(i, 0)
            end_cell = self.get_cell_rect(i, self.matr_shape[1])
            start = (start_cell.left, start_cell.top)
            end = (end_cell.left, end_cell.top)
            pygame.draw.line(self.surface, self.line_color, start, end, width=self.line_width)
