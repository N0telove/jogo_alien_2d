import pygame
from pygame.sprite import Sprite
import sys
from random import randint
from pathlib import Path


class Sky():
    def __init__(self):
        """Initialize the game."""
        pygame.init()
        self.settings = Configuration2()
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        self.clock = pygame.time.Clock()

        self.stars = pygame.sprite.Group()
        self._create_skyfull()

        # print(f"Planetas criados: {len(self.stars)}")

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


        max_x = self.settings.screen_width - star_width
        max_y = self.settings.screen_height - star_height

        planets_to_create = 40
        attempts = 0 # Trava de segurança

        # O loop continua até termos x planetas na tela
        # A trava "attempts" evita que o jogo trave em um loop infinito
        # caso a tela fique cheia
        while len(self.stars) < planets_to_create and attempts < 1000:

            # Sorteamos coordenadas seguras
            random_x = randint(0, max_x)
            random_y = randint(0, max_y)

            # Criamos um retângulo virtual na posição sorteada para testar

            new_rect = pygame.Rect(random_x, random_y , star_width, star_height)

            # Verificamos se esse novo retângulo bate em algum planeta
            overlap = False
            for existing_star in self.stars.sprites():
                if new_rect.colliderect(existing_star):
                    overlap = True
                    break # Bateu em alguém, paramos de testar e validamos o overlap

            # Se não sobrepôs ninguém, é um local seguro! Podemos criar o planeta
            if not overlap:
                self._create_star(random_x, random_y)

            attempts += 1


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

        self.image = pygame.image.load(Path().cwd() / Path("try_it_yourself/planets/Frames/earth1.bmp"))
        self.image.set_colorkey((255, 255, 255))
        self.image = pygame.transform.scale(self.image, (90, 90))

        self.rect = self.image.get_rect()

        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        self.x = float(self.rect.x)




class Configuration2:
    """Set screen settings"""

    def __init__(self):
        """Initialize the game's settings."""
        # Screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_screen = (220, 220, 220)


if __name__ == "__main__":
    bluesky = Sky()
    bluesky.run_game()