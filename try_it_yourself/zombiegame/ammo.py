import pygame
from pygame.sprite import Sprite

class Ammo(Sprite):
    """A class to manage the ammo fired from the gun."""

    def __init__(self, ai_game):
        """Create an ammo object at the gun's current position."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.ammo_color

        # Create an ammo rect at (0, 0) and then set correct position
        self.rect = pygame.Rect(0, 0, self.settings.ammo_width,
                                self.settings.ammo_height)
        self.rect.midright = ai_game.gun.rect.midright

        # Store the ammo's position as a float.
        self.x = float(self.rect.x)

    def update(self):
        """Move the bullet right the screen."""
        # Update the exact position of the bullet.
        self.x += self.settings.ammo_speed
        # Update the rect position.
        self.rect.x = self.x

    def draw_ammo(self):
        """Draw the ammo to the screen."""
        pygame.draw.rect(self.screen, self.color, self.rect)