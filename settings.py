class Settings:
    """A classe to store all setings for Alien Invasion."""
    
    def __init__(self):
        """intialize the game's settings."""
        # Screen settings
        self.mode = 2
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)
        self.ship_speed = 3.5