import pygame

# Initialize pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
FPS = 30

# Load sprite sequences
# Replace with your actual image paths
sprite_sequences = {
    "run_right": [pygame.image.load(f"run_right_{i}.png") for i in range(1, 6)],
    # "run_left": [pygame.image.load(f"run_left_{i}.png") for i in range(1, 6)],
    "attack_right": [pygame.image.load("attack_right_{i}.png") for i in range(1, 6)],
    # "attack_left": [pygame.image.load(f"attack_left_{i}.png") for i in range(1, 6)],
}

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vel = 5
        self.current_action = "attack_right"
        self.frame_index = 0
        self.image = sprite_sequences[self.current_action][self.frame_index]
        self.flip = False
        self.last_update = pygame.time.get_ticks()
        self.animation_speed = 100  # milliseconds per frame

    def update(self, keys):
        # if keys[pygame.K_LEFT]:
        #     self.x -= self.vel
        #     self.current_action = "run_left"
        if keys[pygame.K_RIGHT]:
            # self.x += self.vel
            self.current_action = "attack_right"
        # elif keys[pygame.K_a]:
        #     self.current_action = "attack_left"
        elif keys[pygame.K_d]:
            self.current_action = "attack_right"
        
        # Handle animation timing
        now = pygame.time.get_ticks()
        if now - self.last_update > self.animation_speed:
            self.last_update = now
            self.frame_index = (self.frame_index + 1) % len(sprite_sequences[self.current_action])
            self.image = sprite_sequences[self.current_action][self.frame_index]

    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))

# Player instance
player = Player(WIDTH // 2, HEIGHT // 2)

running = True
while running:
    screen.fill((0, 0, 0))
    
    keys = pygame.key.get_pressed()
    player.update(keys)
    player.draw(screen)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
