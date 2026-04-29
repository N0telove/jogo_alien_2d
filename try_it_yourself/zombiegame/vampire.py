import pygame
from pygame.sprite import Sprite
from pathlib import Path

class Vampire(Sprite):
    """A class to represent a single vampire in the fleet."""

    def __init__(self, ai_game):
        """Initialize the vampire and set its starting position."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        # Load the vampire image and set its rect atribute
        self.image = pygame.image.load(Path().cwd() / Path("try_it_yourself/zombiegame/bmpfiles/vampire.bmp"))