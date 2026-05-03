import pygame

class CounterKill:
    def __init__(self, ai_game):
        """Initialize the counterkills settings"""
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.font = pygame.font.SysFont("Arial", 20, bold=True)

    def draw_counter(self):
        """Draw the counter on the screen"""
        text_surf = self.font.render(f"Eliminados: {self.settings.eliminate_sprites}", True, (0, 0, 0))
        text_rect = text_surf.get_rect()

        # Define the text right top
        text_rect.topright = (self.settings.screen_width -10, 10)
        self.screen.blit(text_surf, text_rect)