import pygame

class Sprite:
    def __init__(self, model_path, screen, height, width, x, y, state=0):
        self.sprite_sheet = pygame.image.load(model_path)
        self.position = pygame.Vector2(x, y)
        self.state = state
        self.screen = screen
        self.height = height
        self.width = width

        # Calculate sprite dimensions
        self.sprite_width = self.sprite_sheet.get_width()
        self.sprite_height = self.sprite_sheet.get_height() // 3

    def draw(self):
        # Calculate the crop area for the current state
        crop_rect = pygame.Rect(0, self.state * self.sprite_height, self.sprite_width, self.sprite_height)
        sprite_image = self.sprite_sheet.subsurface(crop_rect)
        scaled_image = pygame.transform.scale(sprite_image, (self.width, self.height))
        self.screen.blit(scaled_image, (self.position.x, self.position.y))

    def update(self):
        # Cycle through the states
        self.state = (self.state + 1) % 3
        self.draw()