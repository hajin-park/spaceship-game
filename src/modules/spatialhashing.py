#Spatial hashing
import pygame
import numpy
import modules.item
from modules.particle import Particle


class SpatialHashing:
    def __init__(self, main, cell_size):
        self.main = main
        self.screen = main.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = main.settings
        self.cells = {}
        self.min = (0, 0)
        self.max = main.settings.window_dimensions
        self.cell_size = cell_size
        self.width = self.max[0] / self.cell_size
        self.height = self.max[1] / self.cell_size
        self.buckets = self.width * self.height
        self.destroyed_mystery_boxes = set()
        self.destroyed_powerups = set()
        
    def hash(self, p1, p2): #p1-TopLeft p2-BottomRight
        cells = set()
        cellx = p1[0]//self.cell_size
        
        # ------------------------------ Return set of cells occupied by a rectangle
        while cellx * self.cell_size <= p2[0]:
            celly = p1[1]//self.cell_size
            while celly * self.cell_size <= p2[1]:
                cells.add((cellx, celly))
                celly += 1
            cellx += 1
        return cells

    # ------------------------------ Add object to cell(s) in the hash table
    def add_object(self, p1, p2, obj): #p1-TopLeft p2-BottomRight
        object_cells = self.hash(p1, p2)

        for cell in object_cells:
            if cell in self.cells:
                self.cells[cell].add(obj)
            else:
                tup = (obj,)
                self.cells[cell] = set(tup)

    # ------------------------------ Remove object from cell(s) in the hash table
    def remove_object(self, p1, p2, obj): #p1-TopLeft p2-BottomRight
        object_cells = self.hash(p1, p2)

        for cell in object_cells:
            if cell in self.cells:
                self.cells[cell].remove(obj)
                
                # ------------------------------ Remove empty cell(s) from hash table
                if not self.cells[cell]:
                    del self.cells[cell]

    # ------------------------------ Mystery box collisions
    def mystery_box_collision(self):

        # ------------------------------ Find all cells containing objects
        for value in self.cells.values():
            mystery_boxes = []
            projectiles = []
            add_objects = False

            # ------------------------------ Find projectile and mystery box objects
            for obj in value:
                if obj.__class__.__name__ ==  "Projectile":
                    projectiles.append(obj)
                    add_objects = True
                elif obj.__class__.__name__ ==  "MysteryBox":
                    mystery_boxes.append(obj)
    
            # ------------------------------ Check for mystery box collisions in projectile's cells
            if add_objects and mystery_boxes:
                collision_mystery_box = set()
                for projectile in projectiles:
                    for box in mystery_boxes:
                        if pygame.sprite.collide_mask(box, projectile):
                            collision_mystery_box.add(box)
                            self.main._spawn_mystery_box_particles(box)
                            self.main._spawn_projectile_particles(projectile)
                            projectile.kill()

                if collision_mystery_box:
                    self.destroyed_mystery_boxes.update(collision_mystery_box)

        # ------------------------------ Remove collided mystery boxes; spawn powerups
        for mystery_box in self.destroyed_mystery_boxes:
            self.remove_object((mystery_box.rect.x, mystery_box.rect.y), (mystery_box.rect.x + mystery_box.rect.width, mystery_box.rect.y + mystery_box.rect.height), mystery_box)
            self.main._spawn_powerup((mystery_box.rect.center[0], mystery_box.rect.center[1]))
            mystery_box.kill()

        self.destroyed_mystery_boxes.clear()

    # ------------------------------ Powerup collisions
    def powerup_collision(self):

        # ------------------------------ Find all cells containing objects
        for value in self.cells.values():
            powerups = []
            ships = []
            add_objects = False

            # ------------------------------ Find player ships and powerup objects
            for obj in value:
                if obj.__class__.__name__ ==  "Player":
                    ships.append(obj)
                    add_objects = True
                elif issubclass(obj.__class__, modules.item.PowerUp):
                    powerups.append(obj)
    
            # ------------------------------ Check for powerup collisions in ships's cells
            if add_objects and powerups:
                collision_powerup = set()
                for ship in ships:
                    for powerup in powerups:
                        if pygame.sprite.collide_mask(powerup, ship):
                            collision_powerup.add(powerup)

                if collision_powerup:
                    self.destroyed_powerups.update(collision_powerup)

        # ------------------------------ Remove collided powerups
        for powerup in self.destroyed_powerups:
            self.remove_object((powerup.rect.x, powerup.rect.y), (powerup.rect.x + powerup.rect.width, powerup.rect.y + powerup.rect.height), powerup)
            powerup.kill()

        self.destroyed_powerups.clear()
