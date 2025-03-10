import pygame
from scripts.config import *
from game import Game

class Decoration:
    def entry_text(self):
        font = pygame.font.Font("data/font/clashroyale.ttf", 26)  # Default font, size 26

        texts = [self.team_name2,"v/s",self.team_name1]
        for i, text in enumerate(texts):
            text_surface = font.render(text, True, (255,255,255))
            text_rect = text_surface.get_rect(center=(ARENA_WIDTH // 2 , ARENA_HEIGHT // 2+ (i-1)*30))
            self.screen.blit(text_surface, text_rect)

    def outro_text(self):
        self.tower1.render()
        self.tower2.render()
        font = pygame.font.Font("data/font/clashroyale.ttf", 36)  # Default font, size 36
        if not self.winner:
            if self.tower1.health > self.tower2.health:
                self.winner = self.team_name1
            elif self.tower1.health < self.tower2.health:
                self.winner = self.team_name2
            else:
                self.winner = "Tie"
        if self.winner == "Tie":
            text_surface = font.render(self.winner, True, (255,255,255))
            text_rect = text_surface.get_rect(center=(ARENA_WIDTH // 2 , ARENA_HEIGHT // 2))
            self.screen.blit(text_surface, text_rect)
        else:
            texts = ["Winner", self.winner]
            for i, text in enumerate(texts):
                text_surface = font.render(text, True, (255,255,255))
                text_rect = text_surface.get_rect(center=(ARENA_WIDTH // 2 , ARENA_HEIGHT // 2+ (i-1)*40))
                self.screen.blit(text_surface, text_rect)

    def check_game_end(self:Game):
        if self.tower1.health <= 0 and self.tower2.health <= 0:
            self.game_counter = GAME_END_TIME
            self.winner = "Tie"
        if self.tower1.health <= 0:
            self.game_counter = GAME_END_TIME
            self.winner = self.team_name2
        if self.tower2.health <= 0:
            self.game_counter = GAME_END_TIME
            self.winner = self.team_name1
        if self.team1_script_test and not self.team2_script_test:
            self.winner = self.team_name1
            print(f"RULES BROKEN BY {self.team_name2}")
        if not self.team1_script_test and self.team2_script_test:
            self.winner = self.team_name2
            print(f"RULES BROKEN BY {self.team_name1}")
        if not self.team1_script_test and not self.team2_script_test:
            self.winner = "Tie"
            print(f"RULES BROKEN BY BOTH {self.team_name1} and {self.team_name2}")

class Decoration_Left:
    def render_background(self):
        image = self.assets['left_side_image']
        image = pygame.transform.scale(image,self.side_display_size)
        self.left_screen.blit(image,(0,0))
        
    troops_displayed = []
    
    def update_troops(self):
        if len(Decoration_Left.troops_displayed) <=8:
            troops = self.tower1.myTroops
            for troop in troops:
                if troop.name not in Decoration_Left.troops_displayed:
                    Decoration_Left.troops_displayed.append(troop.name)
                
    def render_troop_cards(self):
        Decoration_Left.update_troops(self)
        troops = Decoration_Left.troops_displayed
        for i in range(len(troops)):
            image = self.assets[f'{troops[i]}_card']
            image = pygame.transform.scale(image,(CARD_PLATE_WIDTH*2.2/3,CARD_PLATE_HEIGHT*99/832))
            self.left_screen.blit(image,(CARD_PLATE_WIDTH*1//6,int(FULL_WIDTH*11/108 + (CARD_PLATE_HEIGHT*93/832)*i)))
        Decoration_Left.render_elixir_bar(self)

    def render_time(self):
        font = pygame.font.Font("data/font/clashroyale.ttf", 40)
        remaining_seconds = (GAME_END_TIME - self.game_counter)//10
        minutes = remaining_seconds // 60
        seconds = remaining_seconds % 60
        timer_text = font.render(f"{minutes:02}:{seconds:02}", True, (244,196,76))
        self.left_screen.blit(timer_text,(FULL_WIDTH*0.17,FULL_HEIGHT*0.933)) 

        text = font.render(f'x{max(3-minutes,1)}',True,(220,68,220))
        self.left_screen.blit(text,(FULL_WIDTH*0.33,FULL_HEIGHT*0.93))
        
        img = self.assets[f'elixir']
        img = pygame.transform.scale(img,(FULL_WIDTH*0.026,FULL_HEIGHT*0.056))
        self.left_screen.blit(img,(FULL_WIDTH*0.3,FULL_HEIGHT*0.93))
            
    def render_elixir_bar(self):
        img = self.assets[f'bar_{int(self.tower1.total_elixir)}']
        img = pygame.transform.scale(img,(FULL_WIDTH*0.26,FULL_HEIGHT*0.086))
        self.left_screen.blit(img,(FULL_WIDTH*0.10,FULL_HEIGHT*0.2))

    def render_name(self):
        font = pygame.font.Font("data/font/clashroyale.ttf", 40)
        text = font.render(f'{self.team_name1}',True,((73,152,196)))
        self.left_screen.blit(text,(FULL_WIDTH*0.10,FULL_HEIGHT*0.15)) 
        
class Decoration_Right:
    def render_background(self):
        image = self.assets['right_side_image']
        image = pygame.transform.scale(image,self.side_display_size)
        self.right_screen.blit(image,(0,0))
        
    troops_displayed = []
    
    def update_troops(self):
        if len(Decoration_Right.troops_displayed) <=8:
            troops = self.tower2.myTroops
            for troop in troops:
                if troop.name not in Decoration_Right.troops_displayed:
                    Decoration_Right.troops_displayed.append(troop.name)
                 
    def render_troop_cards(self):
        Decoration_Right.update_troops(self)
        troops = Decoration_Right.troops_displayed
        for i in range(len(troops)):
            image = self.assets[f'{troops[i]}_card']
            image = pygame.transform.scale(image,(CARD_PLATE_WIDTH*2.2/3,CARD_PLATE_HEIGHT*99/832))
            self.right_screen.blit(image,(int(FULL_WIDTH*69/196 - CARD_PLATE_WIDTH*4.5/6),int(FULL_WIDTH*11/108 + (CARD_PLATE_HEIGHT*93/832)*i))) 
        Decoration_Right.render_elixir_bar(self) 
            
    def render_elixir_bar(self):
        img = self.assets[f'bar_{int(self.tower2.total_elixir)}']
        img = pygame.transform.scale(img,(FULL_WIDTH*0.26,FULL_HEIGHT*0.086))
        self.right_screen.blit(img,(FULL_WIDTH*0.05,FULL_HEIGHT*0.2))

    def render_name(self):
        font = pygame.font.Font("data/font/clashroyale.ttf", 40)
        text = font.render(f'{self.team_name2}',True,((200, 57, 90)))
        self.right_screen.blit(text,(FULL_WIDTH*0.05,FULL_HEIGHT*0.15)) 

    def render_game_speed(self):
        game_speed = self.fps/FPS
        font = pygame.font.Font("data/font/clashroyale.ttf", 40)
        text = font.render(f'Game Speed: x{game_speed}',True,((255, 255, 255)))
        self.right_screen.blit(text,(FULL_WIDTH*0.06,FULL_HEIGHT*0.93)) 




