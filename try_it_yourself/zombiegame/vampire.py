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
        self.image.set_colorkey((255, 255, 255))
        self.image = pygame.transform.scale(self.image, (70, 70))
        self.rect = self.image.get_rect()

        # Start each new vammpire near the top left of the screen
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Store the vampire's exact horizontal position
        self.x = float(self.rect.x)


    def check_edges(self):
        """Return True if vampire is at the edge of screen."""
        screen_rect = self.screen.get_rect()
        return (self.rect.top >= screen_rect.height) or (self.rect.bottom >= 0)


    def update(self):
        """Move the vampire right or left."""
        self.x -= self.settings.vampire_speed
