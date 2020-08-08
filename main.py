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
        pygame.draw.rect(window, (255, 0, 0), (self.x, self.y, 50, 50))

# Create main event loop to handle all events
def main():
    run = True
    # Frame rate
    FPS = 60
    level = 1
    lives = 5
    clock = pygame.time.Clock()
    main_font = pygame.font.SysFont("comicsans", 50)
    
    player_velocity = 5 # Move 5 pixels
    
    ship = Ship(300, 650)

    def redraw_window():
        # The blit method takes one of the images provided and draws it on the window
        # Draw image background at point 0, 0
        WINDOW.blit(BACKGROUND, (0,0))      
        # draw text
        lives_label = main_font.render(f"Lives: {lives}", 1, (255, 255, 255))
        level_label = main_font.render(f"Level: {level}", 1, (255, 255, 255))
        
        WINDOW.blit(lives_label, (10, 10))
        WINDOW.blit(level_label, (WIDTH - level_label.get_width() - 10, 10))
        
        ship.draw(WINDOW)
        
        pygame.display.update()

    while run:
        clock.tick(FPS)
        redraw_window()
        for event in pygame.event.get():
            # if event has occured, do something
            if event.type == pygame.QUIT:
                run = False

        # Returns a dictionary of all keys pressed during runtime
        keys = pygame.key.get_pressed()
        # Will look for arrow keys
        if keys[pygame.K_LEFT]: # Move left
            ship.x -= player_velocity
        if keys[pygame.K_RIGHT]: # Move right
            ship.x += player_velocity
        if keys[pygame.K_UP]: # Move up
            ship.y -= player_velocity
        if keys[pygame.K_DOWN]: # Move down
            ship.y += player_velocity

main()