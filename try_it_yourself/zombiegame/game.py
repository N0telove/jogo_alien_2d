import sys
from time import sleep
from random import randint

import pygame

from configuration import ScreenSettings
from stats import Stats
from counter_kill import CounterKill
from zombie import Zombie
from gun import Gun
from ammo import Ammo
from vampire import Vampire
from keys import Button

class Game:
    """Initialize the Zombie game."""

    def __init__(self):
        """Initialize the game, and create game resources."""
        pygame.init()
        self.settings = ScreenSettings()
        if self.settings.mode == 1:
            self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        else:
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
            self.settings.screen_width = self.screen.get_rect().width
            self.settings.screen_height = self.screen.get_rect().height
        self.clock = pygame.time.Clock()


        pygame.display.set_caption("I'm a Zombieee, i'll bite you...")

        self.zombie = Zombie(self)
        self.gun = Gun(self)
        self.ammos = pygame.sprite.Group() # ammo is uncountable, but...
        self.vampires = pygame.sprite.Group()
        self.stats = Stats(self) # Instance of statistics.
        self.counter = CounterKill(self)

        self._create_coven()

        # Start the game in an active state.
        self.game_active = False
        # Make a first play state
        self.first_play = False
        pygame.mouse.set_visible(False)

        # Make the Play button
        self.play_button = Button(self, "Play")

    def run_game(self):
        """Initialize the game."""
        while True:
            
            # A arma é atualizada para a posição do zumbi
            self.gun.update(self.zombie.rect)

            self._check_events()
            if self.game_active:
                self.zombie.update()
                self._update_ammos()
                self._update_vampires()
            
            self._update_screen()
            self.clock.tick(60)

    def _check_events(self):
        """Respond to keypresses and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            
            # Move the Zombie 
            elif event.type == pygame.KEYDOWN:
                    self._check_presses_event(event)

            # Stop moving the Zombie
            elif event.type == pygame.KEYUP:
                self._check_releases_event(event)

            elif event.type == pygame.MOUSEBUTTONDOWN and self.first_play:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_play_button(self, mouse_pos=(0,)):
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        """Start a new game when the player clicks Play."""
        if button_clicked and not self.game_active: 
            # Reset the game statistics and settings.
            self.settings.initialize_dynamic_settings()
            self.stats.reset_stats()

            self.game_active = True
            # Get rid of any remaining bullets and aliens.
            self.ammos.empty()
            self.vampires.empty()

            # Create a new fleet and center the ship.
            self._create_coven()
            self.zombie.position_zombie()

            # Update the game score and level
            self.counter.prep_images()

            # Hide the mouse cursor.
            pygame.mouse.set_visible(False)

    def _check_presses_event(self, event):
        """Respond to keypresses."""
        if event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_p and not self.first_play:
            self.first_play = True
            self.game_active = True
        elif event.key == pygame.K_RIGHT:
            self.zombie.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.zombie.moving_left = True
        elif event.key == pygame.K_UP:
            self.zombie.moving_up = True
        elif event.key == pygame.K_DOWN:
            self.zombie.moving_down = True
        elif event.key == pygame.K_SPACE:
            if self.game_active:
                self._fire_ammo()

    def _check_releases_event(self, event):
        """Respond to key releases."""
        if event.key == pygame.K_RIGHT:
            self.zombie.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.zombie.moving_left = False
        elif event.key == pygame.K_UP:
            self.zombie.moving_up = False
        elif event.key == pygame.K_DOWN:
            self.zombie.moving_down = False

    def _fire_ammo(self):
        """Create a new ammo and add it to the ammos group."""
        if len(self.ammos) < self.settings.ammo_alowed:
            new_ammo = Ammo(self)
            self.ammos.add(new_ammo)

    def _update_ammos(self):
        """Update position of ammos and get rid of old ammos."""
        # Update ammo positions
        self.ammos.update()

        # Get rid of ammos that have dissapeared.
        for ammo in self.ammos.copy():
            if ammo.rect.left > self.screen.get_rect().right:
                self.ammos.remove(ammo)

        self._check_ammo_vampire_collisions()

    def _check_ammo_vampire_collisions(self):
        """Respond to ammo-alien collisions."""
        # Remove any ammo and vampire that have collided.
        collisions = pygame.sprite.groupcollide(
            self.ammos, self.vampires, True, True
        )
        if collisions:
            for zombie in collisions.values():
                self.settings.increase_speed()
                self.stats.eliminate_sprites += 1
            self.counter.prep_kills()
            self.counter.check_highest_kills()


        if not self.vampires:
            # Destroy existing ammos and create new coven.
            self._new_level()

    def _new_level(self):
        self.ammos.empty()
        self._create_coven()

        # Increase level.
        self.stats.level += 1
        self.counter.prep_level()


    def _update_vampires(self):
        """Update positions of vampires and check collisions."""
        self.vampires.update()
        self._check_vampire_collisions()

        # Look for vampires-zombie collisions.
        if pygame.sprite.spritecollideany(self.zombie, self.vampires):
            self._zombie_hit()

        # Look for vampires hitting the left edge of the screen.
        self._check_vampire_left()

    def _create_coven(self):
        """Create a group of vampires with random positions."""
        vampire = Vampire(self)
        vampire_width, vampire_height = vampire.rect.size

        # Create vampires in random positions across the right side of screen
        for _ in range(15):  # Create 15 vampires
            x_pos = randint(self.settings.screen_width - 200, self.settings.screen_width - vampire_width - 10)
            y_pos = randint(vampire_height, self.settings.screen_height - vampire_height - 10)
            self._create_vampire(x_pos, y_pos)

    def _create_vampire(self, x_position, y_position):
        """Create a vampire and place it in the coven."""
        new_vampire = Vampire(self)
        new_vampire.x = x_position
        new_vampire.rect.x = x_position
        new_vampire.y = y_position
        new_vampire.rect.y = y_position
        self.vampires.add(new_vampire)

    def _check_vampire_collisions(self):
        """Check and resolve collisions between vampires."""
        vampires_list = self.vampires.sprites()
        
        for i, vampire in enumerate(vampires_list):
            for other_vampire in vampires_list[i + 1:]:
                if vampire.rect.colliderect(other_vampire.rect):
                    # Reverse directions when colliding
                    vampire.vertical_direction *= -1
                    other_vampire.vertical_direction *= -1
                    
                    # Move apart to prevent sticking
                    if vampire.rect.top < other_vampire.rect.top:
                        vampire.rect.y -= 5
                        other_vampire.rect.y += 5
                    else:
                        vampire.rect.y += 5
                        other_vampire.rect.y -= 5
                    
                    # Update y positions
                    vampire.y = float(vampire.rect.y)
                    other_vampire.y = float(other_vampire.rect.y)

    def _check_vampire_left(self):
        """Check if any vampire have reached the left edge of the screen."""
        for vampire in self.vampires.sprites():
            if vampire.rect.left <= 0:
                # Treat this the same as if the zombie got bite.
                self._zombie_hit()
                break

    def _zombie_hit(self):
        """Respond to the zombie being bite by a vampire."""
        if self.stats.zombies_left > 0:
            
            # Decrement zombies left and update scoreboard.
            self.stats.zombies_left -= 1
            self.counter.prep_life()

            # Get rid of any remaining ammo and vampires.
            self.ammos.empty()
            self.vampires.empty()

            # Create a new coven and position the new zombie.
            self._create_coven()
            self.zombie.position_zombie()

            # Update lives counter
            self.counter.prep_life()

            # Restart the game's speed
            self.settings.initialize_dynamic_settings()

            self.ammos.empty()

            # Pause
            sleep(0.5)
        else:
            self.stats.save_max_kills()
            self.game_active = False
            pygame.mouse.set_visible(True)


    def _update_screen(self):
        """Update the image"""
        self.screen.fill(self.settings.bg_screen)
        for ammo in self.ammos.sprites():
            ammo.draw_ammo()

        self.zombie.blitme()
        self.gun.blit_gun()
        self.vampires.draw(self.screen)
        self.counter.draw_counter()

        # Draw the play button if the game is inactive,
        if not self.game_active and self.first_play:
            self.play_button.draw_button()

        pygame.display.flip()


if __name__ == "__main__":
    # Make a instance and run the game
    main = Game()
    main.run_game()