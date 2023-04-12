class GameStats:
    """Track Statistics for Alien Invasion"""
    def __init__(self, ai_game):
        """Initialize Statistics"""
        self.settings = ai_game.settings
        self.reset_stats()
        self.game_active = False

    def reset_stats(self):
        """Initialize Statistics that can change during the game"""
        self.ships_left = self.settings.ship_limit