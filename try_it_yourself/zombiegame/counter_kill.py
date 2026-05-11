import pygame

class CounterKill:
    def __init__(self, ai_game):
        """Initialize the counterkills settings"""
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.stats = ai_game.stats
        self.font = pygame.font.SysFont("Arial", 20, bold=True)
        self.text_color = (0, 0, 0) # Preto

        self.life_surf = None
        self.life_rect = None
        self.render_life()

    def render_life(self):
        """Render the life image (it's called just when lives changes)"""
        self.text_life = f"Lives: {self.stats.zombies_left}"
        self.life_surf = self.font.render(self.text_life, True, self.text_color)
        self.life_rect = self.life_surf.get_rect()

        #  Define the text bellow kills counter
        self.life_rect.topright = (self.settings.screen_width - 10, 40)

    def draw_counter(self):
        """Draw the counter on the screen"""
        # First: draw the lives counter, that it's already pre-render
        self.screen.blit(self.life_surf, self.life_rect)


        # now draws <p>: kills (changes constantly)
        text_kill = f"Kills: {self.stats.eliminate_sprites}"
        kill_surf = self.font.render(text_kill, True, self.text_color)
        kill_rect = kill_surf.get_rect()

        # Define the text right top
        kill_rect.topright = (self.settings.screen_width -10, 10)
        self.screen.blit(kill_surf, kill_rect)
