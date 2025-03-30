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

from random import randint, choice
import math

class Firework:
    def __init__(self, x, y, color, num_particles=30):
        self.particles = []
        for _ in range(num_particles):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(3, 7)  # Faster explosion effect
            dx = speed * math.cos(angle)
            dy = speed * math.sin(angle)
            size = random.randint(2, 5)  # Random sizes
            self.particles.append([x, y, dx, dy, 255, size])  # (x, y, dx, dy, alpha, size)
        self.color = color

    def update(self):
        """Update positions, apply gravity, and fade out."""
        for particle in self.particles:
            particle[0] += particle[2]  # Move X
            particle[1] += particle[3]  # Move Y
            particle[3] += 0.1  # Simulate gravity
            particle[4] -= random.randint(3, 7)  # Faster fade
            particle[5] = max(1, particle[5] - 0.1)  # Shrink over time
        self.particles = [p for p in self.particles if p[4] > 0]  # Remove faded particles

    def draw(self, screen):
        """Draw glowing particles."""
        for particle in self.particles:
            color = (
                min(255, self.color[0] + random.randint(-20, 20)),
                min(255, self.color[1] + random.randint(-20, 20)),
                min(255, self.color[2] + random.randint(-20, 20)),
                particle[4]
            )
            pygame.draw.circle(screen, color, (int(particle[0]), int(particle[1])), int(particle[5]))



