import os
import pygame
from scripts.config import *
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
        x = position[0]*50/ARENA_WIDTH
        y = position[0]*100/ARENA_WIDTH
        return(x,y)

    x = position[0]*ARENA_WIDTH/50
    y = position[1]*ARENA_HEIGHT/100
    return (x,y)

def get_positions(position, area, troop_deploy_radius, troop_number):
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
    for _ in range(troop_number):
        angle = random.uniform(0, 2 * math.pi)
        radius = math.sqrt(random.uniform(0, troop_deploy_radius**2))
        rand_x = deploy_x + radius * math.cos(angle)
        rand_y = deploy_y + radius * math.sin(angle)
        arr.append((rand_x, rand_y))
        
    return arr
    