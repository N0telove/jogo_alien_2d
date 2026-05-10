import pygame
from pygame.sprite import Sprite
import sys
from random import randint, choice
from pathlib import Path
from time import sleep
import pygame.font


class Shoot():
    def __init__(self):
        """Initialize the game."""
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        self.clock = pygame.time.Clock()

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.rectangle = pygame.sprite.Group()
        self.stats = GameStats(self)

        self.game_active = False

        self.play_button = Button(self, "Play")

    def run_game(self):
        while True:
            self._check_events()
            if self.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_rectangle()

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

            # Stop moving
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
    
    def _check_play_button(self, mouse_pos=(0,)):
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        """Start a new game when the player clicks Play."""
        if button_clicked and not self.game_active: 
            # Reset the game statistics.
            self.stats.reset_stats()
            self.game_active = True
            # Get rid of any remaining bullets and aliens.
            self.bullets.empty()

            # Create a new fleet and center the ship.
            self._create_rectangle()
            self.ship.center_ship()

            # Hide the mouse cursor.
            pygame.mouse.set_visible(False)


    def _check_keydown_events(self, event):
        """Respond to keypresses."""
        if event.key == pygame.K_UP:
            self.ship.moving_up = True
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
    
    def _check_keyup_events(self, event):
        """Respond to key releases."""
        if event.key == pygame.K_UP:
            self.ship.moving_up = False
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = False

    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group."""
        if len(self.bullets) < self.settings.bullets_alowed and self.stats.bullets_left > 0:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)
            self.stats.bullets_left -= 1
        

    def _update_bullets(self):
        """Update position of bullets and get rid of old bullets."""
        #Update bullet positions
        self.bullets.update()
        
        # Get rid of bullets that have disappeared.
        for bullet in self.bullets.copy():
            if bullet.rect.right >= self.settings.screen_width:
                self.bullets.remove(bullet)

        self._check_bullet_rectangle_collisions()

    def _check_bullet_rectangle_collisions(self):
        """Respond to bullet-alien collisions."""
        # Remove any bullets and aliens that have collided.
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.rectangle, False, True
        )

        if collisions:
            self.settings.eliminate_sprites += 1
            self.bullets.empty()
            self._create_rectangle()
            sleep(3)
        
        if self.settings.eliminate_sprites == 3:
            self.game_active = False

    def _create_rectangle(self):
        """Create a rectangle"""
    
        new_rectangle = Rectangle(self)
        new_rectangle.x = self.settings.screen_width - 100
        new_rectangle.rect.x = new_rectangle.x
        new_rectangle.rect.y = self.settings.screen_height // 2
        new_rectangle.y = new_rectangle.y
        self.rectangle.add(new_rectangle)

    def _update_rectangle(self):
        """Update rectangle position"""
        # Update rectangle position.
        self.rectangle.update()

    def _update_screen(self):
        self.screen.fill(self.settings.bg_screen)
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        self.ship.blitme()
        self.rectangle.draw(self.screen)


        if self.stats.bullets_left < 1 and not self.bullets:
            self.game_active = False
            self.rectangle.empty()

        if not self.game_active:
            self.play_button.draw_button()
            pygame.mouse.set_visible(True)

        pygame.display.flip()


class Ship:
    """A classe to manage the ship."""

    def __init__(self, ai_game):
        """Initialize the ship and set its starting position."""
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.settings = ai_game.settings

        # Load the ship image and get its rect.
        self.image = pygame.image.load("aliengame/images/ship.bmp")
        self.image = pygame.transform.rotate(self.image, -90)
        self.rect = self.image.get_rect()

        # Start each new ship at the midleft of the screen
        self.rect.midleft = self.screen_rect.midleft

        # Store a float for the ship's exact horizontal position
        self.y = float(self.rect.y)

        # Movement flags; start with a ship that's not moving.
        self.moving_up = False
        self.moving_down = False


    def update(self):
        """Update the ship's position based on the movement flags."""
        # Update the ship's x value, not the rect.
        if self.moving_up and self.rect.top >= 0:
            self.y -= self.settings.ship_speed
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.y += self.settings.ship_speed

        # Update rect object from self.x.
        self.rect.y = self.y

    def center_ship(self):
        """Center the ship on the screen."""
        self.rect.midleft = self.screen_rect.midleft
        self.y = float(self.rect.y)

    def blitme(self):
        """Draw the ship at its current location."""
        self.screen.blit(self.image, self.rect)


