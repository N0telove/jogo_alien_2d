import pygame
from pygame.sprite import Sprite
import sys
from random import randint
from pathlib import Path

# Classe principal
class FireDrop:
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
            self._update_drops()
            self._update_screen()
            self.clock.tick(60)

    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

    def _update_drops(self):
        self._check_drops_edges()
        self.drops.update()

    def _create_sky(self):
        drop = Drops(self)
        drop_width = drop.rect.width

        # Calcula quantas gotas cabem na largura da tela com espaçamento
        available_space_x = self.settings.screen_width
        number_drops_x = available_space_x // (2 * drop_width)

        for drop_number in range(number_drops_x):
            random_y = randint(-800, 0)
            self._create_firedrop(drop_number * 2 * drop_width, random_y)

    def _create_firedrop(self, x_position, y_position):
        new_drop = Drops(self)
        new_drop.y = y_position
        new_drop.rect.y = y_position
        new_drop.rect.x = x_position
        self.drops.add(new_drop)

    def _check_drops_edges(self):
        self.drops.update()
        for drop in self.drops.sprites():
            if drop.check_edges():
                drop.rect.y = randint(-100, -40)
                drop.y = float(drop.rect.y)
                drop.rect.x = randint(0, self.settings.screen_width)
                self.drop.wind_speed *= -1
                
    

    def _update_screen(self):
        self.screen.fill(self.settings.bg_screen)
        self.drops.draw(self.screen)

        pygame.display.flip()


class Drops(Sprite):
    def __init__(self, drop_game):
        super().__init__()
        self.screen = drop_game.screen
        self.settings = drop_game.settings

        self.image = pygame.image.load(Path().cwd() / Path("try_it_yourself/raindrops/sprites/fire_sprite.bmp"))
        self.image.set_colorkey((255, 255, 255))
        self.image = pygame.transform.scale(self.image, (90, 90))

        self.rect = self.image.get_rect()

        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        self.speed = drop_game.settings.drop_speed + randint(0, 2)
        self.y = float(self.rect.y)


    def check_edges(self):
        """Return True if alien is at the bottom edge of screen."""
        screen_rect = self.screen.get_rect()
        return (self.rect.top >= screen_rect.height) or (self.rect.right >= screen_rect.width)
        
    def update(self):
        """Move the alien down."""
        self.y += self.speed
        self.rect.y = self.y

        self.rect.x += self.settings.wind_speed


class Configuration3:
    """Set screen settings."""

    def __init__(self):
        """Initialize the game's settings."""
        # Configurações da tela.
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_screen = (220, 220, 220)

        # Configuração da velocidade da gota
        self.drop_speed = 3
        self.wind_speed = 1.5

if __name__ == "__main__":
    run = FireDrop()
    run.run_game()