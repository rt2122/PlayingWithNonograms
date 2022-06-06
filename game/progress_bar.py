"""Module for GameProgressBar."""
from pygame_gui.elements import UIProgressBar
from tr import _


class GameProgressBar(UIProgressBar):
    """GameProgressBar."""

    def status_text(self):
        """Return status text."""
        return _("YOU WON") if getattr(self, "win", False) else None
