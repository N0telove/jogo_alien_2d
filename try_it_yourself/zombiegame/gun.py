import pygame
from pygame.sprite import Sprite
from pathlib import Path

class Gun(Sprite):
    """A class to manage the zombie weapon."""

    def __init__(self, ai_game):
        """Initialize the ship and set its starting position."""
        super().__init__()
        self.screen = ai_game.screen

        # Load the image and make some adjustments
        #self.image = pygame.image.load(r"C:\Users\rh.agriter\Desktop\eu\codigos\python_crash_course\jogo_alien_2d\try_it_yourself\bmpfiles\ak-47-gun.bmp")
        self.image = pygame.image.load(Path().cwd() / Path("try_it_yourself/zombiegame/bmpfiles/ak-47-gun.bmp"))

        self.image.set_colorkey((255, 255, 255))
        self.image = pygame.transform.scale(self.image, (60, 60))

        # Get the image shape
        self.rect = self.image.get_rect()

    def update(self, pos_zombie):
        # Set the X and Y distance from zombie's hand
        self.rect.centerx = pos_zombie.centerx + 21
        self.rect.centery = pos_zombie.centery + 17

    def blit_gun(self):
        """Draw the gun to the screen."""
        self.screen.blit(self.image, self.rect)