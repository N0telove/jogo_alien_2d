import pygame.font

class Label:
    """Create labels for the input boxes"""
    def __init__(self, ai_game, msg, position):
        """Initialize label attributes."""
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.msg = msg
        self.position = position
        self.box_color = (0, 0, 0)
        self.rect = pygame.Rect(0, 0, 120, 50)
        self.rect.center = position
        self.font = pygame.font.SysFont(None, 48)
        self.msg_image = self.font.render(msg, True, (255, 255, 255),
                self.box_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.topleft = self.position

    def draw_label(self):
        """Draw blank button and then draw message."""
        self.screen.fill(self.box_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)