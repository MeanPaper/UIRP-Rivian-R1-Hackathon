import pygame

class Platform:
    def __init__(self, screen, elevations, platform_width, platform_height):
        self.screen = screen
        self.elevations = elevations
        self.platform_width = platform_width
        self.platform_height = platform_height
        self.segments = self._create_segments()

        self.scroll_offset = pygame.Vector2(0, 0)

    def _create_segments(self):
        # Create platform segments based on elevations
        segments = []
        for i, elevation in enumerate(self.elevations):
            x = i * self.platform_width
            y = self.screen.get_height() - elevation
            segment = pygame.Vector2(x, y)
            segments.append(segment)
        return segments


    def draw(self, car_rect):
        # Draw the platform segments
        for i in range(len(self.segments) - 1):
            start_pos = (self.segments[i].x - self.scroll_offset.x, self.segments[i].y + (self.scroll_offset.y if not self.check_collision(car_rect) else 0))
            end_pos = (self.segments[i + 1].x - self.scroll_offset.x, self.segments[i + 1].y + (self.scroll_offset.y if not self.check_collision(car_rect) else 0))
            pygame.draw.line(
                self.screen,
                (0, 255, 0),
                start_pos,
                end_pos,
                5  # Line thickness
            )


    def scroll(self, offset_x, offset_y):
        # Scroll the platform based on the car's movement
        self.scroll_offset.x += offset_x
        self.scroll_offset.y += offset_y

    def check_collision(self, car_rect):
        # Check for collisions with the car
        for i in range(len(self.segments) - 1):
            start_pos = (self.segments[i].x - self.scroll_offset.x, self.segments[i].y)
            end_pos = (self.segments[i + 1].x - self.scroll_offset.x, self.segments[i + 1].y)
            if self._line_rect_collision(start_pos, end_pos, car_rect):
                return True
        return False

    def _line_rect_collision(self, line_start, line_end, rect):
        # Check if a line segment intersects with a rectangle (car)
        line_rect = pygame.Rect(min(line_start[0], line_end[0]), min(line_start[1], line_end[1]), abs(line_start[0] - line_end[0]), abs(line_start[1] - line_end[1]))
        return rect.colliderect(line_rect)
    
    def get_ground_y(self, x):
        # Get the y-coordinate of the ground at a specific x-coordinate
        adjusted_x = x + self.scroll_offset.x
        for i in range(len(self.segments) - 1):
            if self.segments[i].x <= adjusted_x <= self.segments[i + 1].x:
                # Interpolate the y value
                x1, y1 = self.segments[i]
                x2, y2 = self.segments[i + 1]
                return y1 + (y2 - y1) * (adjusted_x - x1) / (x2 - x1)
        return self.segments[-1][1]  # If x is beyond the platform, return the last segment's y
