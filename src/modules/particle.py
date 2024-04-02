#Particles
import pygame
import numpy
from numpy.random import randint


class Particle:
    def __init__(self, main, pos, size, color, vel, duration):
        self.main = main
        self.screen = main.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = main.settings

        self.vel = vel
        if self.vel == (0, 0):
            self.vel = (randint(0, 120) / 20 - 3, randint(0, 120) / 20 - 3)

        self.particle = pygame.Surface((size, size))
        self.particle.fill(color)
        self.rect = self.particle.get_rect()
        self.center = pos
        self.rect.center = self.center
        self.duration = duration
        self.fade = 255

    # ------------------------------ Update particle alpha (transparency)
    def update(self):
        self.rect.x += self.vel[0] * self.settings.UPDATE_TIME
        self.rect.y += self.vel[1] * self.settings.UPDATE_TIME
        self.particle.set_alpha(self.fade)
        self.fade -= numpy.random.randint(self.duration[0], self.duration[1])
        if self.fade < 0:
            self.fade = 0

    # ------------------------------ Render particle
    def blitme(self):
        self.screen.blit(self.particle, self.rect)
