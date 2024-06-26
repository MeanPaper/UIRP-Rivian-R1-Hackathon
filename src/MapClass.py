import pygame
import Macros
class Platform:
    def __init__(self, screen, elevations, platform_width, platform_height):
        self.screen = screen
        self.elevations = elevations
        self.platform_width = platform_width
        self.platform_height = platform_height

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
                self.elevations[i] -= (3)
        if self.uphill(car_x_pos) and self.car_moved:
            for i in range(len(self.elevations)):
                self.elevations[i] += (1)
    

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

            color = (255, 0, 0) if (i - car_x_pos - 20 >= 0 and i - car_x_pos - 20 <= 128) else (0, 255, 0)
            pygame.draw.line(
                self.screen,
                color,
                start_pos,
                end_pos,
                8  # Line thickness
            )

    def scroll(self, offset_x, offset_y, car_x_pos, car_rect):
        # Scroll the platform based on the car's movement
        self.scroll_offset.y += offset_y
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

        start_pos = (car_x_pos, self.elevations[car_x_pos])
        end_pos = (car_x_pos + 128, self.elevations[car_x_pos + 128])

        # if (self.elevations[car_x_pos + 128] > self.elevations[car_x_pos]):
        return car_rect.bottomright[1] >= self.elevations[car_x_pos + 128] or car_rect.bottomleft[1] >= self.elevations[car_x_pos]
            # return car_rect.bottomright[1] > self.elevations[car_x_pos + 128]
        # else:
            # return car_rect.bottomleft[1] >= self.elevations[car_x_pos]

        # return self._line_rect_collision(start_pos, end_pos, car_rect)

    def _line_rect_collision(self, line_start, line_end, car_rect):
        # Check if a line segment intersects with a rectangle (car)
        line_rect = pygame.Rect(min(line_start[0], line_end[0]), min(line_start[1], line_end[1]), abs(line_end[0] - line_start[0]), abs(line_end[1] - line_start[1]))
        return car_rect.colliderect(line_rect)
    
    def get_ground_y(self, x):
        # Get the y-coordinate of the ground at a specific x-coordinate
        adjusted_x = x + self.scroll_offset.x
        for i in range(len(self.elevations) - 1):
            if i <= adjusted_x < i + 1:
                # Interpolate the y value
                x1, y1 = self.elevations[i]
                x2, y2 = self.elevations[i + 1]
                return y1 + (y2 - y1) * (adjusted_x - x1) / (x2 - x1)
        return self.elevations[-1]  # If x is beyond the platform, return the last segment's y