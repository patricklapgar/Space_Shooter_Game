# Main file for Space Invaders computer game
import pygame
import os
import time
import random

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
BACKGROUND = pygame.image.load(os.path.join("assets", "background-black.png"))

# Create main event loop to handle all events
def main():
    run = True
    # Frame rate
    FPS = 60
    clock = pygame.time.Clock()

    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            # if event has occured, do something
            if event.type == pygame.QUIT:
                run = False
            
main()