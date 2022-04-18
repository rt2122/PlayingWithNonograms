import pygame_gui
import pygame


class MenuButton(pygame_gui.elements.UIButton):
    """
    Class representing a menu button.

    :param top: top indent
    :type top: int
    :param text: text
    :type text: str
    :param manager: gui manager
    :type manager: pygame_gui.UIManager
    :param next_page: page to show after this button is pressed
    :type next_page: str
    """
    def __init__(self, top: int, text: str, manager: pygame_gui.UIManager, next_page: str) -> None:
        super().__init__(relative_rect=pygame.Rect((350, top), (100, 50)),
                         text=text, manager=manager,
                         object_id=pygame_gui.core.ObjectID(class_id='@menu_buttons'))
        self.next_page = next_page
