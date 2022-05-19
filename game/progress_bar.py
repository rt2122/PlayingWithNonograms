from pygame_gui.elements import UIProgressBar


class GameProgressBar(UIProgressBar):
    def status_text(self):
        return "YOU WON" if getattr(self, "win", False) else None
