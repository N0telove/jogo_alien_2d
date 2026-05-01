import pygame
from pygame.sprite import Sprite
from pathlib import Path
from random import randint, choice

class Vampire(Sprite):
    """A class to represent a single vampire in the fleet."""

    def __init__(self, ai_game):
        """Initialize the vampire and set its starting position."""
        super().__init__()
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.settings = ai_game.settings

        # Load the vampire image and set its rect atribute
        self.image = pygame.image.load(Path().cwd() / Path("try_it_yourself/zombiegame/bmpfiles/vampire.bmp"))
        self.image.set_colorkey((255, 255, 255))
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()

        # Start each new vampire near the top right of the screen
        self.rect.midright = self.screen_rect.midright

        # Store the vampire's exact horizontal and vertical position
        self.y = float(self.rect.y)
        self.x = float(self.rect.x)

        # Vertical movement: 1 = down, -1 = up
        self.vertical_direction = choice([-1, 1])
        # Random speed variation for natural movement
        self.speed_variation = randint(0, 100) / 100.0  # 0.0 to 1.0


    def check_edges(self):
        """Return True if vampire is at the edge of screen."""
        screen_rect = self.screen.get_rect()
        return (self.rect.top <= 0) or (self.rect.bottom >= screen_rect.height)


    def update(self):
        """Move the vampire vertically with random variation."""
        # Calculate speed with variation
        base_speed = self.settings.vampire_speed
        speed = base_speed * (0.5 + self.speed_variation)
        
        # Move vertically and horizontally
        self.x -= speed
        self.rect.x = self.x
        self.y += speed * self.vertical_direction
        self.rect.y = self.y
        
        # Keep within screen bounds
        if self.rect.top <= 0:
            self.rect.top = 0
            self.y = float(self.rect.y)
            self.vertical_direction = 1  # Change to down
        elif self.rect.bottom >= self.screen_rect.height:
            self.rect.bottom = self.screen_rect.height
            self.y = float(self.rect.y)
            self.vertical_direction = -1  # Change to up
        
        # Random direction change (small chance)
        if randint(0, 100) < 2:  # 2% chance to change direction
            self.vertical_direction *= -1
