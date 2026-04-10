import pygame
import sys
from configuration import ScreenSettings
from zombie import Zombie

class Game:
    """Initialize the Zombie game."""

    def __init__(self):
        """Initialize the game, and create game resources."""
        pygame.init()
        self.settings = ScreenSettings()
        if self.settings.mode == 1:
            self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        else:
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
            self.settings.screen_width = self.screen.get_rect().width
            self.settings.screen_height = self.screen.get_rect().height
        self.clock = pygame.time.Clock()

        pygame.display.set_caption("I'm a Zombieee, i'll bite you...")

        self.zombie = Zombie(self)

    def run_game(self):
        """Initialize the game."""
        while True:
            self._check_events()
            self.zombie.update()
            self._update_screen()
            self.clock.tick(60)

    def _check_events(self):
        """Respond to keypresses and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            
            # Move the Zombie 
            elif event.type == pygame.KEYUP:
                self._check_presses_event(event)

            # Stop moving the Zombie
            elif event.type == pygame.KEYDOWN:
                self._check_releases_event(event)

    def _check_presses_event(self, event):
        """Respond to keypresses."""
        if event.key == pygame.K_RIGHT:
            self.zombie.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.zombie.moving_left = True
        elif event.key == pygame.K_UP:
            self.zombie.moving_up =True
        elif event.key == pygame.K_DOWN:
            self.zombie.moving_down = True
        elif event.key == pygame.K_q:
            sys.exit()

    def _check_releases_event(self, event):
        """Respond to key releases."""
        if event.key == pygame.K_RIGHT:
            self.zombie.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.zombie.moving_left = False
        elif event.key == pygame.K_UP:
            self.zombie.moving_up = False
        elif event.key == pygame.K_DOWN:
            self.zombie.moving_down = False

    def _update_screen(self):
        """Update the image"""
        self.screen.fill(self.settings.bg_screen)
        self.zombie.blitme()

        pygame.display.flip()


if __name__ == "__main__":
    # Make a instance and run the game
    main = Game()
    main.run_game()