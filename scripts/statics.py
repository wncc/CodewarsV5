import pygame
from scripts.config import *

class GrassTile:
    def __init__(self, img, tile_size, display_size):
        self.tile_size = tile_size
        self.display_size = display_size

        self.img = pygame.transform.scale(img, (8*self.tile_size, 8*self.tile_size))

    def render(self, surf):
        
        for i in range(0, self.display_size[1], 8*self.tile_size):
            surf.blit(self.img,(-2*self.tile_size,i))
            surf.blit(self.img,(6*self.tile_size,i))

class RockTile:
    def __init__(self, img, tile_size, display_size):
        self.tile_size = tile_size
        self.display_size = display_size

        self.img = pygame.transform.scale(img, (10*self.tile_size, 10*self.tile_size))

    def render(self, surf):
        
        for i in range(-self.tile_size*4, self.display_size[0]-self.tile_size*4, self.tile_size):
            surf.blit(self.img,(i,-6*self.tile_size))
            surf.blit(self.img,(i,HEIGHT-7*self.tile_size))