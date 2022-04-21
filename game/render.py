import pygame
import numpy as np
from typing import Tuple


class Renderer:
    """
    -1  ==  Black square
    -2  ==  X
    -3  ==  White square
    """
    def __init__(self, surface: pygame.Surface, bkg_rect: pygame.Rect, matr_shape: Tuple[int]):
        """
        Initialize Renderer object. bkg_rect - rectangle, in which all picture will be inscribed.
        matr_shape - shape of the matrix (including hint numbers).
        """
        self.surface = surface
        self.bkg_color = pygame.Color("#93c28a")
        self.field_color = pygame.Color("#dbc26e")
        self.line_color = pygame.Color("#000000")
        self.dark_square_color = pygame.Color("#383838")
        self.x_color = pygame.Color("#7d7d7d")
        self.bkg_rect = bkg_rect
        self.matr_shape = matr_shape

        self.x_step = bkg_rect.width // matr_shape[0]
        self.y_step = bkg_rect.height // matr_shape[1]

        pygame.font.init()
        self.printer = pygame.font.SysFont('Comic Sans MS', self.y_step)

        self.line_width = 5
        self.active = True

    def hide(self):
        self.active = False

    def show(self):
        self.active = True

    def get_cell_rect(self, i: int, j: int) -> pygame.Rect:
        """
        Get pygame.Rect object for matr[i,j].
        """
        left = self.bkg_rect.left + i * self.x_step
        top = self.bkg_rect.top + j * self.y_step
        return pygame.Rect(left, top, self.x_step, self.y_step)

    def render(self, matr: np.ndarray) -> None:
        """
        Render given matrix.
        """

        if not self.active:
            return

        # Draw background
        pygame.draw.rect(self.surface, self.bkg_color, self.bkg_rect)
        # Draw field
        i, j = np.where(matr < 0)
        i, j = i[0], j[0]
        left = self.bkg_rect.left + i * self.x_step
        top = self.bkg_rect.top + j * self.y_step
        width = self.bkg_rect.width - i * self.x_step
        height = self.bkg_rect.height - j * self.y_step
        field_rect = pygame.Rect(left, top, width, height)
        pygame.draw.rect(self.surface, self.field_color, field_rect)

        corner_rect = pygame.Rect(self.bkg_rect.left, self.bkg_rect.top,
                                  i * self.x_step, j * self.y_step)
        pygame.draw.rect(self.surface, self.x_color, corner_rect)

        # Draw numbers, squares and x's
        for i in range(self.matr_shape[0]):
            for j in range(self.matr_shape[1]):
                cell = self.get_cell_rect(i, j)
                val = matr[i, j]
                if val > 0:  # Number
                    text = self.printer.render(str(val), True, self.line_color)
                    center = (cell.left + cell.right) / 2, (cell.top + cell.bottom) / 2
                    coords = text.get_rect(center=center)
                    self.surface.blit(text, coords)
                elif val == -1:  # Black square
                    pygame.draw.rect(self.surface, self.dark_square_color, cell)
                elif val == -2:  # X
                    pygame.draw.line(self.surface, self.x_color,
                                     (cell.left, cell.top), (cell.right, cell.bottom),
                                     width=self.line_width)
                    pygame.draw.line(self.surface, self.x_color,
                                     (cell.left, cell.bottom), (cell.right, cell.top),
                                     width=self.line_width)

        # Draw grid
        # Vertical lines
        for i in range(self.matr_shape[0] + 1):
            start_cell = self.get_cell_rect(0, i)
            end_cell = self.get_cell_rect(self.matr_shape[1], i)
            start = (start_cell.top, start_cell.left)
            end = (end_cell.top, end_cell.left)
            pygame.draw.line(self.surface, self.line_color, start, end, width=self.line_width)
        # Horizontal lines
        for i in range(self.matr_shape[1] + 1):
            start_cell = self.get_cell_rect(i, 0)
            end_cell = self.get_cell_rect(i, self.matr_shape[0])
            start = (start_cell.top, start_cell.left)
            end = (end_cell.top, end_cell.left)
            pygame.draw.line(self.surface, self.line_color, start, end, width=self.line_width)
