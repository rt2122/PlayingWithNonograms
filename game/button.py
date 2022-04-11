import pygame_gui
import pygame


class MenuButton(pygame_gui.elements.UIButton):
    def __init__(self, top, text, manager) -> None:
        return super().__init__(relative_rect=pygame.Rect((350, top), (100, 50)),
                                text=text,
                                manager=manager,
                                object_id=pygame_gui.core.ObjectID(class_id='@menu_buttons'))
