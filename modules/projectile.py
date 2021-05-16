#Player projectiles
import pygame
from numpy import math

from pygame.sprite import Sprite


class Projectile(Sprite):
    def __init__(self, main):
        super().__init__()
        self.main = main
        self.settings = main.settings
        self.screen = main.screen
        self.screen_rect = self.screen.get_rect()
        self.p_angle = self.main.ship.ship_angle
        self.projectile = pygame.transform.scale(pygame.image.load('assets/projectiles/bullet.png').convert_alpha(), (8, 8))
        self.rect = self.projectile.get_rect()
        self.rect.center = main.ship.rect.center
        self.mask = pygame.mask.from_surface(self.projectile)
        self.y = float(self.rect.y)
        self.x = float(self.rect.x)
    
    # ------------------------------ Update bullet position and collisions
    def update(self):
        self.y += math.sin(self.p_angle * math.pi/180) * (self.settings.projectile_movement_speed * self.settings.UPDATE_TIME)
        self.x += math.cos(self.p_angle * math.pi/180) * (self.settings.projectile_movement_speed * self.settings.UPDATE_TIME)
        self.rect.x = self.x
        self.rect.y = self.y

        # ------------------------------ Check for screen boundaries
        for projectile in self.main.projectiles:
            if projectile.rect.bottom <= 0 or projectile.rect.bottom >= self.screen_rect.bottom or projectile.rect.x <= 0 or projectile.rect.x >= self.screen_rect.right:
                self.main._spawn_projectile_particles(projectile)
                self.main.projectiles.remove(projectile)
        
        # ------------------------------ Update spatial hashing / collisions
        self.main.spatial_hashing.add_object((self.rect.x, self.rect.y), (self.rect.x + self.rect.width, self.rect.y + self.rect.height), self)
        self.main.spatial_hashing.mystery_box_collision()
        self.main.spatial_hashing.remove_object((self.rect.x, self.rect.y), (self.rect.x + self.rect.width, self.rect.y + self.rect.height), self)

    # ------------------------------ Render projectile
    def blitme(self):
        self.screen.blit(self.projectile, self.rect)
        #pygame.draw.rect(self.screen, (255, 255, 255), self.rect, 1) #- Hitbox outline
