import pygame
import sys
from scripts.utils import *
from scripts.statics import *
from scripts.assets import load_assets
from scripts.Troops.tower import Tower
from scripts.decoration import Decoration, Decoration_Left, Decoration_Right, Firework
from scripts.dataflow import DataFlow
import random
from scripts.game_config import *
import cv2
import numpy as np
from ffpyplayer.player import MediaPlayer

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
                            self.screen, self.shadow_screen, self.middle_screen, deployable_troops1)
        self.tower2 = Tower("Tower 2", convert_player2(towers_position, self.arena_display_size),
                            self.assets, self.tower_size, convert_player2_area(deploy_area, self.arena_display_size),
                            self.screen, self.shadow_screen, self.middle_screen, deployable_troops2, troop2=True)
        
        self.tower1.oppTower = self.tower2
        self.tower1.oppTroops = self.tower2.myTroops
        self.tower2.oppTower = self.tower1
        self.tower2.oppTroops = self.tower1.myTroops
        self.data_provided1 = {}
        self.data_provided2 = {}
        
        pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
        self.final_music = "./data/audio/final_1x.mp3"
        self.win_music = "./data/audio/winner.mp3"
        self.current_music = None
        
        self.fireworks = []
        self.fireworks_active = False
        
        self.speed_to_music = {
            1.0: "./data/audio/final_1x.mp3",
            1.5: "./data/audio/final_1x.mp3",
            2.0: "./data/audio/final_1x.mp3",
            2.5: "./data/audio/final_1x.mp3",
            3.0:"./data/audio/final_1x.mp3",
            3.5: "./data/audio/final_1x.mp3",
            4.0: "./data/audio/final_1x.mp3",
            4.5: "./data/audio/final_1x.mp3",
            5.0: "./data/audio/final_1x.mp3",
            5.5: "./data/audio/final_1x.mp3",
            6.0: "./data/audio/final_1x.mp3",
            6.5: "./data/audio/final_1x.mp3",
            7.0: "./data/audio/final_1x.mp3",
        }
        self.speed_multiplier = 1.0  # Default speed
        self.song_length = 180  # 3 minutes in seconds
        self.current_music_position = 0  # Track music position

    def start_fireworks(self):
        """Triggers full-screen fireworks animation after the game ends."""
        if self.fireworks_active and self.game_counter % 7 == 0:  # More frequent fireworks
            for _ in range(5):  # Create 5 fireworks at a time
                x = random.randint(50, FULL_WIDTH - 50)  # Cover full screen width
                y = random.randint(50, FULL_HEIGHT - 200)
                color = (random.randint(150, 255), random.randint(50, 255), random.randint(50, 255))  # Bright colors
                self.fireworks.append(Firework(x, y, color, num_particles=random.randint(25, 40)))

        for fw in self.fireworks:
            fw.update()

        # Remove faded fireworks
        self.fireworks = [fw for fw in self.fireworks if len(fw.particles) > 0]

    def play_intro_video(self, video_path):
        cap = cv2.VideoCapture(video_path)
        player = MediaPlayer(video_path)  # Load audio

        if not cap.isOpened():
            print("Error: Could not open video.")
            return

        fps = int(cap.get(cv2.CAP_PROP_FPS))
        clock = pygame.time.Clock()

        while cap.isOpened():
            ret, frame = cap.read()
            audio_frame, val = player.get_frame()  # Get audio frame

            if not ret:
                break  # End of video

            # Fix the flipped video issue
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert BGR to RGB
            frame = np.flipud(frame)  # Flip vertically if needed (try removing if unnecessary)
            frame = np.rot90(frame, -1)  # Rotate counterclockwise to correct orientation
            
            frame_surface = pygame.surfarray.make_surface(frame)

            # Scale video to fit Pygame main screen
            scaled_frame = pygame.transform.scale(frame_surface, self.main_screen.get_size())

            # Display video in Pygame
            self.main_screen.blit(scaled_frame, (0, 0))
            pygame.display.update()

            # Handle quitting or skipping
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key in [pygame.K_RETURN, pygame.K_SPACE]:
                    cap.release()
                    return  # Skip video

            clock.tick(fps)

        cap.release() 

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

        # Draw to respective screens
        self.main_screen.blit(self.middle_screen, ((FULL_WIDTH - MIDDLE_WIDTH) // 2, 0))
        self.main_screen.blit(self.shadow_screen, ((FULL_WIDTH - MIDDLE_WIDTH) // 2, 0))
        self.main_screen.blit(self.screen, ((FULL_WIDTH - MIDDLE_WIDTH) // 2, 0))

        # Fireworks on all screens
        if self.fireworks_active:
            self.start_fireworks()
            for firework in self.fireworks:
                firework.draw(self.main_screen)  # Middle screen
                firework.draw(self.left_screen)  # Left screen
                firework.draw(self.right_screen)  # Right screen


    def render_left_screen(self):
        Decoration_Left.render_background(self)
        if GAME_END_TIME > self.game_counter >= GAME_START_TIME:
            Decoration_Left.render_screen(self)

        # Draw fireworks on the left screen
        if self.fireworks_active:
            for firework in self.fireworks:
                firework.draw(self.left_screen)

        self.main_screen.blit(self.left_screen, (0, 0))


    def render_right_screen(self):
        Decoration_Right.render_background(self)
        if GAME_END_TIME > self.game_counter >= GAME_START_TIME:
            Decoration_Right.render_screen(self)

        # Draw fireworks on the right screen
        if self.fireworks_active:
            for firework in self.fireworks:
                firework.draw(self.right_screen)

        self.main_screen.blit(self.right_screen, ((FULL_WIDTH + MIDDLE_WIDTH) // 2, 0))
    
    def run(self):
        self.play_intro_video("./data/video/wncc.mp4")
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