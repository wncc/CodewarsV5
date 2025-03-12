import pygame
from scripts.game_config import *

class Middle_Map:
    def __init__(self, img):
        self.img = pygame.transform.scale(img, (MIDDLE_WIDTH,MIDDLE_HEIGHT))
    def render(self,surf):
        surf.blit(self.img,(0,0))
