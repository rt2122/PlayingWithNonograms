"""Main program."""
import pygame
import pygame_gui
import os
from typing import Tuple
from . import (GameProcessor, Renderer, Page, ChoosingWindow, MenuButton, Nonogram,
               GameProgressBar, _)


class TestApp:
    """Class that runs program.

    :param window_size: Size of window.
    :type window_size: Tuple[int]
    """

    def __init__(self, window_size: Tuple[int]):
        """Initialize."""
        module_dir = os.path.dirname(__file__)

        pygame.init()
        pygame.display.set_caption(_("PWN"))
        self.window_size = window_size
        self.window_surface = pygame.display.set_mode(window_size)

        self.background = pygame.Surface(window_size)
        self.manager = pygame_gui.UIManager(window_size, os.path.join(module_dir, "./theme.json"))
        self.background.fill(self.manager.get_theme().get_colour("main", ["background", "colours"]))

        self.clock = pygame.time.Clock()
        self.is_running = True

        self.ngram_path = os.path.join(module_dir, "./ngrams")
        self.load_ngram(os.path.join(module_dir, "./ngrams/test.npy"))

        self.progress_bar = GameProgressBar(pygame.Rect((window_size[0] // 2 - 200, 100),
                                                        (400, 80)), self.manager, None,
                                    object_id=pygame_gui.core.ObjectID("#progress_bar_normal")) # noqa E128
        page1 = Page([MenuButton(window_size[0] // 2 - 75, window_size[1] // 2 - 100,
                                 _("Start Game"), self.manager, "choose"),
                      MenuButton(window_size[0] // 2 - 75, window_size[1] // 2, _("Exit"),
                                 self.manager, "exit")], active=True)
        page2 = Page([MenuButton(window_size[0] // 2 - 75, window_size[1] - 150, _("Back to menu"),
                                 self.manager,
                                 "page1"),
                      self.progress_bar, self.rend])
        self.pages = {"page1": page1, "page2": page2}
        self.page_display = page1

        self.progress_bar.percent_full = 0

    def load_ngram(self, path: str, reload_pages: bool = False, step: int = 60):
        """Load selected nonogram.

        :param path: Path of the nonogram.
        :type path: str
        :param reload_pages: Flag for reloading pages.
        :type reload_pages: bool
        :param step: Size of one cell in nonogram.
        :type step: int
        """
        self.ngram = Nonogram(path)
        ngram_shape = (self.ngram.current_matr.shape[0] * step,
                       self.ngram.current_matr.shape[1] * step)
        left = self.window_size[0] // 2 - ngram_shape[0] // 2
        top = self.window_size[1] // 2 - ngram_shape[1] // 2
        self.rend_sf = pygame.Surface(self.window_size)
        self.rend_sf.fill(self.manager.get_theme().get_colour("main", ["background", "colours"]))
        self.proc = GameProcessor(self.ngram.current_matr, left, top, step)
        self.rend = Renderer(self.rend_sf,
                             pygame.Rect(left, top, *ngram_shape),
                             self.ngram.current_matr.shape, self.manager, self.ngram.ngram_idx)
        self.rend.hide()
        if reload_pages:
            self.pages["page2"].buttons[-1] = self.rend

    def open_new_page(self, page_link: str) -> None:
        """Open page.

        :param page_link: Link to the page.
        :type page_link: str
        :rtype: None
        """
        if page_link is None:
            return
        if page_link == "exit":
            self.is_running = False
            return
        if page_link == "choose":
            window_size = (700, 500)
            w = ChoosingWindow(pygame.Rect((50, 50), window_size), self.manager, self.ngram_path)
            self.page_display.append(w.button_go)
            self.page_display.append(w)
            return

        if page_link == "page2":
            w = self.page_display.buttons[-1]
            selected = w.drop_down_menu.selected_option
            w.kill()
            self.load_ngram(os.path.join(self.ngram_path, selected), True)

        if page_link == "page1":
            self.progress_bar.win = False
            self.progress_bar.percent_full = 0
            self.rend.hide()

        self.page_display.hide_all()
        self.page_display = self.pages[page_link]
        self.page_display.show_all()

    def process_event(self, event):
        """Process game event.

        :param event: Event.
        """
        if self.rend.active:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if (cell := self.proc.click(*event.pos)):
                    self.ngram.change_matr(*cell, event.button)
                    progress = self.ngram.progress()
                    self.progress_bar.percent_full = min(100, progress * 100)
                    win = self.ngram.check()
                    if win:
                        self.progress_bar.bar_filled_colour = self.manager.get_theme().get_colour(
                                "filled_bar", ["#progress_bar_win", "colours"])
                        self.progress_bar.win = True
                    elif progress >= 1:
                        self.progress_bar.bar_filled_colour = self.manager.get_theme().get_colour(
                                "filled_bar", ["#progress_bar_defeat", "colours"])
                    else:
                        self.progress_bar.bar_filled_colour = self.manager.get_theme().get_colour(
                                "filled_bar", ["progress_bar", "colours"])
                    self.progress_bar.redraw()
                    return True

        handled = self.manager.process_events(event)
        if (event.type == pygame_gui.UI_BUTTON_PRESSED):
            for button in self.page_display.buttons:
                if event.ui_element == button:
                    self.open_new_page(button.next_page)
            handled = True

        return handled

    def run(self):
        """Run program."""
        while self.is_running:
            time_delta = self.clock.tick(60) / 1000.0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_running = False
                self.process_event(event)

            self.manager.update(time_delta)

            self.window_surface.blit(self.background, (0, 0))
            if self.rend.active:
                self.window_surface.blit(self.rend_sf, (0, 0))
            self.manager.draw_ui(self.window_surface)
            self.rend.render(self.ngram.current_matr)

            pygame.display.update()


if __name__ == "__main__":
    app = TestApp(window_size=(1920, 1080))
    app.run()
