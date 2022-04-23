from typing import List


class Page:
    """
    Page class. Contains objects with methods show() and hide().

    :param buttons: Objects of this page.
    :type buttons: List
    :param active: If page should be active from the start.
    :type active: bool
    """

    def __init__(self, buttons: List, active: bool = False):
        """
        Constructor.
        """
        self.buttons = buttons
        if not active:
            self.hide_all()

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
