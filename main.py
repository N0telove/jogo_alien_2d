import sys
import pygame

# In Alien Invasion, the player controls a rocket ship that appears
# at the bottom center of the screen. The player can move the ship
# right and left using the arrow keys and shoot bullets using the
# spacebar. When the game begins, a fleet of aliens fills the sky
# and moves across and down the screen. The player shoots and
# destroys the aliens. If the player destroys all the aliens, a new fleet
# appears that moves faster than the previous fleet. If any alien hits
# the player’s ship or reaches the bottom of the screen, the player
# loses a ship. If the player loses three ships, the game ends.

# first development phase

class AlienInvasion:
    """Overall class to manage game assets and behavior."""

    def __init__(self):
        """Initialize the game, and create game resources."""
        pygame.init()

        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((1200, 800))
        pygame.display.set_caption("Alien Invasion")

        self.bg_color = (230, 230, 230)

    def run_game(self):
        """Start the main loop for the game."""
        while True:
            # Watch for keyboard and mouse events.
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            # Redraw the screen during each pass through the loop.
            self.screen.fill(self.bg_color)

            # Make the most recently drawn screen visible.
            pygame.display.flip()
            self.clock.tick(60)

if __name__ == "__main__":
    # Make a instance, and run the game.
    ai = AlienInvasion()
    ai.run_game()