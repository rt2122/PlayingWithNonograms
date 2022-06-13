import PlayingWithNonograms.progress_bar
import pygame_gui
import pygame

ws = (1920, 1080)
pygame.init()
manager = pygame_gui.UIManager(ws)


def test_win():
    pb = PlayingWithNonograms.progress_bar.GameProgressBar(pygame.Rect(0, 0, 0, 0), manager)
    pb.win = True
    assert pb.status_text()


def test_lose():
    pb = PlayingWithNonograms.progress_bar.GameProgressBar(pygame.Rect(0, 0, 0, 0), manager)
    assert not pb.status_text()
