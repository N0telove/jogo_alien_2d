import pygame
from pygame.sprite import Sprite
import sys
from random import randint
from pathlib import Path

# Classe principal
class RainDrop:
    def __init__(self):
        """Inicia o jogo."""
        pygame.init() # Inicia os sub-modulos (display, por exemplo) do pygame
        self.settings = Configuration3()
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        self.clock = pygame.time.Clock()

        self.drops = pygame.sprite.Group()
        self._create_sky()

    def run_game(self):
        while True:
            self._check_events()
            self._update_screen()
            self.clock.tick(60)

    def __check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

    def _create_sky(self):
        drop = Drops(self)
        drop_width, drop_height = drop.rect.size
        self._create_raindrop(drop_width, drop_height)

    def _create_raindrop(self, x_position, y_position):
        new_drop = Drops(self)
        new_drop.x = x_position
        new_drop.rect.x = x_position
        new_drop.rect.y = y_position
        self.drops.add(new_drop)

    def _update_screen(self):
        self.screen.fill(self.settings.bg_screen)
        self.drops.draw(self.screen)

        pygame.display.flip()


class Drops(Sprite):
    def __init__(self, drop_game):
        super().__init__()
        self.screen = drop_game.screen