class Bullet(Sprite):
    """A class to manage bullet fired from the ship."""

    def __init__(self, ai_game):
        """Create a bullet object at the ship's current position."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.bullet_color

        # Create a bullet rect at (0, 0) and then set correct position.
        self.rect = pygame.Rect(0, 0, self.settings.bullet_height,
                                self.settings.bullet_width)
        self.rect.midright = ai_game.ship.rect.midright

        # Store the bullet's position as a float.
        self.x = float(self.rect.x)

    def update(self):
        """Move the bullet up the screen."""
        # Update the exact position of the bullet.
        self.x += self.settings.bullet_speed
        # Update the rect position.
        self.rect.x = self.x
    
    def draw_bullet(self):
        """Draw the bullet to the screen."""
        pygame.draw.rect(self.screen, self.color, self.rect)


class Rectangle(Sprite):
    """A classe to manage the rectangle."""

    def __init__(self, ai_game):
        """Initialize the rectangle and set its starting position."""
        super().__init__()
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.settings = ai_game.settings

        # Load the rectangle image and get its rect.
        self.image = pygame.image.load(Path().cwd() / Path("try_it_yourself/shoot_practice/bmp_sprites/chocolate_monster.bmp"))
        self.image.set_colorkey((255, 255, 255))
        self.image = pygame.transform.scale(self.image, (60, 60))
        self.rect = self.image.get_rect()

        # Start each new rectangle at the midright of the screen
        self.rect.midright = self.screen_rect.midright

        # Store a float for the rectangle's exact vertical position
        self.y = float(self.rect.y)

        # Vertical movement: 1 = down, -1 = up
        self.vertical_direction = choice([-1, 1])
        # Random speed variation for natural movement
        self.speed_variation = randint(0, 100) / 100.0  # 0.0 to 1.0

    def check_edges(self):
        """Return True if vampire is at the edge of screen."""
        screen_rect = self.screen.get_rect()
        return (self.rect.top <= 0) or (self.rect.bottom >= screen_rect.height)


    def update(self):
        """Update the rectangle's position based on the movement flags."""
        # Update the ship's x value, not the rect.
        base_speed = self.settings.rectangle_speed
        speed = base_speed * (0.5 + self.speed_variation)

        # Move vertically
        self.y += speed * self.vertical_direction
        self.rect.y = self.y
        
        # Keep within screen bounds
        if self.rect.top <= 0:
            self.rect.top = 0
            self.y = float(self.rect.y)
            self.vertical_direction = 1  # Change to down
        elif self.rect.bottom >= self.screen_rect.height:
            self.rect.bottom = self.screen_rect.height
            self.y = float(self.rect.y)
            self.vertical_direction = -1  # Change to up
        
        # Random direction change (small chance)
        if randint(0, 100) < 2:  # 2% chance to change direction
            self.vertical_direction *= -1

class Button:
    """A class to build buttons for the game."""

    def __init__(self, ai_game, msg):
        """Initialize button attributes."""
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        # Set the dimensions and properties of the button.
        self.width, self.height = 200, 50
        self.button_color = (0, 135, 0)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)

        # Build the button's rect object and center it.
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        # The button message needs to be prepped only once.
        self._prep_msg(msg)

    def _prep_msg(self, msg):
        """Turn msg into a rendered image and center text on the button."""
        self.msg_image = self.font.render(msg, True, self.text_color,
                self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        """Draw blank button and then draw message."""
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)


class Settings:
    """Set screen settings"""

    def __init__(self):
        """Initialize the game's settings."""
        # Screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_screen = (220, 220, 220)

        # Ship settings
        self.ship_speed = 3.5

        # Rectangle settings
        self.rectangle_speed = 5
        self.rectangle_direction = -1

        # Bullet settings
        self.bullet_speed = 4.0
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_alowed = 5
        self.bullets_limit = 100

        self.eliminate_sprites = 0

class GameStats:
    """Track statistics."""

    def __init__(self, ai_game):
        """Initialize statistics."""
        self.settings = ai_game.settings
        self.reset_stats()

    def reset_stats(self):
        """Initialize statistics that can change during the game."""
        self.bullets_left = self.settings.bullets_limit
        self.kills = self.settings.eliminate_sprites


if __name__ == "__main__":
    game = Shoot()
    game.run_game()