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

# Laser class
class Laser:
    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.image = image
        self.mask = pygame.mask.from_surface(self.image)

    def draw(self, window):
        window.blit(self.image, (self.x, self.y))

    def move(self, vel):
        self.y += vel

    def off_screen(self, height):
        return not (self.y <= height and self.y >= 0)
    
    # Check to see if an object is colliding with the laser
    def collision(self, obj):
        return collide(obj, self)

def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    # Return True or False depending on if two objects are overlapping each other
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None

# Ship class
class Ship:
    COOLDOWN = 25
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
        for laser in self.lasers:
            laser.draw(WINDOW)

    def move_lasers(self, vel, obj):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            elif laser.collision(obj):
                obj.health -= 10
                self.lasers.remove(laser)

    def cooldown(self):
        if self.cool_down_counter >= self.COOLDOWN:
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1

    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1

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
    
    def move_lasers(self, vel, objs):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            # The lasers will move and if it is off screen
            if laser.off_screen(HEIGHT):
                # Delete laser shot
                self.lasers.remove(laser)
            else:
                # Else, for every enemy ship (aka object) in the game
                for obj in objs:
                    # If the laser hits a ship
                    if laser.collision(obj):
                        # Remove the ship from the game
                        objs.remove(obj)
                        self.lasers.remove(laser)
    def draw(self, window):
        super().draw(window)
        self.healthbar(window)

    def healthbar(self, window):
        # Draw a healthbar 10 pixels above the height of the player ship
        pygame.draw.rect(window, (255, 0, 0), (self.x, self.y + self.ship.img.get_height() + 10, self.ship_img.get_width(), 10))
        pygame.draw.rect(window, (0, 255, 0), (self.x, self.y + self.ship.img.get_height() + 10, self.ship_img.get_width() * ((self.health)/self.max_health), 10))

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

    # Offset the position where enemy shoots shoot their lasers
    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x-18, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1


# Create main event loop to handle all events
def main():
    run = True
    # Frame rate
    FPS = 60
    level = 0
    lives = 5
    clock = pygame.time.Clock()
    main_font = pygame.font.SysFont("comicsans", 50)
    lost_font = pygame.font.SysFont("comicsans", 60)


    enemies = []
    # Wave of enemies
    wave_length = 5
    # Enemy velocity
    enemy_vel = 1
    # Laser velocity
    laser_vel = 6

    player_velocity = 5 # Move 5 pixels
    
    player = Player(300, 650)

    lost = False
    lost_timer = 0

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

        if lost:
            lost_label = lost_font.render("Game Over... You Lost!!",1, (255, 255, 255))
            WINDOW.blit(lost_label, (WIDTH/2 - lost_label.get_width()/2, 350))
        
        pygame.display.update()

    while run:
        clock.tick(FPS)
        redraw_window()

        if lives <= 0 or player.health <= 0:
            lost = True
            lost_timer += 1
        
        # If the player has lost, and the lost timer is greater than 5 second then stop the game
        if lost:
            if lost_timer > FPS * 5:
                run = False
            else: 
                continue

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
        if keys[pygame.K_SPACE]:
            player.shoot()

        for enemy in enemies[:]:
            enemy.move(enemy_vel)
            enemy.move_lasers(laser_vel, player)
            
            if random.randrange(0, 2*60) == 1:
                enemy.shoot()

            if collide(enemy, player):
                player.health -= 10
                enemies.remove(enemy)
            
            if collide(enemy, player):
                player.health -= 10
                enemies.remove(enemy)

            elif enemy.y + enemy.get_height() > HEIGHT:
            # If enemy ships move out of the screen, decrease the number of lives
                lives -= 1
                enemies.remove(enemy)
        
        player.move_lasers(-laser_vel, enemies)

main()