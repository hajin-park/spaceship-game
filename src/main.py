"""
Astro Party Online Game
By Hajin and David
"""

import sys
import os
import time
import pygame

from numpy.random import randint
from modules.settings import Settings
from modules.fps import GetFPS
from modules.player import Player
from modules.projectile import Projectile
from modules.item import MysteryBox, Shield, PowerUp
from modules.spatialhashing import SpatialHashing
from modules.particle import Particle

os.environ["SDL_VIDEO_CENTERED"] = "1"


class AstroPartyOnline:

    # ------------------------------ Initialize game
    def __init__(self):

        pygame.init()
        pygame.display.set_caption("ASSTRO PARTY ONLINE TEST HPWIGGLER")
        pygame.mouse.set_cursor(*pygame.cursors.broken_x)

        self.settings = Settings(self)
        self.screen = pygame.display.set_mode(
            self.settings.window_dimensions, pygame.NOFRAME
        )
        self.screen_rect = self.screen.get_rect()
        self.clock = pygame.time.Clock()

        # ------------------------------ Modules
        self.spatial_hashing = SpatialHashing(self, 80)
        self.fps = GetFPS(self)
        self.ship = Player(self)

        # ------------------------------ Sprite groups
        self.projectiles = pygame.sprite.Group()
        self.mystery_boxes = pygame.sprite.Group()
        self.powerups = pygame.sprite.Group()
        self.engine_particles = []
        self.powerup_particles = []
        self.destroyed_mystery_box_particles = []
        self.destroyed_projectile_particles = []
        self.destroyed_ship_particles = []

        # ------------------------------ Game timers
        self.current_time = time.time()
        self.time = 0.0
        self.accumulator = 0.0
        self.powerup_timer = 0
        self.ship_timer = 0
        self.mystery_box_timer = 0
        self.engine_particle_timer = 0

        # ------------------------------ Flags
        self.mystery_box_collision = False
        self.projectile_collision = False
        self.ship_collision = False

    # ------------------------------ Start game
    def run_game(self):

        # ------------------------------ Main game loop
        while True:
            self.clock.tick(self.settings.framerate)
            self._update_delta()

            # ------------------------------ Update objects
            while self.accumulator >= self.settings.UPDATE_TIME:
                self.fps._update_fps()
                self._update_timers()
                self._check_events()
                self.ship._update_pos()
                self.projectiles.update()
                self._update_particles()

                self.time += self.settings.UPDATE_TIME
                self.accumulator -= self.settings.UPDATE_TIME

            # ------------------------------ Render objects
            self._update_screen()

    # ------------------------------ Respond to events and player inputs
    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                self._check_keydown(event)

            elif event.type == pygame.KEYUP:
                self._check_keyup(event)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                self._check_mouseclick(event)

    # ------------------------------ Check key press event
    def _check_keydown(self, event):
        if event.key == pygame.K_SPACE:
            self.spawn_mystery_box()

    # ------------------------------ Check key release event
    def _check_keyup(self, event):
        if event.key == pygame.K_ESCAPE:
            sys.exit()
        elif event.key == pygame.K_d:
            self.ship.moving_right = False
        elif event.key == pygame.K_a:
            self.ship.moving_left = False
        elif event.key == pygame.K_w:
            self.ship.moving_up = False
        elif event.key == pygame.K_s:
            self.ship.moving_down = False

    # ------------------------------ Check mouse events
    def _check_mouseclick(self, event):
        if event.button == 1:
            self._fire_bullet()

    # ------------------------------ Spawn ship projectile
    def _fire_bullet(self):
        new_projectile = Projectile(self)
        self.projectiles.add(new_projectile)

    # ------------------------------ Manage framerate independency
    def _update_delta(self):
        new_time = time.time()
        frame_time = new_time - self.current_time

        if frame_time > 0.1:
            frame_time = 0.1

        self.current_time = new_time
        self.accumulator += frame_time

    # ------------------------------ Spawn mystery box (random location)
    def spawn_mystery_box(self):
        new_mystery_box = MysteryBox(self)
        self.mystery_boxes.add(new_mystery_box)

    # ------------------------------ Spawn random powerup from mystery box
    def _spawn_powerup(self, pos):
        random_powerup = randint(0, 1)
        glitch_chance = randint(0, 500)

        if random_powerup == 0 and glitch_chance != 0:
            new_powerup = Shield(self, pos)
            self.powerups.add(new_powerup)

        elif random_powerup == 1 and glitch_chance != 0:
            pass

        elif random_powerup == 2 and glitch_chance != 0:
            pass

        elif random_powerup == 3 and glitch_chance != 0:
            pass

        elif random_powerup == 4 and glitch_chance != 0:
            pass

        else:
            new_powerup = PowerUp(self, pos)
            self.powerups.add(new_powerup)

    # ------------------------------ Update / remove particles
    def _update_particles(self):
        for particle in self.engine_particles:
            particle.update()
            if particle.particle.get_alpha() <= 0:
                self.engine_particles.remove(particle)

        for particle in self.destroyed_mystery_box_particles:
            particle.update()
            if particle.particle.get_alpha() <= 0:
                self.destroyed_mystery_box_particles.remove(particle)

        for particle in self.destroyed_projectile_particles:
            particle.update()
            if particle.particle.get_alpha() <= 0:
                self.destroyed_projectile_particles.remove(particle)

        for particle in self.destroyed_ship_particles:
            particle.update()
            if particle.particle.get_alpha() <= 0:
                self.destroyed_ship_particles.remove(particle)

    # ------------------------------ Spawn ship engine particles
    def _spawn_engine_particles(self, ship):
        for _ in range(randint(1, 3)):
            new_particle = Particle(
                self,
                (
                    ship.rect.center[0] + (randint(0, 7) - 6),
                    ship.rect.center[1] + (randint(0, 7) - 6),
                ),
                randint(2, 6),
                (255, randint(155, 256), 0),
                (
                    -self.ship.vel.x * self.settings.UPDATE_TIME,
                    -self.ship.vel.y * self.settings.UPDATE_TIME,
                ),
                (10, 15),
            )  # - (pos, size, color, vel, duration)
            self.engine_particles.append(new_particle)

    # ------------------------------ Spawn mystery box collision particles
    def _spawn_mystery_box_particles(self, box):
        for _ in range(randint(8, 13)):
            new_particle = Particle(
                self,
                box.rect.center,
                randint(2, 6),
                (randint(0, 256), randint(0, 256), randint(0, 256)),
                (randint(0, 120) / 20 - 3, randint(0, 120) / 20 - 3),
                (5, 10),
            )  # - (pos, size, color, vel, duration)
            self.destroyed_mystery_box_particles.append(new_particle)

    # ------------------------------ Spawn projectile collision particles
    def _spawn_projectile_particles(self, projectile):
        for _ in range(randint(50, 100)):
            new_particle = Particle(
                self,
                projectile.rect.center,
                randint(2, 6),
                (255, randint(155, 256), 0),
                (randint(60, 200) / 20 - 3, randint(60, 200) / 20 - 3),
                (8, 13),
            )  # - (pos, size, color, vel, duration)
            self.destroyed_projectile_particles.append(new_particle)

    # ------------------------------ Manage timers
    def _update_timers(self):
        self.ship_timer += 1
        self.ship_timer %= 30

        self.mystery_box_timer += 1
        self.mystery_box_timer %= 32

        self.powerup_timer += 1
        self.powerup_timer %= 35

        self.engine_particle_timer += 1
        self.engine_particle_timer %= randint(5, 8)

    # ------------------------------ Render game objects and screen
    def _update_screen(self):
        self.screen.fill((0, 0, 70))

        for projectile in self.projectiles.sprites():
            projectile.blitme()

        for mystery_box in self.mystery_boxes.sprites():
            mystery_box.blitme()

        for powerup in self.powerups.sprites():
            powerup.blitme()

        for particle in self.engine_particles:
            particle.blitme()

        for particle in self.destroyed_projectile_particles:
            particle.blitme()

        for particle in self.destroyed_mystery_box_particles:
            particle.blitme()

        self.ship.blitme()
        self.fps.blitme()

        pygame.display.flip()


if __name__ == "__main__":
    AstroPartyOnline().run_game()
