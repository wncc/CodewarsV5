import pygame
from scripts.config import *

class Decoration:
    def entry_text(self):
        font = pygame.font.Font("/Users/tusharsingharoy/coderoyale/data/font/clashroyale.ttf", 26)  # Default font, size 36

        texts = [self.team_name2,"v/s",self.team_name1]
        for i, text in enumerate(texts):
            text_surface = font.render(text, True, (255,255,255))
            text_rect = text_surface.get_rect(center=(WIDTH // 2 , HEIGHT // 2+ (i-1)*30))
            self.screen.blit(text_surface, text_rect)

    def outro_text(self):
        self.tower1.render()
        self.tower2.render()
        font = pygame.font.Font(None, 36)  # Default font, size 36
        if not self.winner:
            if self.tower1.health > self.tower2.health:
                self.winner = self.team_name1
            elif self.tower1.health < self.tower2.health:
                self.winner = self.team_name2
            else:
                self.winner = "Tie"
        if self.winner == "Tie":
            text_surface = font.render(self.winner, True, (255,255,255))
            text_rect = text_surface.get_rect(center=(WIDTH // 2 , HEIGHT // 2))
            self.screen.blit(text_surface, text_rect)
        else:
            texts = ["Winner", self.winner]
            for i, text in enumerate(texts):
                text_surface = font.render(text, True, (255,255,255))
                text_rect = text_surface.get_rect(center=(WIDTH // 2 , HEIGHT // 2+ (i-1)*30))
                self.screen.blit(text_surface, text_rect)

    def check_game_end(self):
        if self.tower1.health <= 0 and self.tower2.health <= 0:
            self.game_counter = 1830
            self.winner = "Tie"
        if self.tower1.health <= 0:
            self.game_counter = 1830
            self.winner = self.team_name2
        if self.tower2.health <= 0:
            self.game_counter = 1830
            self.winner = self.team_name1