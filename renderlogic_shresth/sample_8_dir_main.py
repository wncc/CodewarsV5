import pygame
from master_render import MasterRender

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
FPS = 30

# Create an instance of MasterRender for an "archer"
player = MasterRender("barbarian", WIDTH // 2, HEIGHT // 2, scale=3.0)

running = True
while running:
    screen.fill((0, 0, 0))
    
    keys = pygame.key.get_pressed()
    player.update(keys)
    player.draw(screen)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.attack()
            # elif event.key == pygame.K_f:  # Example: Press 'F' to shoot
            #     player.shoot()

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
