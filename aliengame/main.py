import sys
from time import sleep

import pygame

from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from inputbox import InputBox
from label import Label
from ship import Ship
from bullet import Bullet
from alien import Alien


# In Alien Invasion, the player controls a rocket ship that appears
# at the bottom center of the screen. The player can move the ship
# right and left using the arrow keys and shoot bullets using the
# spacebar. When the game begins, a fleet of aliens fills the sky
# and moves across and down the screen. The player shoots and
# destroys the aliens. If the player destroys all the aliens, a new fleet
# appears that moves faster than the previous fleet. If any alien hits
# the player’s ship or reaches the bottom of the screen, the player
# loses a ship. If the player loses three ships, the game ends.

# first development phase

class AlienInvasion:
    """Overall class to manage game assets and behavior."""

    def __init__(self):
        """Initialize the game, and create game resources."""
        pygame.init()
        self.settings = Settings()
        if self.settings.mode == 1:
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
            self.settings.screen_width = self.screen.get_rect().width
            self.settings.screen_height = self.screen.get_rect().height
        else:
            self.screen = pygame.display.set_mode((self.settings.screen_width,self.settings.screen_height))

        self.clock = pygame.time.Clock()

        pygame.display.set_caption("Alien Invasion")

        # Create an instance to store game statistics.
        # and create a scoreboard.
        self.stats = GameStats(self)
        self.scoreboard = Scoreboard(self)

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()

        # Start Alien Invasion in an inactive state.
        self.game_active = False
        # Make a first play state
        self.first_play = True
        pygame.mouse.set_visible(False)

        # Make the Play button.
        self.play_button = Button(self, "Play", (0, 135, 0), self.screen.get_rect().center, (200, 50), self._play_button)

        # Make the config button.
        self.config_button = Button(self, "Settings", (0, 0, 100), (200, 400), (250, 100), self._settings_button)
        self.config = False
        self.create_instance = False
        self.label_state = None
        self.input_state = None

        # The key continues to work while pressed down
        pygame.key.set_repeat(500, 50)




    def run_game(self):
        """Start the main loop for the game."""
        while True:
            self._check_events()
            if self.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()

            self._update_screen()
            self.clock.tick(60)
    
    def _check_events(self):
        """Respond to keypresses and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            # Move the ship to the right
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
                if self.input_state:
                    self.input_state.handle_key_event(event)

            # Stop moving
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

            elif event.type == pygame.MOUSEBUTTONDOWN and not self.game_active:
                mouse_pos = pygame.mouse.get_pos()
                if self.label_state:
                    self.input_state.handle_mouse_event(event)
                        
                self._check_collide(mouse_pos)

    def _check_collide(self, mouse_pos):
        if self.play_button.rect.collidepoint(mouse_pos) and not self.first_play:
            self.play_button.action()
        
        elif self.config_button.rect.collidepoint(mouse_pos):
            self.config_button.action()
            self._create_settings_button()    

        elif self.config:
            buttons = {self.alien_speed_button: [self.alien_label, self.input_alien_speed],
                    self.ship_speed_button: [self.ship_label, self.input_ship_speed],
                    self.bullets_alowed_button: [self.bullets_label, self.input_bullets_alowed]}
            for button in buttons.keys():
                if button.rect.collidepoint(mouse_pos):
                    label = buttons[button][0]
                    input_box = buttons[button][1]
                    self.label_state = label.draw_label
                    self.input_state = input_box
                    break


    def _play_button(self):
        """Start a new game when the player clicks Play."""
        if not self.game_active: 
            # Reset the game statistics.
            self.stats.reset_stats()
            self.game_active = True
            # Get rid of any remaining bullets and aliens.
            self.bullets.empty()
            self.aliens.empty()

            # Create a new fleet and center the ship.
            self._create_fleet()
            self.ship.center_ship()

            # Hide the mouse cursor.
            pygame.mouse.set_visible(False)

            # Update the game score and level
            self.scoreboard.prep_images()

    def _settings_button(self):
        """Open settings when the player clicks the button.."""
        if not self.game_active and not self.create_instance:
            self.alien_speed_button = Button(self, "Alien Speed", (0, 0, 0), (200, 100), (250, 100))
            self.alien_label = Label(self, "Speed:", (200, 200))
            self.input_alien_speed =  InputBox(self, f"{self.settings.alien_speed}", (self.alien_label.msg_image_rect.right + 10, self.alien_label.msg_image_rect.centery), (65, 55), self.settings, "alien_speed")

            self.ship_speed_button = Button(self, "Ship Speed", (0, 0, 0), (200, 310), (250, 100))
            self.ship_label = Label(self, "Speed:", (200, 430))
            self.input_ship_speed = InputBox(self, f"{self.settings.ship_speed}", (self.ship_label.msg_image_rect.right + 10, self.ship_label.msg_image_rect.centery), (65, 55), self.settings, "ship_speed")

            self.bullets_alowed_button = Button(self, "Bullets Alowed", (0, 0, 0), (200, 560), (250, 100))  
            self.bullets_label = Label(self, "Bullets:", (200, 670))
            self.input_bullets_alowed = InputBox(self, f"{self.settings.bullets_alowed}", (self.bullets_label.msg_image_rect.right + 10, self.bullets_label.msg_image_rect.centery), (65, 55), self.settings, "bullets_alowed")

            self.create_instance = True
        self.config = True

    def _create_settings_button(self):
        self.alien_speed_button.draw_button()
        self.ship_speed_button.draw_button()
        self.bullets_alowed_button.draw_button()                  

    def _check_keydown_events(self, event):
        """Respond to keypresses."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_p and self.first_play:
            pygame.mouse.set_visible(False)
            self.first_play = False
            self.game_active = True
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
    
    def _check_keyup_events(self, event):
        """Respond to key releases."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group."""
        if len(self.bullets) < self.settings.bullets_alowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """Update position of bullets and get rid of old bullets."""
        #Update bullet positions
        self.bullets.update()
        
        # Get rid of bullets that have disappeared.
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collisions()
        
    def _check_bullet_alien_collisions(self):
        """Respond to bullet-alien collisions."""
        # Remove any bullets and aliens that have collided.
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True
        )
        
        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.scoreboard.prep_score()
            self.scoreboard.check_high_score()


        if not self.aliens:
            self._new_level()

    def _new_level(self):
        # Destroy existing bullets and create new fleet.
        self.bullets.empty()
        self._create_fleet()
        self.settings.increase_speed()

        # Increase level.
        self.stats.level += 1
        self.scoreboard.prep_level()

    def _update_aliens(self):
        """Check if the fleet is at an edge, then Update positions"""
        self._check_fleet_edges()
        self.aliens.update()

        # Look for alien-ship collisions.
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
        
        # Look for aliens hitting the bottom of the screen.
        self._check_aliens_bottom()

        

    def _create_fleet(self):
        """Create the fleet of aliens."""
        # Create an alien and keep adding aliens until there's no room left.
        # Spacing between aliens is one alien width and height.

        alien = Alien(self)
        alien_width, alien_height = alien.rect.size

        current_x, current_y = alien_width, alien_height
        while current_y < (self.settings.screen_height - 9 * alien_height):
            while current_x < (self.settings.screen_width - 2 * alien_height):
                self._create_alien(current_x, current_y)
                current_x += 2 * alien_width

            # Finished a row; reset x value, and increment y value.
            current_x = alien_width
            current_y += 2 * alien_height

    def _create_alien(self, x_position, y_position):
        """Create an alien and place it in the fleet."""
        new_alien = Alien(self)
        new_alien.x = x_position
        new_alien.rect.x = x_position
        new_alien.rect.y = y_position
        self.aliens.add(new_alien)

    def _check_fleet_edges(self):
        """Respond appropriately if any aliens have reached an edge."""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _check_aliens_bottom(self):
        """Check if any aliens have reached the bottom of the screen."""
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.settings.screen_height:
                # Treat this the same as if the ship got hit.
                self._ship_hit()
                break
        
    def _change_fleet_direction(self):
        """Drop the entire fleet and change the fleet's direction."""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _ship_hit(self):
        """Respond to the ship being hit by an alien."""
        if self.stats.ships_left > 0:

            # Decrement ships left, and update scoreboard.
            self.stats.ships_left -= 1
            self.scoreboard.prep_ships()

            # Get rid of any remaining bullets and aliens.
            self.bullets.empty()
            self.aliens.empty()

            # Create a new fleet and center the ship.
            self._create_fleet()
            self.ship.center_ship()

            # Pause
            sleep(0.5)
        else:
            self.stats.save_high_score(self.stats.score)
            self.game_active = False
            self.config = False
            pygame.mouse.set_visible(True)


    def _update_screen(self):
        """Update images on the screen, and flip to the new screen."""
        # Draw the play button if the game is inactive,
        self.screen.fill(self.settings.bg_color)
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.ship.blitme()
        self.aliens.draw(self.screen)

        # Draw the score information
        self.scoreboard.show_score()

        if not self.game_active:
            pygame.mouse.set_visible(True)
            if not self.config:
                self.config_button.draw_button()
            elif self.config:
                self._create_settings_button()
                if self.label_state:
                    self.label_state()
                    self.input_state.draw_input()
            if not self.first_play:
                self.play_button.draw_button()
                    
        pygame.display.flip()            

if __name__ == "__main__":
    # Make a instance, and run the game.
    ai = AlienInvasion()
    ai.run_game()