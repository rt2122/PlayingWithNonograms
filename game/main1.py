import os
import numpy as np
import pygame
import pygame_gui
from typing import Tuple
from ngram import Nonogram
from render import Renderer
from proc import GameProcessor
from button import MenuButton
from screen import ChoosingWindow, CheckResultWindow


class TestApp:
    def __init__(self, window_size: Tuple[int]):
        pygame.init()
        pygame.display.set_caption('PWN')
        self.window_size = window_size
        self.window_surface = pygame.display.set_mode(window_size)

        self.background = pygame.Surface(window_size)
        self.background.fill(pygame.Color('#4B88A2'))
        self.manager = pygame_gui.UIManager(window_size, "./theme.json")

        self.clock = pygame.time.Clock()
        self.is_running = True

        self.ngram_path = '../ngrams'
        self.load_ngram('../ngrams/test.npy')
        self.buttons = [MenuButton(100, 10, "Exit", self.manager, "exit"),
                        MenuButton(300, 10, "Check", self.manager, "check"), self.rend]

        self.progress_bar = pygame_gui.elements.UIStatusBar(pygame.Rect((500, 10), (200, 50)),
                                                            self.manager, None,
                                            object_id=pygame_gui.core.ObjectID('#progress_bar'))
        self.progress_bar.percent_full = 0
        self.choosing = ChoosingWindow(pygame.Rect((50, 50), np.array(window_size) / 2), self.manager)

    def process_event(self, event):
        if self.rend.active:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if cell := self.proc.click(*event.pos):
                    self.ngram.change_matr(self.proc.change_cell(*cell, event.button))
                    return True

        handled = self.manager.process_events(event)

        if (event.type == pygame_gui.UI_BUTTON_PRESSED):
            for button in self.buttons + [self.choosing.button_go]:
                if event.ui_element == button:
                    if button.next_page == 'exit':
                        self.is_running = False
                    elif button.next_page == 'check':
                        progress = self.ngram.progress()
                        self.progress_bar.percent_full = progress * 100
                    elif button.next_page == 'go':
                        selected = self.choosing.drop_down_menu.selected_option
                        self.choosing.kill()
                        self.load_ngram(os.path.join(self.ngram_path, selected), True)
                        self.rend.show()

        handled = True
        return handled

    def load_ngram(self, path: str, reload_pages: bool = False):
        self.ngram = Nonogram(path)
        step = 60
        left = top = 100
        self.rend_sf = pygame.Surface((self.ngram.current_matr.shape[0] * step + 10,
                                       self.ngram.current_matr.shape[1] * step + 10))
        self.rend_sf.fill(pygame.Color('#4B88A2'))
        self.rend = Renderer(self.rend_sf,
                             pygame.Rect(5, 5, self.ngram.current_matr.shape[0] * step,
                                         self.ngram.current_matr.shape[1] * step),
                             self.ngram.current_matr.shape)
        self.rend.hide()
        self.proc = GameProcessor(self.ngram.current_matr, left, top, step)

    def run(self):
        while self.is_running:
            time_delta = self.clock.tick(60) / 1000.0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_running = False
                self.process_event(event)

            self.manager.update(time_delta)

            self.window_surface.blit(self.background, (0, 0))
            if self.rend.active:
                self.window_surface.blit(self.rend_sf, (95, 95))
            self.manager.draw_ui(self.window_surface)
            self.rend.render(self.ngram.current_matr)

            pygame.display.update()


if __name__ == '__main__':
    app = TestApp(window_size=(1200, 720))
    app.run()
