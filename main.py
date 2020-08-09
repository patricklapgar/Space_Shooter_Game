# Main file for Space Invaders computer game
import pygame
import os
import time
import random
pygame.font.init()

# Initialize pygame window
WIDTH, HEIGHT = 750, 750
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders Clone")

# Upload image assets
RED_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_red_small.png"))
GREEN_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_green_small.png"))
BLUE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_blue_small.png"))

# Player ship
YELLOW_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_yellow.png"))

# Upload laser images
RED_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_red.png"))
GREEN_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_green.png"))
BLUE_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_blue.png"))
YELLOW_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_yellow.png"))

# Upload background image
BACKGROUND = pygame.transform.scale(pygame.image.load(os.path.join("assets", "background-black.png")), (WIDTH, HEIGHT))

# Ship class
class Ship:
    # There are enemy ships and the player ship
    # This class will be abstract other classes will inherit from it
    def __init__(self, x, y, health=100):
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = None
        self.laser_img = None
        self.lasers = []
        # How much time until the player can shoot another laser
        self.cool_down_counter = 0

    def draw(self, window):
        window.blit(self.ship_img, (self.x, self.y))

    def get_width(self):
        return self.ship_img.get_width()

    def get_height(self):
        return self.ship_img.get_height()

# Player class inherits from Ship
class Player(Ship):
    def __init__(self, x, y, health=100):
        super().__init__(x, y, health)
        self.ship_img = YELLOW_SHIP
        self.laser_img = YELLOW_LASER
        # Create a mask to create pixel-perfect collisions
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health

# Enemy ship class
class Enemy(Ship):
    # Dictionary that maps an enemy color to a ship
    COLOR_MAP = {
        "red": (RED_SHIP, RED_LASER),
        "green": (GREEN_SHIP, GREEN_LASER),
        "blue": (BLUE_SHIP, BLUE_LASER)
    }

    def __init__(self, x, y, color, health=100):
        super().__init__(x, y, health)
        self.ship_img, self.laser_img = self.COLOR_MAP[color]
        # Create mask
        self.mask = pygame.mask.from_surface(self.ship_img)

    def move(self, vel):
        self.y += vel


# Create main event loop to handle all events
def main():
    run = True
    # Frame rate
    FPS = 60
    level = 0
    lives = 5
    clock = pygame.time.Clock()
    main_font = pygame.font.SysFont("comicsans", 50)
    
    enemies = []
    # Wave of enemies
    wave_length = 5
    # Enemy velocity
    enemy_vel = 1

    player_velocity = 5 # Move 5 pixels
    
    player = Player(300, 650)

    def redraw_window():
        # The blit method takes one of the images provided and draws it on the window
        # Draw image background at point 0, 0
        WINDOW.blit(BACKGROUND, (0,0))      
        # draw text
        lives_label = main_font.render(f"Lives: {lives}", 1, (255, 255, 255))
        level_label = main_font.render(f"Level: {level}", 1, (255, 255, 255))
        
        WINDOW.blit(lives_label, (10, 10))
        WINDOW.blit(level_label, (WIDTH - level_label.get_width() - 10, 10))
        
        for enemy in enemies:
            enemy.draw(WINDOW)

        player.draw(WINDOW)
        
        pygame.display.update()

    while run:
        clock.tick(FPS)
        
        # If all enemies are destroyed
        if len(enemies) == 0:
            # Increase level and number of enemies
            level += 1
            wave_length += 5
            for i in range(wave_length):
                enemy = Enemy(random.randrange(50, WIDTH - 100), random.randrange(-1500, -100), random.choice(["red", "blue", "green"]))
                enemies.append(enemy)

        for event in pygame.event.get():
            # if event has occured, do something
            if event.type == pygame.QUIT:
                run = False

        # Returns a dictionary of all keys pressed during runtime
        keys = pygame.key.get_pressed()
        # Will look for arrow keys
        if keys[pygame.K_LEFT] and player.x - player_velocity > 0: # Move left
            player.x -= player_velocity
        if keys[pygame.K_RIGHT] and player.x + player_velocity + player.get_width() < WIDTH: # Move right
            player.x += player_velocity
        if keys[pygame.K_UP] and player.y - player_velocity > 0: # Move up
            player.y -= player_velocity
        if keys[pygame.K_DOWN] and player.y + player_velocity + player.get_height() < HEIGHT: # Move down
            player.y += player_velocity
        
        for enemy in enemies:
            enemy.move(enemy_vel)

        redraw_window()

main()