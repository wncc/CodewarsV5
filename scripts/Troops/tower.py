import math
import pygame
from scripts.game_config import *
from scripts.Troops.troops import *
from config import VALUE_ERROR
from scripts.utils import get_positions

class Tower:
    def __init__(self, name, position, assets, size, deploy_area, arena_surf, surf_shadow, middle_surf, deployable_troops, troop2 = False):
        """
        Initialize a tower with essential attributes.

        :param position: Fixed coordinates (x, y).
        :param health: Health of the tower.
        :param damage: Damage dealt per attack.
        :param attack_range: Attack range in tiles.
        """
        self.name = name
        self.assets = assets
        if troop2:
            self.image_tower = assets['RedTower']
            self.image_tower_shadow = assets['RedTower_shadow']
            self.image_cannon = assets['RedCannon']
        else:
            self.image_tower = assets['BlueTower']
            self.image_tower_shadow = assets['BlueTower_shadow']
            self.image_cannon = assets['BlueCannon']
        self.image_destroyed = assets['TowerDamaged']
        self.position = position
        self.health = 7032
        self.max_health = 7032
        self.damage = 158
        self.attack_range = 10 * size/4
        self.dummy = None
        self.target = None
        self.size = size        # size = radius i.e. distance from center
        self.deploy_area = deploy_area
        self.shadow_surf = surf_shadow
        self.middle_surf = middle_surf
        self.arena_surf = arena_surf
        self.attack_speed = FAST_ATTACK
        self.velocity = FAST_SPEED
        self.deployable_troops = deployable_troops
        self.discovered_troops = {}
        self.tower_in_range = 0.0

        self.troop2 = troop2        # rendering purpose only
        self.game_timer = 0

        self.attack_counter = 0
        self.run_counter = 0
        
        # Initialize user resources
        self.total_elixir = 10 
        self.total_dark_elixir = 0
        self.oppTower:Tower = None
        self.myTroops = []
        self.oppTroops = None
        self.level = 1
        self.uid_maker = 1

        self.images = {}

        self.resize()

    # CORE FUNCTIONS

    def do_work(self):
        
        self.check_tie2()
        
        if self.total_elixir < 10:
            update_rate = 0.05
            if self.game_timer < FPS * 60:
                self.total_elixir += 1*update_rate  # Increasing elixir x1 in each frame
            elif self.game_timer < FPS * 120:
                self.total_elixir += 1*update_rate  # Increasing elixir x1 in each frame
            elif self.game_timer < FPS * 180:
                self.total_elixir += 2*update_rate  # Increasing elixir x2 in each frame
        if self.total_dark_elixir < 10:
            self.total_dark_elixir += 0.1  # Increasing dark elixir

        self.game_timer += 1

        self.discover_targets()

        if self.target:
            if self.target.health <= 0:
                self.target = None
            else:
                if self.is_in_range(self.target, self.attack_range):
                    if (self.attack_counter+1 == self.attack_speed*FRAMES):
                        self.attack()
                    self.render_attack()
                    return
                self.target = None
                self.attack_counter = 0

        self.render()
        self.find_target()

    def get_next_cycle(self,troop):
        self.deployable_troops.remove(troop)
        self.deployable_troops.append(troop)

    def discover_targets(self):
        self.discovered_troops.clear()
        if not self.target:
            for entity in self.oppTroops:
                distance = self.calculate_distance(entity.position)
                self.discovered_troops[entity] = distance

    def find_target(self):
        if self.discovered_troops and not self.target:
            nearest = min(self.discovered_troops.items(), key=lambda item: item[1])
            nearest_entity, nearest_distance = nearest
            if self.is_in_range(nearest_entity, self.attack_range):
                self.target = nearest_entity

    def attack(self):
        self.target.health -= self.damage
        if self.target.health <= 0:
            self.target = None
            
    def check_tie2(self):
        for troop in self.myTroops:
            if troop.is_in_range(self.oppTower,troop.attack_range):
                self.tower_in_range += 1/(troop.attack_range+1)

    def deploy(self, troop: str, position): # replace it with self.assets and then take name as key to get the corresponding image
        area = self.deploy_area
        """
        NOTE:
        4 TROOPS AVAILABLE ONLY
        """
        if troop in self.deployable_troops[:4]:
            if area[0] <= position[0] <= area[1] and area[2] <= position[1] <= area[3]:
                troop_class = globals()[troop]
                if self.troop2:
                    troop_instance = troop_class(position=position, myTower=self, images = self.assets["Red"], std_size = self.size, uid = self.uid_maker)
                else:
                    troop_instance = troop_class(position=position, myTower=self, images = self.assets["Blue"], std_size = self.size, uid = self.uid_maker)
                if self.total_elixir >= troop_instance.elixir:
                    self.total_elixir -= troop_instance.elixir
                    troop_number = troop_instance.number
                    troop_deploy_radius = troop_instance.deploy_radius
                    if troop_number == 1:
                        self.myTroops.append(troop_instance)
                        self.uid_maker += 1
                    else:
                        del troop_instance
                        positions = get_positions(position,area,troop_deploy_radius,troop_number, self.troop2)
                        for pos in positions:
                            if self.troop2:
                                troop_instance = troop_class(position=pos, myTower=self, images = self.assets["Red"], std_size = self.size, uid = self.uid_maker)
                            else:
                                troop_instance = troop_class(position=pos, myTower=self, images = self.assets["Blue"], std_size = self.size, uid = self.uid_maker)
                            self.myTroops.append(troop_instance)
                            self.uid_maker += 1
                    self.get_next_cycle(troop)
                else:
                    if VALUE_ERROR:
                        raise ValueError(f"Invalid Troop Deployment: Current elixers are not enough for {troop}")
            else:
                if VALUE_ERROR:
                    raise ValueError(f"Invalid Troop Deployment: {troop} is not in deployable area")
        else:
            if VALUE_ERROR:
                raise ValueError(f"Invalid Troop Deployment: {troop} is not in current deployable cycle")

    # UTILITY FUNCTION

    def is_in_range(self, entity, range_):
        """Checks if an entity is within the specified range."""
        return self.calculate_distance(entity.position) <= range_ + self.size + entity.size

    def calculate_distance(self, other_position):
        """Calculates the Euclidean distance to another position."""
        return math.sqrt((self.position[0] - other_position[0])**2 + (self.position[1] - other_position[1])**2)

    def level_up(self):
        pass

    def special_power(self, power):
        pass

    def resize(self):
        team = "Red" if self.troop2 else "Blue"
        for i in range(1,7):
            image = self.assets[team][f"{team}King_{i}"]
            aspect_ratio = image.get_height() / image.get_width()
            image_scaled = pygame.transform.scale(image, (3*self.size, int(3*self.size * aspect_ratio)))
            self.images["_run_"+f'{i}'] = image_scaled
            
            image_attack = self.assets[team][f"{team}KingAttack_{i}"]
            aspect_ratio = image_attack.get_height() / image_attack.get_width()
            image_attack_scaled = pygame.transform.scale(image_attack, (3*self.size, int(3*self.size * aspect_ratio)))
            self.images["_attack_"+f'{i}'] = image_attack_scaled

        aspect_ratio = self.image_cannon.get_height() / self.image_cannon.get_width()
        self.image_cannon = pygame.transform.scale(self.image_cannon, (3*self.size, int(3*self.size * aspect_ratio)))

        aspect_ratio = self.image_tower.get_height() / self.image_tower.get_width()
        self.image_tower = pygame.transform.scale(self.image_tower, (3*self.size, int(3*self.size * aspect_ratio)))
        self.image_tower_shadow = pygame.transform.scale(self.image_tower_shadow, (3*self.size, int(3*1.3*self.size * aspect_ratio)))

        aspect_ratio = self.image_destroyed.get_height() / self.image_destroyed.get_width()
        self.image_destroyed = pygame.transform.scale(self.image_destroyed, (3*self.size, int(3*self.size * aspect_ratio)))

        self.image_tower_height = self.image_tower.get_height()

    # ANIMATION FUNCTION

    def render_health_bar(self,position):  # need to work on positioning since self.size is gonna have some new definition
        pygame.draw.rect(self.middle_surf, (65,76,78), (position[0], position[1] , 2*self.size, 0.15*self.size), 0)
        if self.troop2:
            pygame.draw.rect(self.middle_surf, (200, 57, 90), (position[0], position[1], 2*self.size * self.health/self.max_health, 0.15*self.size), 0)
        else:
            pygame.draw.rect(self.middle_surf, (73,152,196), (position[0], position[1], 2*self.size * self.health/self.max_health, 0.15*self.size), 0)

    def render(self):
        frames = (TOP_SPEED-self.velocity)*FRAMES
        rendering_frame = self.run_counter//(TOP_SPEED-self.velocity)
        x = self.position[0] - 1.5*self.size + PADDING_X
        y = self.position[1] + 2*self.size - self.image_tower_height + PADDING_Y
        if self.health <= 0:
            self.middle_surf.blit(self.image_destroyed, (x, y))
            return
        self.middle_surf.blit(self.image_tower, (x, y))
        self.shadow_surf.blit(self.image_tower_shadow, (x, y-self.size*0.2))
        if self.troop2:
            self.middle_surf.blit(self.image_cannon,(x,y - self.size*0.2))
            self.render_health_bar((x+self.size/2,y))
        else:
            self.middle_surf.blit(self.image_cannon,(x,y - self.size*0.8))
            self.render_health_bar((x+self.size/2,y+2*self.size))
        self.middle_surf.blit(self.images["_run_"+f'{rendering_frame+1}'],(x, y - self.size*0.4))
        self.run_counter = (self.run_counter+1)%frames

    def render_attack(self):
        frames = (self.attack_speed)*FRAMES
        rendering_frame = self.attack_counter//(self.attack_speed)
        x = self.position[0] - 1.5*self.size + PADDING_X
        y = self.position[1] + 2*self.size - self.image_tower_height + PADDING_Y
        if self.health <= 0:
            self.middle_surf.blit(self.image_destroyed, (x, y))
            return
        self.middle_surf.blit(self.image_tower, (x, y))
        self.shadow_surf.blit(self.image_tower_shadow, (x, y-self.size*0.2))
        if self.troop2:
            self.middle_surf.blit(self.image_cannon,(x,y - self.size*(0.2 + 0.05 * (rendering_frame % 6))))
            self.render_health_bar((x+self.size/2,y))
        else:
            self.middle_surf.blit(self.image_cannon,(x,y - self.size*(0.8 - 0.05 * (rendering_frame % 6))))
            self.render_health_bar((x+self.size/2,y+2*self.size))
        self.middle_surf.blit(self.images["_attack_"+f'{rendering_frame+1}'],(x, y - self.size*0.4))
        self.attack_counter = (self.attack_counter+1)%frames
