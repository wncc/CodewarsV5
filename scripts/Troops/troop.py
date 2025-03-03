import math
import pygame
from scripts.config import *

class Troop:
    def __init__(self, name, images, position, elixir, health, damage, velocity, type_, attack_range, attack_speed, surf,
                 discovery_range, myTower, target_type, std_size, splash_range = 0, size = 0):
        """
        Initialize a troop with essential attributes.
        """
        self.name = name
        self.position = position
        self.prev_position = position
        self.elixir = elixir
        self.type = type_
        self.size = std_size*size
        self.dummy = None
        self.health = health
        self.max_health = health
        self.damage = damage
        self.velocity = velocity
        self.attack_range = attack_range * std_size/4
        self.discovery_range = discovery_range * std_size/4
        self.splash_range = splash_range * std_size/4
        self.target_type = target_type
        self.attack_speed = attack_speed
        self.target = None
        self.myTower = myTower
        self.surf = surf
        self.discovered_troops = {}
        self.assets = images
        self.images = {}

        self.attack_counter = attack_speed
        self.orientation = "Front"

        self.resize()

    # CORE FUNCTIONS
    def update_position(self):
        self.position = self.prev_position      # update position

    def do_work(self):
        """The main function to be called for the troop in every frame."""
        self.discover_targets()
        
        if self.target:
            if self.target.health <= 0:
                self.target = None
            else:
                if self.is_in_range(self.target, self.attack_range):
                    
                    self.update_orientation()

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
        self.move()

    def discover_targets(self):
        """Discover troops and towers within range."""
        self.discovered_troops.clear()
        if not self.target:
            self.discovered_troops[self.myTower.oppTower] = self.calculate_distance(self.myTower.oppTower.position)
            for entity in self.myTower.oppTroops:
                if self.target_type.get(entity.type, False):
                    distance = self.calculate_distance(entity.position)
                    self.discovered_troops[entity] = distance

    def move(self):
        """Moves the troop towards the closest target if no target is set."""            
        if self.discovered_troops and not self.target:
            nearest = min(self.discovered_troops.items(), key=lambda item: item[1])
            nearest_entity, nearest_distance = nearest
            if self.is_in_range(nearest_entity, self.discovery_range):
                if self.is_in_range(nearest_entity, self.attack_range):
                    self.target = nearest_entity
                    return
                self.move_towards(nearest_entity.position)

            else:
                straight_position = (self.position[0],self.myTower.oppTower.position[1])
                self.move_towards(self.myTower.oppTower.position)

        else:
            straight_position = (self.position[0],self.myTower.oppTower.position[1])
            self.move_towards(self.myTower.oppTower.position)


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

    def render_health_bar(self):  # need to work on positioning since self.size is gonna have some new definition
        pygame.draw.rect(self.surf, (255,0,0), (self.position[0] + PADDING, self.position[1] + 0.5*self.size , 1*self.size, 0.05*self.size), 0)
        pygame.draw.rect(self.surf, (0,255,0), (self.position[0] + PADDING, self.position[1] + 0.5*self.size , 1*self.size * self.health/self.max_health, 0.05*self.size), 0)


    def render(self):
        x = self.position[0] - self.size + PADDING
        y = self.position[1] - self.size + PADDING
        self.surf.blit(self.images[self.orientation],(x, y))

    def render_attack(self):
        x = self.position[0] - self.size + PADDING
        y = self.position[1] - self.size + PADDING
        self.surf.blit(self.images[self.orientation+"Attack"],(x, y))
    
    # UTILITY FUNCTION

    def resize(self):
        orientation = ["Front","Back"]
        for orient in orientation:
            image = self.assets[self.name+orient]
            aspect_ratio = image.get_height() / image.get_width()
            image_scaled = pygame.transform.scale(image, (2*self.size, int(2*self.size * aspect_ratio)))
            self.images[orient] = image_scaled

            image_attack = self.assets[self.name+orient+"Attack"]
            aspect_ratio = image_attack.get_height() / image_attack.get_width()
            image_attack_scaled = pygame.transform.scale(image_attack, (2*self.size, int(2*self.size * aspect_ratio)))
            self.images[orient+"Attack"] = image_attack_scaled
              
    def is_in_range(self, entity, range_):
        """Checks if an entity is within the troop's discovery or attack range."""
        return self.calculate_distance(entity.position) <= range_ + self.size + entity.size

    def calculate_distance(self, other_position):
        """Calculates the Euclidean distance to another position."""
        return math.sqrt((self.position[0] - other_position[0])**2 + (self.position[1] - other_position[1])**2)

    def move_towards(self, target_position):
        """Moves the troop towards a target position."""
        dx, dy = target_position[0] - self.position[0], target_position[1] - self.position[1]
        self.update_orientation(target_position)
        distance = math.sqrt(dx**2 + dy**2)
        if distance > 0:
            self.prev_position = (
                self.position[0] + self.velocity * dx / distance,
                self.position[1] + self.velocity * dy / distance
            )

    def update_orientation(self, target_position = None):
        if self.target:
            dx, dy = self.target.position[0] - self.position[0], self.target.position[1] - self.position[1]
        else:
            dx, dy = target_position[0] - self.position[0], target_position[1] - self.position[1]
        
        if dy>0:
            self.orientation = "Front"
        elif dy<0:
            self.orientation = "Back"

    def apply_splash_damage(self):
        """Applies splash damage to all entities within the splash radius."""
        for entity in self.myTower.oppTroops + [self.myTower.oppTower]:
            if self.is_in_range(entity, self.splash_range):
                entity.health -= self.damage