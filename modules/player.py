#Player ships
import pygame
from numpy import math
vec = pygame.math.Vector2


class Player:
    def __init__(self, main):
        super().__init__()  
        self.main = main
        self.settings = main.settings
        self.screen = main.screen
        self.screen_rect = main.screen.get_rect()
        self.ship_images  = [pygame.transform.scale(pygame.image.load('assets/ship/player_ship_1.png').convert_alpha(), (32, 32)), 
                             pygame.transform.scale(pygame.image.load('assets/ship/player_ship_2.png').convert_alpha(), (32, 32)), 
                             pygame.transform.scale(pygame.image.load('assets/ship/player_ship_3.png').convert_alpha(), (32, 32))]
        self.ship = self.ship_images[0]
        self.rect = self.ship_images[0].get_rect()
        self.rect.center = self.screen_rect.center
        self.y = float(self.rect.centery)
        self.x = float(self.rect.centerx)
        self.previous_mouse_pos = pygame.mouse.get_pos()
        self.pos = (self.screen_rect.centerx, self.screen_rect.centery)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        x2, y2 = pygame.mouse.get_pos()
        self.ship_angle = round(math.atan2(y2 - self.y, x2 - self.x) * (180 / math.pi), 4)
        self.mask = pygame.mask.from_surface(self.ship_images[0])

    # ------------------------------ Turn ship towards the cursor
    def _update_angle(self):
        
        # ------------------------------ If cursor is still ship continues in one direction
        if self.previous_mouse_pos != pygame.mouse.get_pos():
            x2, y2 = pygame.mouse.get_pos()
            self.ship_angle = round(math.atan2(y2 - self.y, x2 - self.x) * (180 / math.pi), 4)
        
        self.ship = pygame.transform.rotate(self.ship_images[self.main.ship_timer//10], -self.ship_angle - 90)
        self.mask = pygame.mask.from_surface(self.ship)
        self.previous_mouse_pos = pygame.mouse.get_pos()

    # ------------------------------ Update ships location
    def _update_pos(self):
        self._update_angle()
        self.acc = vec(0, 0)

        self.vel.y += math.sin(self.ship_angle * math.pi/180) * (self.settings.player_speed * self.settings.UPDATE_TIME)
        self.vel.x += math.cos(self.ship_angle * math.pi/180) * (self.settings.player_speed * self.settings.UPDATE_TIME)

        self.acc += self.vel * (self.settings.player_friction)
        self.vel += self.acc
        self.pos += self.vel
        self.x = self.pos.x
        self.y = self.pos.y
        self.rect.centerx = self.x
        self.rect.centery = self.y

        # ------------------------------ Check for screen boundaries, bounce ship
        if self.pos.x < self.screen_rect.left + 20:
            self.pos.x = self.screen_rect.left + 20
            #self.vel.x = self.settings.wall_bounce * self.settings.UPDATE_TIME
        elif self.pos.x > self.screen_rect.right - 20:
            self.pos.x = self.screen_rect.right - 20
            #self.vel.x = -self.settings.wall_bounce * self.settings.UPDATE_TIME
        if self.pos.y < self.screen_rect.top + 20:
            self.pos.y = self.screen_rect.top + 20
            #self.vel.y = self.settings.wall_bounce * self.settings.UPDATE_TIME
        elif self.pos.y > self.screen_rect.bottom - 20:
            self.pos.y = self.screen_rect.bottom - 20
            #self.vel.y = -self.settings.wall_bounce * self.settings.UPDATE_TIME

        if self.main.engine_particle_timer == 1:
            self.main._spawn_engine_particles(self)

        # ------------------------------ Update spatial hashing / collisions
        self.main.spatial_hashing.add_object((self.rect.x, self.rect.y), (self.rect.x + self.rect.width, self.rect.y + self.rect.height), self)
        self.main.spatial_hashing.powerup_collision()
        self.main.spatial_hashing.remove_object((self.rect.x, self.rect.y), (self.rect.x + self.rect.width, self.rect.y + self.rect.height), self)

    # ------------------------------ Render ship
    def blitme(self):
        self.screen.blit(self.ship, (self.pos[0] - int(self.ship.get_width() / 2), self.pos[1] - int(self.ship.get_height() / 2)))
        #pygame.draw.rect(self.screen, (255, 255, 255), self.rect, 1) #- Hitbox outline
