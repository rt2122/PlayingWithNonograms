from typing import List
import os
import pygame
import pygame_gui
from pygame_gui.elements import UIWindow, UIDropDownMenu, UILabel
from button import MenuButton, GoButton


class ChoosingWindow(UIWindow):
    """
    Window with drop down menu which allows to choose nonogram from list.

    :param rect: Rectangle in which window would be inscribed.
    :type rect: pygame.Rect
    :param ui_manager: UIManager for window.
    :type ui_manager: pygame_gui.UIManager
    """

    def __init__(self, rect: pygame.Rect, ui_manager: pygame_gui.UIManager) -> None:
        """
        Constructor.
        """
        super().__init__(rect, ui_manager,
                         window_display_title='Choose Nonogram',
                         object_id='#scaling_window',
                         resizable=True)

        ngram_path = '../ngrams'
        files = os.listdir(ngram_path)
        files = list(filter(lambda x: x.endswith('.npy'), files))

        current_ngram = files[0]
        self.drop_down_menu = UIDropDownMenu(files, current_ngram,
                                             pygame.Rect((int(self.rect.width / 2),
                                                          int(self.rect.height * 0.3)), (200, 25)),
                                             self.ui_manager, container=self)
        self.button_go = GoButton(50, 50, "Go!", ui_manager, "page2", self)

        self.set_blocking(True)


class CheckResultWindow(UIWindow):
    """ Window that appears after pressing \"check\" button and shows the result.

    :param win: if the user won or not
    :type win: bool
    :param rect: Rectangle in which window would be inscribed.
    :type rect: pygame.Rect
    :param manager: UIManager for window.
    :type manager: pygame_gui.UIManager
    """
    def __init__(self, win: bool, rect: pygame.Rect, manager: pygame_gui.UIManager) -> None:
        """
        Constructor.
        """
        super().__init__(rect, manager, "", object_id='#scaling_window', resizable=False)

        text = "YOU WON" if win else "YOU LOST"
        btn_text = "To main menu" if win else "Back to puzzle"

        self.text = UILabel(pygame.Rect((50, 50), (200, 50)), text, manager, container=self)
        if win:
            self.button = GoButton(50, 100, btn_text, manager, "page1_won", self)

        self.set_blocking(True)


class Page:
    """
    Page class. Contains objects with methods show() and hide().

    :param buttons: Objects of this page.
    :type buttons: List
    :param active: If page should be active from the start.
    :type active: bool
    """

    def __init__(self, buttons: List, active: bool = False) -> None:
        """
        Constructor.
        """
        self.buttons = buttons
        if not active:
            self.hide_all()

    def append(self, new_obj) -> None:
        """append.

        :param new_obj: Object to add to list of components of this page.
        """
        self.buttons.append(new_obj)

    def hide_all(self) -> None:
        """
        Disable all objects on the page.
        :rtype: None
        """
        for button in self.buttons:
            button.hide()

    def show_all(self) -> None:
        """
        Show all objects on the page.
        :rtype: None
        """
        for button in self.buttons:
            button.show()
