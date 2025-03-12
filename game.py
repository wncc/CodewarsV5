import pygame
import sys
from scripts.utils import *
from scripts.statics import *
from scripts.assets import load_assets
from scripts.Troops.tower import Tower
from scripts.decoration import Decoration, Decoration_Left, Decoration_Right
from scripts.dataflow import DataFlow
import random
from scripts.game_config import *

class Game:
    def __init__(self, troops1, troops2, team_name1, team_name2):
        pygame.init()
        pygame.font.init()
        pygame.display.set_caption('Code Royale')

        self.arena_display_size = (ARENA_WIDTH,ARENA_HEIGHT)
        self.side_display_size = ((FULL_WIDTH-MIDDLE_WIDTH)//2, FULL_HEIGHT)
        self.tile_size = ARENA_WIDTH//12
        self.middle_screen = pygame.Surface((MIDDLE_WIDTH,MIDDLE_HEIGHT))
        self.screen = pygame.Surface((MIDDLE_WIDTH,MIDDLE_HEIGHT),pygame.SRCALPHA)
        self.shadow_screen = pygame.Surface((MIDDLE_WIDTH,MIDDLE_HEIGHT),pygame.SRCALPHA)
        self.left_screen = pygame.Surface(self.side_display_size)
        self.right_screen = pygame.Surface(self.side_display_size)
        self.main_screen = pygame.display.set_mode((FULL_WIDTH,EXTRA_HEIGHT),pygame.RESIZABLE)

        self.fps = FPS
        self.clock = pygame.time.Clock()
        self.game_counter = 0
        self.winner = None
        self.message = None
        self.tower_size = 2.25*self.tile_size
        towers_position = (ARENA_WIDTH/2,ARENA_HEIGHT)
        self.assets = load_assets()
        deploy_area = (0,self.arena_display_size[0],self.arena_display_size[1]/2,self.arena_display_size[1])

        self.middle_map = Middle_Map(self.assets["middle_map"])
        """
        NOTE
        TOWER 1's PERSPECTIVE IS GAME's PERSPECTIVE
        """
        self.team_name1 = team_name1
        self.team_name2 = team_name2
        deployable_troops1 = troops1
        random.shuffle(deployable_troops1)
        deployable_troops2 = troops2
        random.shuffle(deployable_troops2)
        self.team1_script_test = True
        self.team2_script_test = True
        self.tower1 = Tower("Tower 1", towers_position, self.assets,self.tower_size, deploy_area, self.screen, self.shadow_screen, self.middle_screen, deployable_troops1)
        self.tower2 = Tower("Tower 2", convert_player2(towers_position,self.arena_display_size), self.assets ,self.tower_size, convert_player2_area(deploy_area,self.arena_display_size), self.screen, self.shadow_screen, self.middle_screen, deployable_troops2, troop2=True) # troop2 means you are player 2
        self.tower1.oppTower = self.tower2
        self.tower1.oppTroops = self.tower2.myTroops
        self.tower2.oppTower = self.tower1
        self.tower2.oppTroops = self.tower1.myTroops
        self.data_provided1 = {}
        self.data_provided2 = {}
    
    def render_game_screen(self):
        self.middle_map.render(self.middle_screen)
        
        self.screen.fill((0, 0, 0, 0)) # clear screen
        self.shadow_screen.fill((0, 0, 0, 0)) # clear screen
        
        if GAME_END_TIME > self.game_counter >= GAME_START_TIME:
            DataFlow.provide_data(self)
            DataFlow.deployment(self)
            DataFlow.attack_die(self)
            Decoration.check_game_end(self)
        elif self.game_counter < GAME_START_TIME - 2: # 2 -> BUFFER
            Decoration.entry_text(self)
        elif self.game_counter >= GAME_END_TIME:
            Decoration.outro_text(self)

        self.main_screen.blit(self.middle_screen, ((FULL_WIDTH-MIDDLE_WIDTH)//2, 0))
        self.main_screen.blit(self.shadow_screen, ((FULL_WIDTH-MIDDLE_WIDTH)//2, 0))
        self.main_screen.blit(self.screen, ((FULL_WIDTH-MIDDLE_WIDTH)//2, 0))
    
    def render_left_screen(self):
        Decoration_Left.render_background(self)
        if GAME_END_TIME > self.game_counter >= GAME_START_TIME:
            Decoration_Left.render_screen(self)
        self.main_screen.blit(self.left_screen, (0, 0))
    def render_right_screen(self):
        Decoration_Right.render_background(self)
        if GAME_END_TIME > self.game_counter >= GAME_START_TIME:
            Decoration_Right.render_screen(self)       
        self.main_screen.blit(self.right_screen, ((FULL_WIDTH+MIDDLE_WIDTH)//2, 0))

    def run(self):
        while True:
            self.render_game_screen()
            self.render_left_screen()
            self.render_right_screen()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.fps = min(70,self.fps+5)
                    if event.key == pygame.K_DOWN:
                        self.fps = max(5,self.fps - 5)
            pygame.display.update()
            self.clock.tick(self.fps)
            self.game_counter += 1