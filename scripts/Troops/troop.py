import math
import pygame
from scripts.game_config import *

class Troop:
    def __init__(self, name, images, position, elixir, health, damage, velocity, type_, attack_range, attack_speed,
                 discovery_range, myTower, target_type, std_size, uid, splash_range = 0, size = 0, number = 1):
        """
        Initialize a troop with essential attributes.
        """
        self.name = name
        self.position = position
        self.prev_position = position
        self.elixir = elixir
        self.type = type_
        self.number = number
        self.std_size = std_size
        self.size = std_size*size
        self.deploy_radius = 3*self.size
        self.dummy = None
        self.health = health
        self.max_health = health
        self.damage = damage
        self.velocity = velocity
        self.attack_range = attack_range * std_size/5
        self.discovery_range = discovery_range * std_size/5
        self.splash_range = splash_range * std_size/5
        self.target_type = target_type
        self.attack_speed = attack_speed
        self.target = None
        self.myTower = myTower
        self.surf = self.myTower.arena_surf
        self.shadow_surf = self.myTower.shadow_surf
        self.discovered_troops = {}
        self.assets = images
        self.images = {}
        self.uid = uid

        self.attack_counter = 0
        self.orientation = "s"
        self.run_counter = 0

        self.xx, self.yy, self.w, self. h = CENTERS.loc[name.lower()]

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

                    if (self.attack_counter+1 == self.attack_speed*FRAMES):
                        self.attack()
                    self.render_attack()
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
                    self.attack_counter = 0
                    return
                self.move_towards(nearest_entity.position)

            else:
                if abs(self.position[1] - self.myTower.oppTower.position[1]) >= ARENA_HEIGHT/2:
                    straight_position = (self.position[0],self.myTower.oppTower.position[1])
                    self.move_towards(straight_position)
                else:
                    self.move_towards(self.myTower.oppTower.position)

        else:
            if abs(self.position[1] - self.myTower.oppTower.position[1]) >= ARENA_HEIGHT/2:
                    straight_position = (self.position[0],self.myTower.oppTower.position[1])
                    self.move_towards(straight_position)
            else:
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
        y_health_bar = self.position[1] - self.h
        if self.type == 'air':
            y_health_bar -= AIR_HEIGHT/2
        pygame.draw.rect(self.surf, (65,76,78), (self.position[0] - self.size + PADDING_X, y_health_bar + PADDING_Y, 2*self.size, 0.08*self.std_size), 0)
        if self.myTower.troop2:
            pygame.draw.rect(self.surf, (200, 57, 90), (self.position[0] - self.size + PADDING_X, y_health_bar + PADDING_Y, 2*self.size * self.health/self.max_health, 0.08*self.std_size), 0)
        else:
            pygame.draw.rect(self.surf, (73,152,196), (self.position[0] - self.size + PADDING_X, y_health_bar + PADDING_Y, 2*self.size * self.health/self.max_health, 0.08*self.std_size), 0)


    def render(self):
        frames = (TOP_SPEED-self.velocity)*FRAMES
        rendering_frame = self.run_counter//(TOP_SPEED-self.velocity)
        x = self.position[0] -  self.xx - self.size
        y = self.position[1] - self.yy - self.h + self.size/2
        y_shadow = y
        if self.type == 'air':
            y -= AIR_HEIGHT/2
            y_shadow += AIR_HEIGHT/2
        self.shadow_surf.blit(self.images["_run_"+self.orientation+f"_{rendering_frame+1}_shadow"],(x + PADDING_X, y_shadow + PADDING_Y))
        self.surf.blit(self.images["_run_"+self.orientation+f"_{rendering_frame+1}"],(x + PADDING_X, y + PADDING_Y))
        self.run_counter = (self.run_counter+1)%frames
        self.render_health_bar()

    def render_attack(self):
        frames = (self.attack_speed)*FRAMES
        rendering_frame = self.attack_counter//(self.attack_speed)
        x = self.position[0] - self.xx - self.size
        y = self.position[1] - self.yy - self.h + self.size/2
        y_shadow = y
        if self.type == 'air':
            y -= AIR_HEIGHT/2
            y_shadow += AIR_HEIGHT/2
        self.shadow_surf.blit(self.images["_attack_"+self.orientation+f"_{rendering_frame+1}_shadow"],(x + PADDING_X, y_shadow + PADDING_Y))
        self.surf.blit(self.images["_attack_"+self.orientation+f"_{rendering_frame+1}"],(x + PADDING_X, y + PADDING_Y))
        self.attack_counter = (self.attack_counter+1)%frames
        self.render_health_bar()
    
    # UTILITY FUNCTION

    def resize(self):
        orientation = ["n","s", "e", "w", "ne", "nw", "se", "sw"]
        std_img = self.assets[self.name.lower()+"_run_n_6"]
        original_Width = std_img.get_width()
        original_Height = std_img.get_height()
        aspect_ratio = self.h/self.w
        new_width = 2*self.size
        new_height = new_width*aspect_ratio
        new_Width = new_width*original_Width/self.w
        new_Height = new_height*original_Height/self.h
        self.xx = self.xx * new_width/self.w
        self.yy = self.yy * new_height/self.h
        self.h = new_height
        for i in range(6):
            for orient in orientation:
                image = self.assets[self.name.lower()+"_run_"+orient+f'_{i+1}']
                image_scaled = pygame.transform.scale(image, (new_Width, new_Height))
                self.images["_run_"+orient+f'_{i+1}'] = image_scaled

                image_attack = self.assets[self.name.lower()+"_attack_"+orient+f'_{i+1}']
                image_attack_scaled = pygame.transform.scale(image_attack, (new_Width, new_Height))
                self.images["_attack_"+orient+f'_{i+1}'] = image_attack_scaled

                image_shadow = self.assets[self.name.lower()+"_run_"+orient+f'_{i+1}_shadow']
                image_shadow_scaled = pygame.transform.scale(image_shadow, (new_Width, new_Height*1.3))
                self.images["_run_"+orient+f'_{i+1}_shadow'] = image_shadow_scaled

                image_attack_shadow = self.assets[self.name.lower()+"_attack_"+orient+f'_{i+1}_shadow']
                image_attack_shadow_scaled = pygame.transform.scale(image_attack_shadow, (new_Width, new_Height*1.3))
                self.images["_attack_"+orient+f'_{i+1}_shadow'] = image_attack_shadow_scaled
              
    def is_in_range(self, entity, range_):
        """Checks if an entity is within the troop's discovery or attack range."""
        return self.calculate_distance(entity.position) <= range_ + self.size + entity.size
    
    def in_target_range(self, troop):
        return ((self.target.position[0]-troop.position[0])**2+(self.target.position[1]-troop.position[1])**2) <= self.splash_range**2
 
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

        angle = math.degrees(math.atan2(-dy, dx))
        angle = (angle + 360) % 360

        if -22.5 <= angle < 22.5:
            self.orientation = "e"
        elif 22.5 <= angle < 67.5:
            self.orientation = "ne"
        elif 67.5 <= angle < 112.5:
            self.orientation = "n"
        elif 112.5 <= angle < 157.5:
            self.orientation = "nw"
        elif 157.5 <= angle < 202.5:
            self.orientation = "w"
        elif 202.5 <= angle < 247.5:
            self.orientation = "sw"
        elif 247.5 <= angle < 292.5:
            self.orientation = "s"
        elif 292.5 <= angle < 337.5:
            self.orientation = "se"

    def apply_splash_damage(self):
        """Applies splash damage to all entities within the splash radius."""
        for entity in self.myTower.oppTroops + [self.myTower.oppTower]:
            if self.in_target_range(entity):
                entity.health -= self.damage