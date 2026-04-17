import pygame
from configuration import ScreenSettings
from pygame.sprite import Sprite
import sys
import random


class Sky():
    def __init__(self):
        """Initialize the game."""
        pygame.init()
        self.settings = ScreenSettings()
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        self.clock = pygame.time.Clock()

        self.stars = pygame.sprite.Group()
        self._create_skyfull()

    def run_game(self):
        while True:
            self._check_events()
            self._update_screen()
            self.clock.tick(60)

    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

    def _create_skyfull(self):
        star = Stars(self)

        star_width, star_height = star.rect.size

        current_x, current_y = star_width, star_height
        while current_y < (self.settings.screen_height - 9 * star_height):
            while current_x < (self.settings.screen_width - 2 * star_width):
                self._create_star(current_x, current_y)
                current_x += 2 * star_width

            current_x = star_width
            current_y += 2 * star_height


    def _create_star(self, x_position, y_position):
        new_star = Stars(self)
        new_star.x = x_position
        new_star.rect.x = x_position
        new_star.rect.y = y_position
        self.stars.add(new_star)

    def _update_screen(self):
        self.screen.fill(self.settings.bg_screen)
        self.stars.draw(self.screen)

        pygame.display.flip()



class Stars(Sprite):
    def __init__(self, sky_game):
        super().__init__()
        self.screen = sky_game.screen

        self.image = pygame.image.load(r"C:\Users\rh.agriter\Desktop\eu\codigos\python_crash_course\jogo_alien_2d\try_it_yourself\bmpfiles\planets\Frames\earth1.bmp")
        self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect()

        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        self.x = float(self.rect.x)


if __name__ == "__main__":
    bluesky = Sky()
    bluesky.run_game()