class Settings:
    """A classe to store all setings for Alien Invasion."""
    
    def __init__(self):
        """intialize the game's settings."""
        # Screen settings
        self.mode = 2
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)

        # Ship settings
        self.ship_speed = 3.5
        self.ship_limit = 3
        
        # Bullet settings
        self.bullet_speed = 4.0
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_alowed = 3

        # Alien settings
        self.alien_speed = 1.0
        self.fleet_drop_speed = 10
        # fleet_direction of 1 represents right; -1 represents left.
        self.fleet_direction = 1