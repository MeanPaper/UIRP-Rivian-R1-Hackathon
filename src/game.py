import pygame
import sys
from CarClass import Car
from MapClass import Platform

# Game window macros
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
FONT_NAME = "Open Sans"
FONT_SIZE_L = 32
FONT_SIZE_M = 24
FONT_SIZE_S = 16
GRAVITY = -1

# Initialize Pygame
pygame.init()

# Game Font
game_font = pygame.font.SysFont(FONT_NAME, FONT_SIZE_L)

# Add clock
clock = pygame.time.Clock()

# Set up the screen
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

# TODO: change the name later
pygame.display.set_caption("Rivian Hill Climber")

# Platform dimensions
platform_width = 10
platform_height = 20

# Elevation data (example)
elevations = [100, 102, 103, 102, 101, 100] * 20

# Create the platform
platform = Platform(screen, elevations, platform_width, platform_height)
offset_x = 0
offset_y = 0

# Game Car Character
car = Car('../assets/White_R1T.png', 50, 100, 100, x=WINDOW_WIDTH / 2, y=WINDOW_HEIGHT / 2, width=1280/10, height=960/10)

text = game_font.render('Press Enter to start', True, (255, 255, 255))

# Game menu:
game_start = False
while not game_start:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:  # Start the game
                game_start = True
                break

    # Draw the text
    screen.blit(text, (WINDOW_WIDTH / 2 - text.get_width() / 2, WINDOW_HEIGHT / 2 - text.get_height() / 2))

    # Update the display
    pygame.display.flip()   

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Get the state of the keyboard
    keys = pygame.key.get_pressed()

    # Update the car's position and velocity
    dt = clock.get_time() / 1000  # Convert milliseconds to seconds
        
    # Scroll the platform based on the car's horizontal movement
    offset_x = 0
    offset_y += GRAVITY * dt
    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        offset_x += car.acc * dt if car.acc * dt < car.maxVelo else car.maxVelo
    elif keys[pygame.K_a] or keys[pygame.K_LEFT]:
        offset_x -= car.acc * dt if car.acc * dt < car.maxVelo else car.maxVelo

    # Update the platform position with gravity
    screen.fill((136, 206, 235))

    platform.scroll(offset_x, offset_y)
    platform.draw(car.rect)
    car.draw(screen)
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)