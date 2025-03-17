import os
import pygame
from scripts.game_config import *
import math
import random

BASE_IMG_PATH = 'data/images/'

def load_image(path, color_key = None):
    img = pygame.image.load(BASE_IMG_PATH + path).convert_alpha()
    if color_key:
        img.set_colorkey(color_key)
    return img

def load_images(path):
    images = []
    for img_name in sorted(os.listdir(BASE_IMG_PATH + path)):
        images.append(load_image(path + '/' + img_name))
    return images

def convert_player2(position,display_size):  # convert player2 perspective to player1 (game engine) perspective
    x = display_size[0] - position[0]
    y = display_size[1] - position[1]
    return (x,y)

def convert_player2_area(area,display_size:tuple):
    x1 = display_size[0] - area[0]
    x2 = display_size[0] - area[1]
    y1 = display_size[1] - area[2]
    y2 = display_size[1] - area[3]
    return (x2,x1,y2,y1)  # bcz x2<x1 and y2<y1

def rescale_position(position,reverse = False):
    if reverse:
        x = position[0]*50/ARENA_WIDTH - 25
        y = 100 - position[1]*100/ARENA_HEIGHT
        return(x,y)

    x = (position[0]+25)*ARENA_WIDTH/50
    y = (100-position[1])*ARENA_HEIGHT/100
    return (x,y)

def get_positions(position, area, troop_deploy_radius, troop_number, troop2):
    if area[0] >= position[0] - troop_deploy_radius:
        deploy_x = area[0] + troop_deploy_radius
    elif position[0] + troop_deploy_radius >= area[1]:
        deploy_x = area[1] - troop_deploy_radius
    else:
        deploy_x = position[0]

    if area[2] >= position[1] - troop_deploy_radius:
        deploy_y = area[2] + troop_deploy_radius
    elif position[1] + troop_deploy_radius >= area[3]:
        deploy_y = area[3] - troop_deploy_radius
    else:
        deploy_y = position[1]

    arr = []
    
    grid_rows = math.ceil(math.sqrt(troop_number))
    grid_cols = (troop_number + grid_rows - 1) // grid_rows
    
    spacing_x = troop_deploy_radius / (grid_cols - 1) if grid_cols > 1 else 0
    spacing_y = troop_deploy_radius / (grid_rows - 1) if grid_rows > 1 else 0

    flip_y = 1 if troop2 else -1
    flip_x = 1 if troop2 else -1
    
    start_x = deploy_x - (grid_cols // 2) * spacing_x * flip_x
    start_y = deploy_y - (grid_rows // 2) * spacing_y * flip_y

    count = 0
    for i in range(grid_rows):
        for j in range(grid_cols):
            if count < troop_number:
                x = start_x + (j * spacing_x * flip_x)
                y = start_y + (i * spacing_y * flip_y)
                arr.append((x, y))
                count += 1

    return arr
    