class Settings():
    """A Class to store all settings for Alien Invasion"""

    def __init__(self):
        """Initialize the games settings"""
        # Screen Settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)

        # Ship Settings
        self.ship_speed = 2.0
        self.ship_limit = 3

        # Bullet Settings
        self.bullet_speed = 1.0
        self.bullet_width = 5
        self.bullet_height = 10
        self.bullet_color = (255, 0, 0)
        self.bullets_allowed = 15

        # Scoring
        self.alien_points = 50

        # how quickly the alieb points value increase. Its a multiplier
        self.score_scale = 1.5

        # alien settings
        self.alien_speed = 1.0
        self.fleet_drop_speed = 10
        # fleet direction of 1 represents right; -1 represents left
        self.fleet_direction  = 1

        # How quickly the game speeds up
        self.speedup_cycle = 1.1

        self.difficulty_level = 'medium'

        self.initialize_dynamic_setting()

    def initialize_dynamic_setting(self):
        if self.difficulty_level == 'easy':
            self.ship_speed = 2.0
            self.bullet_speed = 1.0
            self.alien_speed = 1.0
            self.fleet_direction = 0.5
        elif self.difficulty_level == 'medium':
            self.ship_speed = 2.5
            self.bullet_speed = 1.5
            self.alien_speed = 1.5
            self.fleet_direction = 1.0
        elif self.difficulty_level == 'hard':
            self.ship_speed = 3.0
            self.bullet_speed = 2.0
            self.alien_speed = 1.5
            self.fleet_direction = 2.5

    def increase_speed(self):
        # Increase speed settings and alienpoint values
        self.ship_speed *= self.speedup_cycle
        self.bullet_speed *= self.speedup_cycle
        self.alien_speed *= self.speedup_cycle

        self.alien_points = int(self.alien_points * self.score_scale)

    def set_difficulty(self, diff_setting):
        if diff_setting == 'easy':
            print('easy')
        elif diff_setting == 'medium':
            pass
        elif diff_setting == 'difficult':
            pass