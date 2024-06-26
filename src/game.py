import pygame
import sys
import Macros # game macros
from CarClass import Car
from MapClass import Platform
from GameMenu import GameMenu
import math

# Initialize Pygame
pygame.init()

# Game Font
game_font = pygame.font.SysFont(Macros.FONT_NAME, Macros.FONT_SIZE_L)

# Add clock
clock = pygame.time.Clock()

# Set up the screen
screen = pygame.display.set_mode((Macros.WINDOW_WIDTH, Macros.WINDOW_HEIGHT))

# TODO: change the name later
pygame.display.set_caption("PRANAV SWAMINATHAN Hill Climber")

# Platform dimensions
platform_width = 10
platform_height = 20

# Elevation data (example)
# elevations = [100] * 1000
# elevations = ([y for x in range(100, 20, -2) for y in (x//2, x//2, x//2, x//2, x//2, x//2, x//2, x//2, x//2)] + [y for x in range(20, 100, 2) for y in (x//2, x//2, x//2, x//2, x//2, x//2, x//2, x//2, x//2)]) * 50
elevations = (
    [y for x in range(100, -40, -1) for y in (x//2,) * 5] +
    [y for x in range(-40, 100, 1) for y in (x//2,) * 5]
) * 50

# Create the platform
platform = Platform(screen, elevations, platform_width, platform_height)
offset_x = 0
offset_y = 0

# Game Car Character
car = Car('/Users/dongmingsbrick/Desktop/UIRP-Rivian-R1-Hackathon/assets/R1T_GREY.png', 50, 20, 100, x=84, y=Macros.WINDOW_HEIGHT / 2, width=1280/10, height=960/10)

text = game_font.render('Press Enter to start', True, (255, 255, 255))

# Game menu:
game_menu = GameMenu(screen, Macros.FONT_NAME, options=['Start'])

game_start = False
if game_menu.run() != Macros.GameMenuCode.MENU_EXIT_OK:
    print("Game menu exited with an error.")
    exit(1)
game_start = True 
# game_start = False
# Game loop
while game_start:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            # sys.exit()

    # Get the state of the keyboard
    keys = pygame.key.get_pressed()

    # Update the car's position and velocity
    dt = clock.get_time() / 100
        
    # Scroll the platform based on the car's horizontal movement
    offset_x = 0
    offset_y = 1
    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        offset_x += math.ceil(car.acc * dt if car.acc * dt < car.maxVelo else car.maxVelo)
    elif keys[pygame.K_a] or keys[pygame.K_LEFT]:
        offset_x -= math.ceil(car.acc * dt if car.acc * dt < car.maxVelo else car.maxVelo)
    
    if offset_x != 0:
        platform.car_moved = True
    else:
        platform.car_moved = False

    # print(offset_x)
    if keys[pygame.K_ESCAPE]: # end game and quick
        game_start = False
        break
        
    # Update the platform position with gravity
    screen.fill((136, 206, 235))

    platform.scroll(offset_x, offset_y, car.x_pos, car.rect)
    car.update(offset_x, platform)
    platform.draw(car.x_pos)
    car.draw(screen)
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(600)


