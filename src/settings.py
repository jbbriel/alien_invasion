class Settings():
    """A Class to store all settings for Alien Invasion"""

    def __init__(self):
        """Initialize the games settings"""
        # Screen Settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)

        # Ship Settings
        self.ship_speed = 1.5
        self.ship_limit = 3

        # Bullet Settings
        self.bullet_speed = 0.5
        self.bullet_width = 300
        self.bullet_height = 10
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 15

        # Scoring
        self.alien_points = 50

        # alien settings
        self.alien_speed = 0.5
        self.fleet_drop_speed = 5
        # fleet direction of 1 represents right; -1 represents left
        self.fleet_direction  = 1

        # How quickly the game speeds up
        self.speedup_cycle = 1.1

        self.initialize_dynamic_setting()

    def initialize_dynamic_setting(self):
        self.ship_speed = 1.5
        self.bullet_speed = 0.5
        self.alien_speed = 0.5

        self.fleet_direction = 1

    def increase_speed(self):
        self.ship_speed *= self.speedup_cycle
        self.bullet_speed *= self.speedup_cycle
        self.alien_speed *= self.speedup_cycle
