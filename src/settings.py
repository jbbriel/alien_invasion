class Settings():
    """A Class to store all settings for Alien Invasion"""

    def __init__(self):
        """Initialize the games settings"""
        # Screen Settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)

        # Ship Settings
        self.ship_speed = 2.5
        self.ship_limit = 3

        # Bullet Settings
        self.bullet_speed = 1.5
        self.bullet_width = 400
        self.bullet_height = 10
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 15

        # alien settings
        self.alien_speed = 1.0
        self.fleet_drop_speed = 10
        # fleet direction of 1 represents right; -1 represents left
        self.fleet_direction  = 1