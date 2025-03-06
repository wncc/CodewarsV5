import pygame
from scripts.config import *

class Arena:
    def __init__(self, img):
        self.img = pygame.transform.scale(img, (ARENA_WIDTH,ARENA_HEIGHT))
    def render(self,surf):
        surf.blit(self.img,(0,0))

class Middle_Map:
    def __init__(self, img):
        self.img = pygame.transform.scale(img, (MIDDLE_WIDTH,MIDDLE_HEIGHT))
    def render(self,surf):
        surf.blit(self.img,(0,0))
