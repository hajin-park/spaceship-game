#Game settings


class Settings:

    def __init__(self, main):
        # ------------------------------ Game render settings
        self.window_dimensions = (1920, 1080)
        self.framerate = 120 # - Framerate cap
        self.UPDATE_TIME = 1/60 # - Refresh rate

        # ------------------------------ Player ship settings
        self.player_speed = 40
        self.player_friction = -0.1
        self.wall_bounce = 0
        self.player_lives = 1
        self.max_ammo = 2

        # ------------------------------ Bullet settings
        self.projectile_movement_speed = 500
        self.projectile_reload_speed = 500
