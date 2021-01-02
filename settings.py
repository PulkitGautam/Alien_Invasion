# A class to store all settings for Alien Invasion
class Settings:

    def __init__(self):     # Initialize the game's settings
        # Screen settings
        self.bg_color = (230, 230, 230)

        # Ship Setting
        self.ship_speed = 0.5
        self.ship_limit = 3

        # Bullet Setting
        self.bullet_speed = 1.0
        self.bullet_allowed = 3
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)

        # Alien Setting
        self.alien_speed = 0.5
        self.alien_drop_speed = 10
        self.fleet_direction = 1                         # 1 = Right, -1 = Left