import pygame

class MasterRender:
    def __init__(self, char_name, x, y, scale=1.0):
        pygame.init()
        
        self.char_name = char_name
        self.x = x
        self.y = y
        self.vel = 5 * scale  # Apply scaling to movement speed
        self.scale = scale
        self.current_action = "attack_e"
        self.frame_index = 0
        self.last_update = pygame.time.get_ticks()
        self.animation_speed = 100  # milliseconds per frame

        self.load_sprites()

    def load_sprites(self):
        directions = ["n", "s", "e", "w", "ne", "nw", "se", "sw"]
        self.sprite_sequences = {}
        
        for direction in directions:
            self.sprite_sequences[f"run_{direction}"] = [pygame.transform.scale(
                pygame.image.load(f"{self.char_name}_run_{direction}_{i}.png"),
                (int(64 * self.scale), int(64 * self.scale))
            ) for i in range(1, 6)]
            
            self.sprite_sequences[f"attack_{direction}"] = [pygame.transform.scale(
                pygame.image.load(f"{self.char_name}_attack_{direction}_{i}.png"),
                (int(64 * self.scale), int(64 * self.scale))
            ) for i in range(1, 6)]
            
            # self.sprite_sequences[f"shot_{direction}"] = [pygame.transform.scale(
            #     pygame.image.load(f"{self.char_name}_shot_{direction}_{i}.png"),
            #     (int(32 * self.scale), int(32 * self.scale))
            # ) for i in range(1, 6)]
        
        self.image = self.sprite_sequences[self.current_action][self.frame_index]

    def update(self, keys):
        direction = None
        
        if keys[pygame.K_UP] and keys[pygame.K_RIGHT]:
            direction = "ne"
        elif keys[pygame.K_UP] and keys[pygame.K_LEFT]:
            direction = "nw"
        elif keys[pygame.K_DOWN] and keys[pygame.K_RIGHT]:
            direction = "se"
        elif keys[pygame.K_DOWN] and keys[pygame.K_LEFT]:
            direction = "sw"
        elif keys[pygame.K_UP]:
            direction = "n"
        elif keys[pygame.K_DOWN]:
            direction = "s"
        elif keys[pygame.K_LEFT]:
            direction = "w"
        elif keys[pygame.K_RIGHT]:
            direction = "e"
        
        if direction:
            self.x += (self.vel if "e" in direction else -self.vel if "w" in direction else 0)
            self.y += (self.vel if "s" in direction else -self.vel if "n" in direction else 0)
            self.current_action = f"run_{direction}"
        
        if keys[pygame.K_SPACE]:  # Attack
            self.current_action = f"attack_{direction}" if direction else self.current_action
        
        # Handle animation timing
        now = pygame.time.get_ticks()
        if now - self.last_update > self.animation_speed:
            self.last_update = now
            self.frame_index = (self.frame_index + 1) % len(self.sprite_sequences[self.current_action])
            self.image = self.sprite_sequences[self.current_action][self.frame_index]

    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))
    
    def attack(self):
        self.frame_index = 0
        self.current_action = f"attack_{self.current_action.split('_')[1]}"

    # def shoot(self):
    #     self.frame_index = 0
    #     self.current_action = f"shot_{self.current_action.split('_')[1]}"
