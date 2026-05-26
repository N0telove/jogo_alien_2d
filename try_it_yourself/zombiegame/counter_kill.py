import pygame.font
from pygame.sprite import Group

from zombie import Zombie

class CounterKill:
    def __init__(self, ai_game):
        """Initialize the Scoreboard attributes."""
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats
        self.font = pygame.font.SysFont("Arial", 20, bold=True)
        self.text_color = (0, 0, 0) # Preto

        self.prep_images()

    def prep_images(self):
        self.prep_kills()
        self.prep_max_kill()
        self.prep_level()
        self.prep_life()
    

    def prep_kills(self):
        """Turn the score kills into a rendered image."""
        self.score_image = self.font.render(f"Score: {self.stats.eliminate_sprites}", True,
                self.text_color, self.settings.bg_screen)
        
        # Display the score at the top right of the screen.
        self.kills_rect = self.score_image.get_rect()
        self.kills_rect.right = self.screen_rect.right - 20
        self.kills_rect.top = 20

    def prep_level(self):
        """Turn the level into a rendered image."""
        level_str = str(self.stats.level)
        self.level_image = self.font.render(level_str, True,
                            self.text_color, self.settings.bg_screen)

        # Position the level below the score.
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.kills_rect.right
        self.level_rect.top = self.kills_rect.bottom + 10

    def prep_max_kill(self):
        """Turn the high score into a rendered image."""
        self.max_kills_image = self.font.render(f"Highest kills: {self.stats.max_kills}", True,
        self.text_color, self.settings.bg_screen)

        # Center the max kill at the top of the screen
        self.max_kills_rect = self.max_kills_image.get_rect()
        self.max_kills_rect.centerx = self.screen_rect.centerx
        self.max_kills_rect.top = self.screen_rect.top

    def check_highest_kills(self):
        """Check to see if there's a new max kills."""
        if self.stats.eliminate_sprites > self.stats.max_kills:
            self.stats.max_kills = self.stats.eliminate_sprites
            self.prep_max_kill()

    def prep_life(self):
        """Render the life image as zombies (it's called just when lives changes)"""
        self.zombies = Group()
        for zombie_number in range(self.stats.zombies_left):
            zombie = Zombie(self.ai_game)
            zombie.rect.x = 10 + zombie_number * zombie.rect.width
            zombie.rect.y = 10
            self.zombies.add(zombie)

    def draw_counter(self):
        """Draw kills score, zombies and level to the screen"""
        self.screen.blit(self.max_kills_image, self.max_kills_rect)
        self.screen.blit(self.score_image, self.kills_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.zombies.draw(self.screen)
