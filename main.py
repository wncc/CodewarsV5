import pygame
import sys
from scripts.utils import *
from scripts.statics import *
from scripts.assets import load_assets
from scripts.Troops.tower import Tower
from scripts.decoration import Decoration
from scripts.dataflow import DataFlow
from teams.team1 import deploy as deploy1, troops as troops1, team_name as team_name1
from teams.team2 import deploy as deploy2, troops as troops2, team_name as team_name2
import random
from scripts.config import *

class Game:
    def __init__(self):
        pygame.init()
        pygame.font.init()
        pygame.display.set_caption('Code Royale')
        self.arena_display_size = (ARENA_WIDTH,ARENA_HEIGHT)
        self.side_display_size = ((FULL_WIDTH-ARENA_WIDTH)//2, FULL_HEIGHT)
        self.tile_size = ARENA_WIDTH//12
        self.main_screen = pygame.display.set_mode((FULL_WIDTH,EXTRA_HEIGHT),pygame.RESIZABLE)
        self.screen = pygame.Surface(self.arena_display_size)
        self.left_screen = pygame.Surface(self.side_display_size)
        self.right_screen = pygame.Surface(self.side_display_size)
        self.clock = pygame.time.Clock()
        self.fps = FPS
        self.game_counter = 0
        self.winner = None
        self.tower_size = 2*self.tile_size
        towers_position = (self.arena_display_size[0]/2,self.arena_display_size[1]-self.tower_size)
        self.assets = load_assets()
        deploy_area = (0,self.arena_display_size[0],self.arena_display_size[1]/2,self.arena_display_size[1])

        self.tilemap = GrassTile(self.assets['tiles'], tile_size=self.tile_size, display_size = self.arena_display_size)
        self.rockmap = RockTile(self.assets['rock'], tile_size=self.tile_size, display_size = self.arena_display_size)

        """
        NOTE
        TOWER 1's PERSPECTIVE IS GAME's PERSPECTIVE
        """
        self.team_name1 = team_name1
        self.team_name2 = team_name2
        deployable_troops1 = troops1
        # random.shuffle(deployable_troops1)
        deployable_troops2 = troops2
        # random.shuffle(deployable_troops2)
        self.tower1 = Tower("Tower 1", towers_position, self.assets,self.tower_size, deploy_area, self.screen, deployable_troops1)
        self.tower2 = Tower("Tower 2", convert_player2(towers_position,self.arena_display_size), self.assets ,self.tower_size, convert_player2_area(deploy_area,self.arena_display_size), self.screen, deployable_troops2, troop2=True) # troop2 means you are player 2
        self.tower1.oppTower = self.tower2
        self.tower1.oppTroops = self.tower2.myTroops
        self.tower2.oppTower = self.tower1
        self.tower2.oppTroops = self.tower1.myTroops
        self.data_provided1 = {}
        self.data_provided2 = {}
    
    def render_game_screen(self):
        self.tilemap.render(self.screen)
        self.rockmap.render(self.screen)
        if GAME_END_TIME > self.game_counter >= GAME_START_TIME:
            DataFlow.provide_data(self)
            DataFlow.deployment(self)
            DataFlow.attack_die(self)
            Decoration.check_game_end(self)
        elif self.game_counter < GAME_START_TIME - 2: # 2 -> BUFFER
            Decoration.entry_text(self)
        elif self.game_counter >= GAME_END_TIME:
            Decoration.outro_text(self)
        self.main_screen.blit(self.screen, ((FULL_WIDTH-ARENA_WIDTH)//2, (FULL_HEIGHT-ARENA_HEIGHT)//2))
    
    def render_left_screen(self):
        # Decoration.function() -- idhar likhna hai
        self.main_screen.blit(self.left_screen, (0, 0))

    def render_right_screen(self):
        # Decoration.function() -- idhar likhna hai
        self.main_screen.blit(self.right_screen, ((FULL_WIDTH+ARENA_WIDTH)//2, 0))

    def run(self):
        while True:
            self.render_game_screen()
            self.render_left_screen()
            self.render_right_screen()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            pygame.display.update()
            self.clock.tick(self.fps)
            self.game_counter += 1

Game().run()