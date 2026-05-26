import json

class Stats:
    """Track statistics for the game."""

    def __init__(self, ai_game):
        """Initialize the statistics."""
        self.settings = ai_game.settings
        # Counter kills settings
        self.reset_stats()

        # Max kills
        self.max_kills = self.get_max_kills()["kills"]

    def reset_stats(self):
        """Initialize statistics that can change during the game."""
        self.zombies_left = self.settings.zombie_limit
        self.eliminate_sprites = 0
        self.level = 1

    def get_max_kills(self):
        with open("try_it_yourself/zombiegame/json/kills.json") as file:
            data = json.load(file)
            return data
        
    def save_max_kills(self):
        data = self.get_max_kills()
        if self.eliminate_sprites > data["kills"]:
            with open("try_it_yourself/zombiegame/json/kills.json", "w") as file:
                data["kills"] = self.eliminate_sprites
                json.dump(data, file)
