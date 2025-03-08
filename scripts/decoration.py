import pygame
from scripts.config import *

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
                text_rect = text_surface.get_rect(center=(ARENA_WIDTH // 2 , ARENA_HEIGHT // 2+ (i-1)*30))
                self.screen.blit(text_surface, text_rect)

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

    def render_time(self):
        if self.start_time:
            font = pygame.font.Font("data/font/clashroyale.ttf", 40)
            elapsed_seconds = (pygame.time.get_ticks() - self.start_time) // 1000
            remaining_seconds = max(180 - elapsed_seconds, 0)  # Countdown from 180s
            minutes = remaining_seconds // 60
            seconds = remaining_seconds % 60
            timer_text = font.render(f"{minutes:02}:{seconds:02}", True, (244,196,76))
            self.left_screen.blit(timer_text,(FULL_WIDTH*0.17,FULL_HEIGHT*0.923))            
        
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


