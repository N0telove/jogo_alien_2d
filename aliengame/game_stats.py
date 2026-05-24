class GameStats:
    """Track statistics for Alien Invasion."""

    def __init__(self, ai_game):
        """Initialize statistics."""
        self.settings = ai_game.settings
        self.reset_stats()

        # High score should never be reset.
        self.high_score = self.get_high_score()

    def reset_stats(self):
        """Initialize statistics that can change during the game."""
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1

    def get_high_score(self):
        with open("aliengame/txt/log.txt", "r", encoding="utf-8") as file:
            scores = []
            for score in file:
                scores.append(int(score))
            if scores:
                return max(scores)
            else:
                return 0
            
    def save_high_score(self, score):
        with open("aliengame/txt/log.txt", "a", encoding="utf-8") as file:
            file.write(f"{score}\n")
