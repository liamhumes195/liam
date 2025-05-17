import pygame
import random
import sys
import traceback

try:
    # Initialize Pygame
    pygame.init()
    print("Pygame initialized successfully")

    # Constants
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
    BLOCK_SIZE = 50
    GRAVITY = 0.8
    JUMP_FORCE = -15

    # Colors
    WHITE = (255, 255, 255)
    GREEN = (0, 255, 0)
    BROWN = (139, 69, 19)
    BLUE = (0, 0, 255)

    # Set up the display
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Simple Minecraft")
    print("Display initialized successfully")

except Exception as e:
    print(f"Error initializing game: {str(e)}")
    traceback.print_exc()
    sys.exit(1)

class Player:
    def __init__(self):
        self.x = SCREEN_WIDTH // 2
        self.y = SCREEN_HEIGHT - BLOCK_SIZE
        self.width = BLOCK_SIZE
        self.height = BLOCK_SIZE
        self.velocity_y = 0
        self.on_ground = False

    def update(self):
        # Apply gravity
        self.velocity_y += GRAVITY
        self.y += self.velocity_y

        # Check for ground collision
        if self.y + self.height > SCREEN_HEIGHT:
            self.y = SCREEN_HEIGHT - self.height
            self.velocity_y = 0
            self.on_ground = True

    def jump(self):
        if self.on_ground:
            self.velocity_y = JUMP_FORCE
            self.on_ground = False

    def draw(self):
        pygame.draw.rect(screen, WHITE, (self.x, self.y, self.width, self.height))

class Block:
    def __init__(self, x, y, block_type):
        self.x = x
        self.y = y
        self.width = BLOCK_SIZE
        self.height = BLOCK_SIZE
        self.block_type = block_type

    def draw(self):
        if self.block_type == "grass":
            color = GREEN
        elif self.block_type == "dirt":
            color = BROWN
        elif self.block_type == "water":
            color = BLUE
        pygame.draw.rect(screen, color, (self.x, self.y, self.width, self.height))

def generate_world():
    blocks = []
    # Generate ground
    for x in range(0, SCREEN_WIDTH, BLOCK_SIZE):
        blocks.append(Block(x, SCREEN_HEIGHT - BLOCK_SIZE, "grass"))
        blocks.append(Block(x, SCREEN_HEIGHT - 2 * BLOCK_SIZE, "dirt"))
        blocks.append(Block(x, SCREEN_HEIGHT - 3 * BLOCK_SIZE, "dirt"))
    
    # Generate some random blocks
    for _ in range(10):
        x = random.randint(0, SCREEN_WIDTH - BLOCK_SIZE)
        # Ensure y values are within valid range
        y = random.randint(SCREEN_HEIGHT - 5 * BLOCK_SIZE, SCREEN_HEIGHT - 4 * BLOCK_SIZE)
        blocks.append(Block(x, y, "dirt"))
    
    return blocks

def main():
    player = Player()
    blocks = generate_world()
    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.jump()

        # Update player position
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player.x -= 5
        if keys[pygame.K_RIGHT]:
            player.x += 5

        # Keep player within screen bounds
        player.x = max(0, min(SCREEN_WIDTH - player.width, player.x))

        # Update game state
        player.update()

        # Draw everything
        screen.fill((135, 206, 235))  # Sky blue background
        
        for block in blocks:
            block.draw()
        
        player.draw()
        
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
