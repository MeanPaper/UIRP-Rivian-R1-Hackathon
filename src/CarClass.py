import pygame
import math
class Car:
    def __init__(self, model_path, acc, maxVelo, mileage=100, x=0, y=0, width=50, height=30):
        self.model = pygame.image.load(model_path)
        self.model = pygame.transform.scale(self.model, (width, height))
        self.model = pygame.transform.flip(self.model, True, False)
        self.original_model = self.model
        self.rect = self.model.get_rect(center=(x, y))
        self.acc = acc
        self.maxVelo = maxVelo
        self.mileage = mileage
        self.x_pos = 84
        
        self.angle = 0
        self.rotate_true = False
        self.slope = 0

        self.velocity = 0

    def update(self, offset_x, platform):
        self.x_pos += offset_x

        slope = platform.get_slope(self.x_pos)
        self.rotate_true = True if slope != self.slope else False
        self.angle = math.atan(slope)
        self.slope = slope


    def draw(self, screen):

        self.model = pygame.transform.rotate(self.original_model, -math.degrees(self.angle)) if self.rotate_true else self.model
        screen.blit(self.model, self.rect.topleft)