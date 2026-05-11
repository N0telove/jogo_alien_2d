class Stats:
    """Track statistics for the game."""

    def __init__(self, ai_game):
        """Initialize the statistics."""
        self.settings = ai_game.settings
        # Counter kills settings
        self.eliminate_sprites = 0
        self.reset_stats()

    def reset_stats(self):
        """Initialize statistics that can change during the game."""
        self.zombies_left = self.settings.zombie_limit
        self.eliminate_sprites = 0