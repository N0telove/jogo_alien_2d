class ScreenSettings:
    """Set screen settings"""

    def __init__(self):
        """Initialize the game's settings."""
        # Screen settings
        self.mode = 1
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_screen = (220, 220, 220)

        # Zombie settings
        self.zombie_speed = 2.5
        self.zombie_limit = 1

        # Ammo settings
        self.ammo_speed = 3.0
        self.ammo_width = 10
        self.ammo_height = 3
        self.ammo_color = (60, 60, 60)
        self.ammo_alowed = 5

        # Vampire settings
        self.vampire_speed = 1.0
        # coven direction of 1 represents right; -1 represents left.
        self.coven_direction = -1

        # Counter kills settings
        self.eliminate_sprites = 0