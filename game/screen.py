import pygame_gui
import pygame

from button import MenuButton
from typing import List


class Page:
    def __init__(self, buttons: List[MenuButton], active=False):
        self.buttons = buttons
        if not active:
            self.hide_all()

    def hide_all(self) -> None:
        for button in self.buttons:
            button.hide()

    def show_all(self) -> None:
        for button in self.buttons:
            button.show()


class TestApp:
    def __init__(self):
        pygame.init()

        pygame.display.set_caption('PWN')
        self.window_surface = pygame.display.set_mode((800, 600))

        self.background = pygame.Surface((800, 600))
        self.background.fill(pygame.Color('#15438c'))
        self.manager = pygame_gui.UIManager((800, 600), "./theme.json")

        self.clock = pygame.time.Clock()
        self.is_running = True

        page1 = Page([MenuButton(100, "Start Game", self.manager, "page2"),
                     MenuButton(150, "Exit", self.manager, "exit")], active=True)
        page2 = Page([MenuButton(200, "Something will be here", self.manager, "page1")])
        self.pages = {"page1": page1, "page2": page2}
        self.page_display = page1

    def open_new_page(self, page_link: str):
        if page_link is None:
            return
        if page_link == "exit":
            self.is_running = False
            return
        self.page_display.hide_all()
        self.page_display = self.pages[page_link]
        self.page_display.show_all()

    def process_event(self, event):
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

            pygame.display.update()


if __name__ == '__main__':
    app = TestApp()
    app.run()
