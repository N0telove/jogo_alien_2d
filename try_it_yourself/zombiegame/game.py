import pygame
import sys
from configuration import ScreenSettings
from zombie import Zombie
from gun import Gun
from ammo import Ammo
from vampire import Vampire

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

        self._create_coven()

    def run_game(self):
        """Initialize the game."""
        while True:
            self._check_events()
            self.zombie.update()
            self.gun.update(self.zombie.rect)
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

    def _check_presses_event(self, event):
        """Respond to keypresses."""
        if event.key == pygame.K_RIGHT:
            self.zombie.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.zombie.moving_left = True
        elif event.key == pygame.K_UP:
            self.zombie.moving_up = True
        elif event.key == pygame.K_DOWN:
            self.zombie.moving_down = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
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
            self.ammos, self.vampires, False, True
        )

        if not self.vampires:
            # Destroy existing ammos and create new coven.
            self.ammos.empty()
            self._create_coven()

    def _update_vampires(self):
        """Check if the coven is an edge, than update positions."""
        self._check_coven_edges()
        self.vampires.update()

    def _create_coven(self):
        """Create the coven of vampires."""
        # Create a vampire and keep adding vampires until there's no room left.
        # Spacing between vampires is one vampire width and height.;

        vampire = Vampire(self)
        vampire_width, vampire_height = vampire.rect.size

        current_x, current_y = vampire_width, vampire_height
        while current_y < (self.settings.screen_height - 5 * vampire_height):
            while current_x < (self.settings.screen_width - 2 * vampire_height):
                self._create_vampire(current_x, current_y)
                current_x += 2 * vampire_width

            # Finished a row; reset x value, and increment y value.
            current_x = vampire_width
            current_y += 2 * vampire_height

    def _create_vampire(self, x_position, y_position):
        """Create a vampire and place it in the coven."""
        new_vampire = Vampire(self)
        new_vampire.x = x_position
        new_vampire.rect.x = x_position
        new_vampire.rect.y = y_position
        self.vampires.add(new_vampire)

    def _check_coven_edges(self):
        """Respond appropriately if any vampires have reached an edge."""
        for vampire in self.vampires.sprites():
            if vampire.check_edges():
                self._change_coven_direction()
                break

    def _change_coven_direction(self):
        """Change the coven's direction."""
        # for vampire in self.vampires.sprites():
        #     vampire.rect.y += self.settings.coven_drop_speed
        self.settings.coven_direction *= -1


    def _update_screen(self):
        """Update the image"""
        self.screen.fill(self.settings.bg_screen)
        for ammo in self.ammos.sprites():
            ammo.draw_ammo()

        self.zombie.blitme()
        self.gun.blit_gun()
        self.vampires.draw(self.screen)

        pygame.display.flip()


if __name__ == "__main__":
    # Make a instance and run the game
    main = Game()
    main.run_game()