import pygame
import sys
import Macros
from typing import Dict, Any

class GameMenu:
    def __init__(self, screen, game_font="Open Sans", font_color=(255, 255, 255), **kwargs: Dict[str, Any]):
        self.screen = screen
        self.font = pygame.font.SysFont(game_font, 36)
        self.font_color = font_color

    def run(self, object_dict: Dict[str, Any] = {}):
        """
        object_dict: output dictionary of object and information will be used in game,
                     the default value is for debugging purposes
        """
        begin_text = self.font.render('Press Enter to start', True, self.font_color)

        while True:
            self.screen.fill((0, 0, 0)) # background color

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:  # Start the game
                        return Macros.GameMenuCode.MENU_EXIT_OK
            
            self.screen.blit(begin_text, (Macros.WINDOW_WIDTH / 2 - begin_text.get_width() / 2, Macros.WINDOW_HEIGHT / 2 - begin_text.get_height() / 2))
            pygame.display.flip()