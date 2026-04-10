import pygame

class Zombie:
    """initialize the main character and set his initial position."""
    def __init__(self, ai_game):
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.settings = ai_game.settings

        # Load the image and gets its rect
        self.image = pygame.image.load("try_it_yourself/bmpfiles/Zombie.bmp")
        self.rect = self.image.get_rect()

        # Start each new Zombie at the bottom center of the screen
        self.rect.midbottom = self.screen_rect.midbottom

        # Stores a float for the zombie's exact horizontal and vertical position.
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

        # Movement flags
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False

    def update(self):
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x -= self.settings.zombie_speed
        if self.moving_left and self.rect.left > 0:
            self.x += self.settings.zombie_speed
        if self.moving_up and self.rect.top < 0:
            self.y += self.settings.zombie_speed
        if self.moving_down and self.rect.bottom > self.screen_rect.bottom:
            self.y -= self.settings.zombie_speed

        # Update rect object from self.x and self.y.
        self.rect.x = self.x
        self.rect.y = self.y

    def blitme(self):
        """Draw the Zombie at his current location."""
        self.screen.blit(self.image, self.rect)