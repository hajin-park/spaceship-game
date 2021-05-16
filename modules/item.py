#Powerups
import numpy as np
import pygame

from pygame.sprite import Sprite


class MysteryBox(Sprite):
    def __init__(self, main):
        super().__init__()
        self.main = main
        self.screen = main.screen
        self.screen_rect = self.screen.get_rect()
        self.mystery_box_images = [pygame.transform.scale(pygame.image.load('assets\mystery_box\doge_mystery_box_1.png').convert_alpha(), (32, 32)),
                                   pygame.transform.scale(pygame.image.load('assets\mystery_box\doge_mystery_box_2.png').convert_alpha(), (32, 32)),
                                   pygame.transform.scale(pygame.image.load('assets\mystery_box\doge_mystery_box_3.png').convert_alpha(), (32, 32)),
                                   pygame.transform.scale(pygame.image.load('assets\mystery_box\doge_mystery_box_4.png').convert_alpha(), (32, 32)),
                                   pygame.transform.scale(pygame.image.load('assets\mystery_box\doge_mystery_box_5.png').convert_alpha(), (32, 32)),
                                   pygame.transform.scale(pygame.image.load('assets\mystery_box\doge_mystery_box_6.png').convert_alpha(), (32, 32)),
                                   pygame.transform.scale(pygame.image.load('assets\mystery_box\doge_mystery_box_7.png').convert_alpha(), (32, 32)),
                                   pygame.transform.scale(pygame.image.load('assets\mystery_box\doge_mystery_box_8.png').convert_alpha(), (32, 32))]
        self.rect = self.mystery_box_images[0].get_rect()
        self.rect.x, self.rect.y = np.random.randint(50, 1230), np.random.randint(50, 670)
        self.mask = pygame.mask.from_surface(self.mystery_box_images[0])
        self.main.spatial_hashing.add_object((self.rect.x, self.rect.y), (self.rect.x + self.rect.width, self.rect.y + self.rect.height), self)

    # ------------------------------ Render mystery box
    def blitme(self):
        self.screen.blit(self.mystery_box_images[self.main.mystery_box_timer//4], self.rect)
        #pygame.draw.rect(self.screen, (255, 255, 255), self.rect, 1) #- Hitbox outline
 
class PowerUp(Sprite):
    def __init__(self, main, pos):
        super().__init__()
        self.main = main
        self.screen = main.screen
        self.screen_rect = self.screen.get_rect()
        self.image = pygame.transform.scale(pygame.image.load('assets\powerups\default.png').convert_alpha(), (32, 32))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pos
        self.mask = pygame.mask.from_surface(self.image)
        self.main.spatial_hashing.add_object((self.rect.x, self.rect.y), (self.rect.x + self.rect.width, self.rect.y + self.rect.height), self)

    # ------------------------------ Render powerup
    def blitme(self):
        self.screen.blit(self.image, self.rect)
        #pygame.draw.rect(self.screen, (255, 255, 255), self.rect, 1) #- Hitbox outline

class Shield(PowerUp):
    def __init__(self, main, pos):
        super().__init__(main, pos)
        self.shield_images = [pygame.transform.scale(pygame.image.load('assets\powerups\shield\powerup_shield_1.png').convert_alpha(), (48, 48)),
                              pygame.transform.scale(pygame.image.load('assets\powerups\shield\powerup_shield_2.png').convert_alpha(), (48, 48)),
                              pygame.transform.scale(pygame.image.load('assets\powerups\shield\powerup_shield_3.png').convert_alpha(), (48, 48)),
                              pygame.transform.scale(pygame.image.load('assets\powerups\shield\powerup_shield_4.png').convert_alpha(), (48, 48)),
                              pygame.transform.scale(pygame.image.load('assets\powerups\shield\powerup_shield_5.png').convert_alpha(), (48, 48))]
        self.mask = pygame.mask.from_surface(self.shield_images[0])
        self.rect = pygame.Rect(0, 0, 48, 48)
        self.rect.center = pos

    # ------------------------------ Render shield powerup
    def blitme(self):
        self.screen.blit(self.shield_images[self.main.powerup_timer//7], self.rect)
        #pygame.draw.rect(self.screen, (255, 255, 255), self.rect, 1) #- Hitbox outline

class Laser(PowerUp):
    def __init__(self, main, pos):
        super().__init__(main, pos)
        self.laser_images = [pygame.transform.scale(pygame.image.load('assets\powerups\shield\powerup_shield_1.png').convert_alpha(), (48, 48)),
                             pygame.transform.scale(pygame.image.load('assets\powerups\shield\powerup_shield_2.png').convert_alpha(), (48, 48)),
                             pygame.transform.scale(pygame.image.load('assets\powerups\shield\powerup_shield_3.png').convert_alpha(), (48, 48)),
                             pygame.transform.scale(pygame.image.load('assets\powerups\shield\powerup_shield_4.png').convert_alpha(), (48, 48)),
                             pygame.transform.scale(pygame.image.load('assets\powerups\shield\powerup_shield_5.png').convert_alpha(), (48, 48))]
        self.mask = pygame.mask.from_surface(self.shield_images[0])
        self.rect = pygame.Rect(0, 0, 48, 48)
        self.rect.x, self.rect.y = pos

    # ------------------------------ Render laser powerup
    def blitme(self):
        self.screen.blit(self.laser_images[self.main.powerup_timer//15], self.rect)
        #pygame.draw.rect(self.screen, (255, 255, 255), self.rect, 1) #- Hitbox outline
