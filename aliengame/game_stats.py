import json

class GameStats:
    """Track statistics for Alien Invasion."""

    def __init__(self, ai_game):
        """Initialize statistics."""
        self.settings = ai_game.settings
        self.reset_stats()

        # High score should never be reset.
        self.high_score = self.get_high_score()["high_score"]

    def reset_stats(self):
        """Initialize statistics that can change during the game."""
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1

    def get_high_score(self):
        with open("aliengame/json/highscore.json") as file:
            data = json.load(file)
            return data
            
    def save_high_score(self, score):
        data = self.get_high_score()
        if score > data["high_score"]:
            with open("aliengame/json/highscore.json", "w") as file:
                data["high_score"] = score
                json.dump(data, file)