import pygame
import pygame_gui
from typing import Tuple
from proc import GameProcessor
from render import Renderer
from screen import Page
from button import MenuButton
from ngram import Nonogram


class TestApp:
    def __init__(self, window_size: Tuple[int]):
        pygame.init()
        pygame.display.set_caption('PWN')
        self.window_surface = pygame.display.set_mode(window_size)

        self.background = pygame.Surface(window_size)
        self.background.fill(pygame.Color('#15438c'))
        self.manager = pygame_gui.UIManager(window_size, "./theme.json")

        self.clock = pygame.time.Clock()
        self.is_running = True

        self.ngram = Nonogram('../ngrams/test.npy')
        step = 60
        left = top = 100
        self.rend = Renderer(self.window_surface,
                             pygame.Rect(left, top, self.ngram.current_matr.shape[0] * step,
                                         self.ngram.current_matr.shape[1] * step),
                             self.ngram.current_matr.shape)
        self.proc = GameProcessor(self.ngram.current_matr, left, top, step)
        self.rend.hide()

        page1 = Page([MenuButton(100, 100, "Start Game", self.manager, "page2"),
                     MenuButton(150, 100, "Exit", self.manager, "exit")], active=True)
        page2 = Page([MenuButton(10, 100, "Back to menu", self.manager, "page1"),
                      MenuButton(10, 300, "Check", self.manager, "check"), self.rend])
        self.pages = {"page1": page1, "page2": page2}
        self.page_display = page1

    def open_new_page(self, page_link: str):
        if page_link is None:
            return
        if page_link == "exit":
            self.is_running = False
            return
        if page_link == "check":
            if self.ngram.check():
                page_link = "page1"
            else:
                return
        self.page_display.hide_all()
        self.page_display = self.pages[page_link]
        self.page_display.show_all()

    def process_event(self, event):
        if self.rend.active:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if cell := self.proc.click(*event.pos):
                    self.ngram.change_matr(self.proc.change_cell(*cell, event.button))
                    return True

        handled = self.manager.process_events(event)
        if (event.type == pygame_gui.UI_BUTTON_PRESSED):
            for button in self.page_display.buttons:
                if event.ui_element == button:
                    self.open_new_page(button.next_page)
            handled = True

        return handled

    def run(self):
        while self.is_running:
            time_delta = self.clock.tick(60) / 1000.0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_running = False
                self.process_event(event)

            self.manager.update(time_delta)

            self.window_surface.blit(self.background, (0, 0))
            self.manager.draw_ui(self.window_surface)
            self.rend.render(self.ngram.current_matr)

            pygame.display.update()


if __name__ == '__main__':
    app = TestApp(window_size=(1200, 720))
    app.run()
