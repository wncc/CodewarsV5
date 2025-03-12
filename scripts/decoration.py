import pygame
from scripts.game_config import *

class Decoration:
    def entry_text(self):
        font = pygame.font.Font("data/font/clashroyale.ttf", FULL_HEIGHT//37)  # Default font, size 26

        texts = [self.team_name2,"v/s",self.team_name1]
        for i, text in enumerate(texts):
            text_surface = font.render(text, True, (255,255,255))
            text_rect = text_surface.get_rect(center=(MIDDLE_WIDTH // 2 , MIDDLE_HEIGHT // 2+ (i-1)*FULL_HEIGHT//37))
            self.middle_screen.blit(text_surface, text_rect)

    def outro_text(self):
        self.tower1.render()
        self.tower2.render()
        font = pygame.font.Font("data/font/clashroyale.ttf", FULL_HEIGHT//27)
        font2 = pygame.font.Font("data/font/clashroyale.ttf", FULL_HEIGHT//80)  # Default font, size 36
        if not self.winner:
            if self.tower1.health > self.tower2.health:
                self.winner = self.team_name1
                self.message = "DECIDED BY TIE BREAKER 1"
            elif self.tower1.health < self.tower2.health:
                self.winner = self.team_name2
                self.message = "DECIDED BY TIE BREAKER 1"
            elif self.tower1.tower_in_range > self.tower2.tower_in_range:
                self.winner = self.team_name1
                self.message = "DECIDED BY TIE BREAKER 2"
            elif self.tower1.tower_in_range < self.tower2.tower_in_range:
                self.winner = self.team_name2
                self.message = "DECIDED BY TIE BREAKER 2"
            else:
                self.winner = "Tie"
        if self.winner == "Tie":
            text_surface = font.render(self.winner, True, (255,255,255))
            text_rect = text_surface.get_rect(center=(MIDDLE_WIDTH // 2 , MIDDLE_HEIGHT // 2))
            self.middle_screen.blit(text_surface, text_rect)
        else:
            texts = ["Winner", self.winner]
            for i, text in enumerate(texts):
                text_surface = font.render(text, True, (255,255,255))
                text_rect = text_surface.get_rect(center=(MIDDLE_WIDTH // 2 , MIDDLE_HEIGHT // 2+ (i-1)*(FULL_HEIGHT//24)))
                self.middle_screen.blit(text_surface, text_rect)
        if self.message:
            text_surface = font2.render(self.message, True, (255,0,0))
            text_rect = text_surface.get_rect(center=(MIDDLE_WIDTH // 2 , MIDDLE_HEIGHT // 2 + (FULL_HEIGHT//24)))
            self.middle_screen.blit(text_surface, text_rect)

    def check_game_end(self):
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
            self.game_counter = GAME_END_TIME
            self.message = f"RULES BROKEN BY {self.team_name2}"
        if not self.team1_script_test and self.team2_script_test:
            self.winner = self.team_name2
            self.game_counter = GAME_END_TIME
            self.message = f"RULES BROKEN BY {self.team_name1}"
        if not self.team1_script_test and not self.team2_script_test:
            self.winner = "Tie"
            self.game_counter = GAME_END_TIME
            self.message = f"RULES BROKEN BY BOTH {self.team_name1} and {self.team_name2}"

class Decoration_Left:
    def render_background(self):
        image = self.assets['left_side_image']
        image = pygame.transform.scale(image,self.side_display_size)
        self.left_screen.blit(image,(0,0))
                
    def render_screen(self):
        Decoration_Left.render_troop_cards(self)
        Decoration_Left.render_time(self)
        Decoration_Left.render_elixir_bar(self)
        Decoration_Left.render_current_cards(self)
        Decoration_Left.render_team_name(self)
        
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
            image = self.assets[f'{troops[i].lower()}_card']
            image = pygame.transform.scale(image,(CARD_PLATE_WIDTH*2.2/3,CARD_PLATE_HEIGHT*99/832))
            self.left_screen.blit(image,(CARD_PLATE_WIDTH*1//6,int(FULL_WIDTH*11/108 + (CARD_PLATE_HEIGHT*93/832)*i)))

    def render_time(self):
        font = pygame.font.Font("data/font/clashroyale.ttf", FULL_HEIGHT//39)
        remaining_seconds = (GAME_END_TIME - self.game_counter)//10
        minutes = remaining_seconds // 60
        seconds = remaining_seconds % 60
        timer_text = font.render(f"{minutes:02}:{seconds:02}", True, (244,196,76))
        self.left_screen.blit(timer_text,(FULL_WIDTH*0.125,FULL_HEIGHT*0.96)) 
        if minutes>0:
            elixer = 1
        else:
            elixer = 2
        text = font.render(f'x{elixer} Elixir',True,(244,196,76))
        self.left_screen.blit(text,(FULL_WIDTH*0.205,FULL_HEIGHT*0.96))
            
    def render_elixir_bar(self):
        img = self.assets[f'bar_{int(self.tower1.total_elixir)}']
        img = pygame.transform.scale(img,(FULL_WIDTH*0.26,FULL_HEIGHT*0.086))
        self.left_screen.blit(img,(FULL_WIDTH*0.10,FULL_HEIGHT*0.225))
        
    def render_current_cards(self):
        img = self.assets['card_slot']
        img = pygame.transform.scale(img,(FULL_WIDTH*0.19,FULL_HEIGHT*0.12))
        self.left_screen.blit(img,(FULL_WIDTH*0.115,FULL_HEIGHT*0.15))
        
        for i in range(len(self.tower1.deployable_troops[:4])):
            img = self.assets[f'{self.tower1.deployable_troops[i].lower()}_card']
            img = pygame.transform.scale(img,(FULL_WIDTH*0.046,FULL_HEIGHT*0.10))
            self.left_screen.blit(img,(FULL_WIDTH*0.118 + i*FULL_WIDTH*0.046,FULL_HEIGHT*0.159))
            
    def render_team_name(self):
        font = pygame.font.Font("data/font/clashroyale.ttf", FULL_HEIGHT//39)
        name = self.team_name1
        text = font.render(f'{name}',True,(255,255,255))
        self.left_screen.blit(text,(FULL_WIDTH*(0.2-0.0055*len(name)),FULL_HEIGHT*0.114))
        
class Decoration_Right:
    def render_background(self):
        image = self.assets['right_side_image']
        image = pygame.transform.scale(image,self.side_display_size)
        self.right_screen.blit(image,(0,0))
        
    def render_screen(self):
        Decoration_Right.render_troop_cards(self)
        Decoration_Right.render_elixir_bar(self)
        Decoration_Right.render_current_cards(self)
        Decoration_Right.render_team_name(self)
        Decoration_Right.render_game_speed(self)
        
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
            image = self.assets[f'{troops[i].lower()}_card']
            image = pygame.transform.scale(image,(CARD_PLATE_WIDTH*2.2/3,CARD_PLATE_HEIGHT*99/832))
            self.right_screen.blit(image,(int(FULL_WIDTH*69/196 - CARD_PLATE_WIDTH*4.5/6),int(FULL_WIDTH*11/108 + (CARD_PLATE_HEIGHT*93/832)*i))) 
            
    def render_elixir_bar(self):
        img = self.assets[f'bar_{int(self.tower2.total_elixir)}']
        img = pygame.transform.scale(img,(FULL_WIDTH*0.26,FULL_HEIGHT*0.086))
        self.right_screen.blit(img,(FULL_WIDTH*0.05,FULL_HEIGHT*0.225))

    def render_game_speed(self):
        game_speed = self.fps/FPS
        font = pygame.font.Font("data/font/clashroyale.ttf", FULL_HEIGHT//39)
        text = font.render(f'x{game_speed}',True,((244,196,76)))
        self.right_screen.blit(text,(FULL_WIDTH*0.31,FULL_HEIGHT*0.96)) 
        
    def render_current_cards(self):
        img = self.assets['card_slot']
        img = pygame.transform.scale(img,(FULL_WIDTH*0.19,FULL_HEIGHT*0.12))
        self.right_screen.blit(img,(FULL_WIDTH*0.065,FULL_HEIGHT*0.15))
        
        for i in range(len(self.tower2.deployable_troops[:4])):
            img = self.assets[f'{self.tower2.deployable_troops[i].lower()}_card']
            img = pygame.transform.scale(img,(FULL_WIDTH*0.046,FULL_HEIGHT*0.10))
            self.right_screen.blit(img,(FULL_WIDTH*0.068 + i*FULL_WIDTH*0.046,FULL_HEIGHT*0.159))
            
    def render_team_name(self):
        font = pygame.font.Font("data/font/clashroyale.ttf", FULL_HEIGHT//39)
        name = self.team_name2
        text = font.render(f'{name}',True,(255,255,255))
        self.right_screen.blit(text,(FULL_WIDTH*(0.16-0.0055*len(name)),FULL_HEIGHT*0.114))