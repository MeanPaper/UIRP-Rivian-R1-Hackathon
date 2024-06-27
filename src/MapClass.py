import pygame
from datetime import datetime
import Macros
import colorsys

class Platform:
    def __init__(self, screen, elevations, platform_width, platform_height, instructions):
        self.screen = screen
        self.elevations = elevations
        self.platform_width = platform_width
        self.platform_height = platform_height
        self.instructions = instructions
        self.car_moved = False

        self.update_elevations()

        self.scroll_offset = pygame.Vector2(0, 0)

    def update_elevations(self):
        # Create platform elevations based on elevations
        for i in range(len(self.elevations)):
            self.elevations[i] = self.screen.get_height() - self.elevations[i]

    def update(self, car_x_pos, car_rect):
        # print("Update")
        car_x_pos = int(car_x_pos)

        if not self.check_collision(car_x_pos, car_rect):
            for i in range(len(self.elevations)):            
                # self.elevations[i] -= (3)
                self.elevations[i] -= self.scroll_offset.y if self.scroll_offset.y < Macros.TERMINAL_VELOCITY else Macros.TERMINAL_VELOCITY
        if self.uphill(car_x_pos) and self.car_moved:
            for i in range(len(self.elevations)):
                self.elevations[i] += 1
    

    def draw(self, car_x_pos):
        car_x_pos = int(car_x_pos)
        # Draw the platform elevations
        for i in range(car_x_pos, car_x_pos + Macros.WINDOW_WIDTH):
        # for i in range(len(self.elevations)):
            if i > len(self.elevations) - 2:
                start_pos = (i - car_x_pos, 0)
                end_pos = (i + 1 - car_x_pos, 0)
            else:
                start_pos = (i - car_x_pos, self.elevations[i])
                end_pos = (i + 1 - car_x_pos, self.elevations[i + 1])

            realtime_hour = datetime.now().hour
            lumin_scale = Macros.shadow_scale(realtime_hour)
            black_hls = (0, 0.6 * lumin_scale, 0)
            black_rgb = colorsys.hls_to_rgb(*black_hls)
            black_rgb = tuple(int(255 * i) for i in black_rgb)

            color = black_rgb if (i - car_x_pos - 20 >= 0 and i - car_x_pos - 20 <= 128) else (45,45,45)
            if (i % 6000 > 0 and i % 6000 < 80):
                color = (0, 0, 255)
            polygon_pts = [start_pos, end_pos, (end_pos[0], self.screen.get_height()), (start_pos[0], self.screen.get_height())]
            pygame.draw.polygon(self.screen, (138,70,45), polygon_pts)

            pygame.draw.line(
                self.screen,
                color,
                start_pos,
                end_pos,
                70  # Line thickness
            )

    def scroll(self, offset_x, offset_y, car_x_pos, car_rect):
        # Scroll the platform based on the car's movement
        self.scroll_offset.y = offset_y
        self.update(car_x_pos, car_rect)

    def get_slope(self, x):
        # print(((self.elevations[x+128]) - (self.elevations[x])) / 128)
        return ((self.elevations[x+128]) - (self.elevations[x])) / 128

    def uphill(self, car_x_pos):
        # print(self.elevations[car_x_pos + 128], self.elevations[car_x_pos])
        return self.elevations[car_x_pos + 128] < (self.elevations[car_x_pos])

    def check_collision(self, car_x_pos, car_rect):
        car_x_pos = int(car_x_pos)
        # Check for collisions with the car
        if car_x_pos < 0 or car_x_pos > len(self.elevations) - 2:
            return False

        # if (self.elevations[car_x_pos + 128] > self.elevations[car_x_pos]):
        return car_rect.bottomright[1] >= self.elevations[car_x_pos + 128] or car_rect.bottomleft[1] >= self.elevations[car_x_pos]