import pygame
import sys

class Game:
    """Initialize the Zombie game."""

    def __init__(self):
        pygame.init()

        self.clock = pygame.time.Clock()
        self.settings = ScreenSettings()
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
    
        self.zombie = Zombie(self)

    def run_game(self):
        """Initialize the game."""
        while True:
            self._check_events()
            self._update_screen()
            self.clock.tick(60)

    def _check_events(self):
        """Respond to keypresses and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

    def _update_screen(self):
        """Update the image"""
        self.screen.fill(self.settings.bg_screen)
        
        pygame.display.flip()

class ScreenSettings:
    """Set screen settings"""

    def __init__(self):
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_screen = (220, 220, 220)

class Zombie:
    """initialize the main character and set his initial position."""
    def __init__(self, ai_game):
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()

        # Load the image and gets its rect
        self.image = pygame.image.load("try_it_yourself/bmpfiles/Zombie.bmp")
        self.rect = self.image.get_rect()

        # Start each new Zombie at the bottom center of the screen
        self.rect.midbottom = self.screen_rect.midbottom

    def blitme(self):
        """Draw the Zombie at his current location."""
        self.screen.blit(self.image, self.rect)


if __name__ == "__main__":
    # Make a instance and run the game
    sky = Game()
    sky.run_game()