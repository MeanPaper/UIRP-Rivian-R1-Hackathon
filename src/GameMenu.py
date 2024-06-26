import pygame
import sys

class GameMenu:
    def __init__(self, screen, items):
        self.screen = screen
        self.items = items
        self.font = pygame.font.Font(None, 36)

    def display(self):
        for index, item in enumerate(self.items):
            text = self.font.render(item, True, (255, 255, 255))
            self.screen.blit(text, (100, 100 + index * 60))

    def run(self):
        while True:
            self.screen.fill((0, 0, 0))
            self.display()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:  # Start the game
                        return

            pygame.display.flip()