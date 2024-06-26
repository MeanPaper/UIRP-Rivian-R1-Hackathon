import pygame

class Platform:
    def __init__(self, screen, elevations, platform_width, platform_height, acc, maxVelo, mileage=100, currMileage=0):
        self.screen = screen
        self.elevations = elevations
        self.platform_width = platform_width
        self.platform_height = platform_height
        self.segments = self._create_segments()
        self.acc = acc
        self.maxVelo = maxVelo
        self.mileage = mileage

        self.velocity = pygame.Vector2(0, 0)

    def _create_segments(self):
        # Create platform segments based on elevations
        segments = []
        for i, elevation in enumerate(self.elevations):
            x = i * self.platform_width
            y = self.screen.get_height() - elevation
            segment = (x, y)
            segments.append(segment)
        return segments

    def draw(self):
        # Draw the platform segments
        for i in range(len(self.segments) - 1):
            pygame.draw.line(
                self.screen,
                (0, 255, 0),
                self.segments[i],
                self.segments[i + 1],
                5  # Line thickness
            )

    def scroll(self, offset_x, offset_y):
        # Scroll the platform based on the car's movement
        for i in range(len(self.segments)):
            self.segments[i] = (self.segments[i][0] - offset_x, self.segments[i][1] + offset_y)

    def check_collision(self, car_rect):
        # Check for collisions with the car
        for i in range(len(self.segments) - 1):
            if self._line_rect_collision(self.segments[i], self.segments[i + 1], car_rect):
                return True
        return False

    def _line_rect_collision(self, line_start, line_end, rect):
        # Check if a line segment intersects with a rectangle (car)
        line_rect = pygame.Rect(min(line_start[0], line_end[0]), min(line_start[1], line_end[1]), abs(line_start[0] - line_end[0]), abs(line_start[1] - line_end[1]))
        return rect.colliderect(line_rect)
    

    def get_ground_y(self, x):
        # Get the y-coordinate of the ground at a specific x-coordinate
        for i in range(len(self.segments) - 1):
            if self.segments[i][0] <= x <= self.segments[i + 1][0]:
                # Interpolate the y value
                x1, y1 = self.segments[i]
                x2, y2 = self.segments[i + 1]
                return y1 + (y2 - y1) * (x - x1) / (x2 - x1)
        return self.segments[-1][1]  # If x is beyond the platform, return the last segment's y


    def update(self, screen, dt, platform):
        self.velocity.y += self.gravity * dt
        self.rect.y += self.gravity * dt

        ground_y = platform.get_ground_y(self.rect.centerx)
        if self.rect.bottom >= ground_y:
            self.rect.bottom = ground_y
            self.velocity.y = 0
        
        if self.rect.top < 0:
            self.rect.top = 0
            self.velocity.y = 0
        elif self.rect.bottom > screen.get_height():
            self.rect.bottom = screen.get_height()
            self.velocity.y = 0
