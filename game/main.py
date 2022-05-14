import pygame
import pygame_gui
import os
from typing import Tuple
from proc import GameProcessor
from render import Renderer
from screen import Page, ChoosingWindow, CheckResultWindow
from button import MenuButton
from ngram import Nonogram


class TestApp:
    def __init__(self, window_size: Tuple[int]):
        pygame.init()
        pygame.display.set_caption('PWN')
        self.window_size = window_size
        self.window_surface = pygame.display.set_mode(window_size)

        self.background = pygame.Surface(window_size)
        self.manager = pygame_gui.UIManager(window_size, "./theme.json")
        self.background.fill(self.manager.get_theme().get_colour("main", ["background", "colours"]))

        self.clock = pygame.time.Clock()
        self.is_running = True

        self.ngram_path = '../ngrams'
        self.load_ngram('../ngrams/test.npy')

        page1 = Page([MenuButton(window_size[0] // 2 - 75, window_size[1] // 2 - 100,
                                 "Start Game", self.manager, "choose"),
                      MenuButton(window_size[0] // 2 - 75, window_size[1] // 2, "Exit",
                                 self.manager, "exit")], active=True)
        page2 = Page([MenuButton(window_size[0] // 2 - 100 - 75, 10, "Back to menu", self.manager,
                                 "page1"),
                      MenuButton(window_size[0] // 2 + 100 - 75, 10, "Check", self.manager,
                                 "check"), self.rend])
        self.pages = {"page1": page1, "page2": page2}
        self.page_display = page1

    def load_ngram(self, path: str, reload_pages: bool = False, step: int = 60):
        self.ngram = Nonogram(path)
        ngram_shape = (self.ngram.current_matr.shape[0] * step,
                       self.ngram.current_matr.shape[1] * step)
        left = self.window_size[0] // 2 - ngram_shape[0] // 2 - 100
        top = self.window_size[1] // 2 - ngram_shape[1] // 2 - 100
        self.rend_sf = pygame.Surface(self.window_size)
        self.rend_sf.fill(self.manager.get_theme().get_colour("main", ["background", "colours"]))
        self.rend = Renderer(self.rend_sf,
                             pygame.Rect(left, top, *ngram_shape),
                             self.ngram.current_matr.shape, self.manager)
        self.proc = GameProcessor(self.ngram.current_matr, left + 100, top + 100, step)
        self.rend.hide()
        if reload_pages:
            self.pages['page2'].buttons[-1] = self.rend

    def open_new_page(self, page_link: str) -> None:
        if page_link is None:
            return
        if page_link == "exit":
            self.is_running = False
            return
        if page_link == "check":
            window_size = (260, 300)
            win = self.ngram.check()
            w = CheckResultWindow(win, pygame.Rect((50, 50), window_size), self.manager)
            if win:
                self.page_display.append(w.button)
            self.page_display.append(w)
            return
        if page_link == "choose":
            window_size = (700, 500)
            w = ChoosingWindow(pygame.Rect((50, 50), window_size), self.manager)
            self.page_display.append(w.button_go)
            self.page_display.append(w)
            return

        if page_link == "page2":
            w = self.page_display.buttons[-1]
            selected = w.drop_down_menu.selected_option
            w.kill()
            self.load_ngram(os.path.join(self.ngram_path, selected), True)

        if page_link == "page1_won":
            page_link = "page1"
            self.page_display.buttons[-1].kill()
            self.rend.hide()

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
            if self.rend.active:
                self.window_surface.blit(self.rend_sf, (95, 95))
            self.manager.draw_ui(self.window_surface)
            self.rend.render(self.ngram.current_matr)

            pygame.display.update()


if __name__ == '__main__':
    app = TestApp(window_size=(1920, 1080))
    app.run()
