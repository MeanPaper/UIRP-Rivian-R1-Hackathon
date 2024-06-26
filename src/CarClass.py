import pygame

class Car:
    def __init__(self, model_path, acc, maxVelo, mileage=100, x=0, y=0, width=50, height=30):
        self.model = pygame.image.load(model_path)
        self.model = pygame.transform.scale(self.model, (width, height))
        self.model = pygame.transform.flip(self.model, True, False)
        self.rect = self.model.get_rect(center=(x, y))
        self.acc = acc
        self.maxVelo = maxVelo
        self.mileage = mileage

    def draw(self, screen):
        screen.blit(self.model, self.rect.topleft)

    # Setters
    def setAcc(self, newAcc):
        self.acc = newAcc
    
    def setMaxVelo(self, newMaxVelo):
        self.maxVelo = newMaxVelo

    def setModel(self, model_path):
        self.model = pygame.image.load(model_path)
        self.model = pygame.transform.scale(self.model, (width, height))
        self.model = pygame.transform.flip(self.model, True, False)

    def setMileage(self, newMileage):
        self.mileage = newMileage