class Game:
    def __init__(self, troops1, troops2, team_name1, team_name2):
        pygame.init()
        pygame.font.init()
        pygame.display.set_caption('Code Royale')

        self.arena_display_size = (ARENA_WIDTH, ARENA_HEIGHT)
        self.side_display_size = ((FULL_WIDTH - MIDDLE_WIDTH) // 2, FULL_HEIGHT)
        self.tile_size = ARENA_WIDTH / 12
        self.middle_screen = pygame.Surface((MIDDLE_WIDTH, MIDDLE_HEIGHT))
        self.screen = pygame.Surface((MIDDLE_WIDTH, MIDDLE_HEIGHT), pygame.SRCALPHA)
        self.shadow_screen = pygame.Surface((MIDDLE_WIDTH, MIDDLE_HEIGHT), pygame.SRCALPHA)
        self.left_screen = pygame.Surface(self.side_display_size)
        self.right_screen = pygame.Surface(self.side_display_size)
        self.main_screen = pygame.display.set_mode((FULL_WIDTH, EXTRA_HEIGHT), pygame.RESIZABLE)

        self.fps = FPS
        self.clock = pygame.time.Clock()
        self.game_counter = 0
        self.winner = None
        self.message = None
        self.tower_size = 2.25 * self.tile_size
        towers_position = (ARENA_WIDTH / 2, ARENA_HEIGHT)
        self.assets = load_assets()
        deploy_area = (0, self.arena_display_size[0], self.arena_display_size[1] / 2, self.arena_display_size[1])

        self.middle_map = Middle_Map(self.assets["middle_map"])

        self.team_name1 = team_name1
        self.team_name2 = team_name2
        deployable_troops1 = troops1.copy()
        random.shuffle(deployable_troops1)
        deployable_troops2 = troops2.copy()
        random.shuffle(deployable_troops2)
        self.team1_script_test = True
        self.team2_script_test = True
        self.tower1 = Tower("Tower 1", towers_position, self.assets, self.tower_size, deploy_area,
                            self.screen, self.shadow_screen, self.middle_screen, troops1)
        self.tower2 = Tower("Tower 2", convert_player2(towers_position, self.arena_display_size),
                            self.assets, self.tower_size, convert_player2_area(deploy_area, self.arena_display_size),
                            self.screen, self.shadow_screen, self.middle_screen, troops2, troop2=True)
        
        self.tower1.oppTower = self.tower2
        self.tower1.oppTroops = self.tower2.myTroops
        self.tower2.oppTower = self.tower1
        self.tower2.oppTroops = self.tower1.myTroops
        self.data_provided1 = {}
        self.data_provided2 = {}
        
        pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
        self.final_music = "./audio/final_1x.mp3"
        self.win_music = "./winner.mp3"
        self.current_music = None
        
        self.fireworks = []
        self.fireworks_active = False
        
        self.speed_to_music = {
            1.0: "./audio/final_1x.mp3",
            1.5: "./audio/final_1x.mp3",
            2.0: "./audio/final_1x.mp3",
            2.5: "./audio/final_1x.mp3",
            3.0:"./audio/final_1x.mp3",
            3.5: "./audio/final_1x.mp3",
            4.0: "./audio/final_1x.mp3",
            4.5: "./audio/final_1x.mp3",
            5.0: "./audio/final_1x.mp3",
            5.5: "./audio/final_1x.mp3",
            6.0: "./audio/final_1x.mp3",
            6.5: "./audio/final_1x.mp3",
            7.0: "./audio/final_1x.mp3",
        }
        self.speed_multiplier = 1.0  # Default speed
        self.song_length = 180  # 3 minutes in seconds
        self.current_music_position = 0  # Track music position

    def start_fireworks(self):
        """Triggers full-screen fireworks animation after the game ends."""
        if self.fireworks_active and self.game_counter % 7 == 0:  # More frequent fireworks
            for _ in range(5):  # Create 5 fireworks at a time
                x, y = random.randint(100, FULL_WIDTH - 100), random.randint(50, FULL_HEIGHT - 200)
                color = (random.randint(150, 255), random.randint(50, 255), random.randint(50, 255))  # Bright colors
                self.fireworks.append(Firework(x, y, color, num_particles=random.randint(25, 40)))

        for fw in self.fireworks:
            fw.update()

        self.fireworks = [fw for fw in self.fireworks if len(fw.particles) > 0]  # Remove faded fireworks


    def play_music(self, music_file, resume_from=0):
        """Plays a new music track, resuming from the appropriate position."""
        if self.current_music != music_file or not pygame.mixer.music.get_busy():
            pygame.mixer.music.load(music_file)
            pygame.mixer.music.play(-1, resume_from)  # Resume at calculated time
            self.current_music = music_file
            print(f"Playing {music_file} from {resume_from:.2f} seconds")

    def update_music(self):
        """Updates the background music based on the game phase."""
        if GAME_START_TIME <= self.game_counter < GAME_END_TIME:
            desired_music = self.speed_to_music[self.speed_multiplier]
        elif self.tower1.health == 0 or self.tower2.health == 0 or self.game_counter >= GAME_END_TIME:
            desired_music = self.win_music
            if self.current_music != self.win_music:
                self.speed_multiplier=3
                self.fps=30
                self.play_music(self.win_music, 0)
            self.fireworks_active = True
        else:
            return  # No music update needed

        # Only change music if it's different from the currently playing track
        if self.current_music != desired_music:
            elapsed_time = (self.game_counter / FPS) * (1 / self.speed_multiplier)
            new_elapsed_time = min(elapsed_time, self.song_length - 1)

            self.play_music(desired_music, new_elapsed_time)

    def render_game_screen(self):
        self.middle_map.render(self.middle_screen)
        self.screen.fill((0, 0, 0, 0))
        self.shadow_screen.fill((0, 0, 0, 0))

        self.update_music()

        if GAME_END_TIME > self.game_counter >= GAME_START_TIME:
            DataFlow.provide_data(self)
            DataFlow.deployment(self)
            DataFlow.attack_die(self)
            Decoration.check_game_end(self)
        elif self.game_counter < GAME_START_TIME - 2:  
            Decoration.entry_text(self)
        elif self.game_counter >= GAME_END_TIME:
            Decoration.outro_text(self)

        self.main_screen.blit(self.middle_screen, ((FULL_WIDTH - MIDDLE_WIDTH) // 2, 0))
        self.main_screen.blit(self.shadow_screen, ((FULL_WIDTH - MIDDLE_WIDTH) // 2, 0))
        self.main_screen.blit(self.screen, ((FULL_WIDTH - MIDDLE_WIDTH) // 2, 0))

        if self.fireworks_active:
            # Create a deep dark overlay
            dark_overlay = pygame.Surface((FULL_WIDTH, FULL_HEIGHT), pygame.SRCALPHA)
            dark_overlay.fill((0, 0, 0, 50))  # Darker effect
            self.main_screen.blit(dark_overlay, (0, 0))  

            # Fireworks animation
            self.start_fireworks()
            for firework in self.fireworks:
                firework.draw(self.main_screen)

    def render_left_screen(self):
        Decoration_Left.render_background(self)
        if GAME_END_TIME > self.game_counter >= GAME_START_TIME:
            Decoration_Left.render_screen(self)
        self.main_screen.blit(self.left_screen, (0, 0))

    def render_right_screen(self):
        Decoration_Right.render_background(self)
        if GAME_END_TIME > self.game_counter >= GAME_START_TIME:
            Decoration_Right.render_screen(self)       
        self.main_screen.blit(self.right_screen, ((FULL_WIDTH + MIDDLE_WIDTH) // 2, 0))

    def run(self):
        while True:
            self.render_game_screen()  # Always render the middle screen

            # If game is not over, render the side screens
            if True:
                self.render_left_screen()
                self.render_right_screen()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.mixer.music.stop()
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and self.current_music != self.win_music:    
                    if self.speed_multiplier > 4.0:
                        # If speed is already greater than 4, don't allow changing speed at all
                        continue  

                    prev_speed = self.speed_multiplier  # Store previous speed
                    prev_fps = self.fps  # Store previous FPS
                    prev_game_counter = self.game_counter  # Store game counter before change

                    if event.key == pygame.K_UP:
                        self.speed_multiplier = min(4.0, self.speed_multiplier + 0.5)
                        self.fps = min(70, self.fps + 5)

                    elif event.key == pygame.K_DOWN:
                        self.speed_multiplier = max(1.0, self.speed_multiplier - 0.5)
                        self.fps = max(5, self.fps - 5)

                    # Ensure only defined speeds (1.0 to 4.0) are used
                    if self.speed_multiplier not in self.speed_to_music:
                        self.speed_multiplier = 4.0  # Default to 4.0 for undefined speeds

                    # If speed did not change, do nothing
                    if self.speed_multiplier == prev_speed:
                        continue

                    # Correctly adjust the elapsed time using the new speed
                    elapsed_time = (prev_game_counter / prev_fps) * (prev_speed / self.speed_multiplier)
                    new_elapsed_time = min(elapsed_time, self.song_length - 1)

                    new_music_file = self.speed_to_music[self.speed_multiplier]
                    self.play_music(new_music_file, new_elapsed_time)
                
            pygame.display.update()
            self.clock.tick(self.fps)
            self.game_counter += 1