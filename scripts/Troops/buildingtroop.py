import math
import pygame
from scripts.game_config import *

class BuildingTroop:
    def __init__(self, name, position, image, image_attack, elixir, health, damage, type_, size, surf, attack_range, attack_speed, std_size,myTower, splash_range=0):
        """
        Initialize a building troop with essential attributes.
        """
        self.name = name
        self.position = position
        self.size = size * std_size
        self.elixir = elixir
        self.type = type_
        self.health = health
        self.dummy = None
        self.damage = damage
        self.attack_speed = attack_speed
        self.attack_range = attack_range * std_size/2
        self.splash_range = splash_range * std_size/2
        self.target_type = {"air": False, "ground": True, "building": False}
        self.target = None
        self.discovered_troops = {}
        self.myTower = myTower
        self.surf = surf

        self.attack_counter = attack_speed

        aspect_ratio = image.get_height() / image.get_width()
        self.image = pygame.transform.scale(image, (2*self.size, int(2*self.size * aspect_ratio)))
        self.image_width = self.image.get_width()
        self.image_height = self.image.get_height()

        aspect_ratio = image_attack.get_height() / image_attack.get_width()
        self.image_attack = pygame.transform.scale(image_attack, (2*self.size, int(2*self.size * aspect_ratio)))
        self.image_attack_width = self.image.get_width()
        self.image_attack_height = self.image.get_height()

    def do_work(self):
        """The main function to be called for the troop in every frame."""
        self.discover_targets()

        if self.target:
            if self.target.health <= 0:
                self.target = None
            else:
                if self.is_in_range(self.target, self.attack_range):
                    if (self.attack_counter == self.attack_speed):
                        self.attack()
                        self.attack_counter = 0
                        self.render_attack()
                    else:
                        self.attack_counter += 1
                        self.render()
                    return
                self.target = None
                self.attack_counter = 0

        self.render()
        self.find_target()

    def discover_targets(self):
        """Discover troops within range and update the `self.discovered_troops` dictionary."""
        self.discovered_troops.clear()
        if not self.target:
            for entity in self.myTower.oppTroops:
                if self.target_type.get(entity.type, False):
                    distance = self.calculate_distance(entity.position)
                    self.discovered_troops[entity] = distance

    def find_target(self):
        """Finds the nearest target within range and sets it as the current target."""
        if self.discovered_troops and not self.target:
            nearest = min(self.discovered_troops.items(), key=lambda item: item[1])
            nearest_entity, nearest_distance = nearest
            if self.is_in_range(nearest_entity, self.attack_range):
                self.target = nearest_entity

    def attack(self):
        """Attacks the current target."""
        if self.splash_range > 0:
            self.apply_splash_damage()
        else:
            self.target.health -= self.damage
        if self.target.health <= 0:
            self.target = None
    
    def die(self):
        if self.health <= 0:
            self.myTower.myTroops.remove(self)

    # ANIMATION FUNCTION

    def render(self):
        x = self.position[0] 
        y = self.position[1] 
        self.surf.blit(self.img, (x, y))

    def render_attack(self):
        x = self.position[0] - self.size 
        y = self.position[1] - self.size 
        self.surf.blit(self.image_attack, (x, y))

    # UTILITY FUNCTION

    def is_in_range(self, entity, range_):
        """Checks if an entity is within the specified range."""
        return self.calculate_distance(entity.position) <= range_ + self.size + entity.size

    def calculate_distance(self, other_position):
        """Calculates the Euclidean distance to another position."""
        return math.sqrt((self.position[0] - other_position[0])**2 + (self.position[1] - other_position[1])**2)

    def apply_splash_damage(self):
        """Applies splash damage to all entities within the splash radius."""
        for entity in self.myTower.oppTroops + [self.myTower.oppTower]:
            if self.is_in_range(entity, self.splash_range):
                entity.health -= self.damage