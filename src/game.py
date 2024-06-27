import pygame
import sys
import os
import math
from datetime import datetime
import color_util

sys.path.append('../')
from CarClass import Car
from MapClass import Platform
from Sprites import Sprite
from api.elevation import check_distance, get_elevation, get_route
from api.emission import read_and_merge, generate_mapping, calculate_emission

# Assuming Macros.py has appropriate constants defined
import Macros

class Button:
    def __init__(self, x, y, width, height, image=None, text=None, font=None, font_color=None, action=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = pygame.transform.scale(image, (width, height)) if image else None
        self.text = text
        self.font = font
        self.font_color = font_color
        self.action = action
        self.rect = pygame.Rect(x, y, width, height)

    def draw(self, screen):
        if self.image:
            screen.blit(self.image, (self.x, self.y))
        if self.text:
            pygame.draw.rect(screen, (0, 0, 255), self.rect)  # Button color
            text_surf = self.font.render(self.text, True, self.font_color)
            screen.blit(text_surf, (self.x + (self.width - text_surf.get_width()) / 2, self.y + (self.height - text_surf.get_height()) / 2))

    def is_over(self, pos):
        return self.rect.collidepoint(pos)

class TextButton(Button):
    def __init__(self, x, y, width, height, text, font, font_color, action=None):
        super().__init__(x, y, width, height, text=text, font=font, font_color=font_color, action=action)

class TextInput:
    def __init__(self, x, y, width, height, font, font_color, background_color=(255, 255, 255)):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = background_color
        self.text = ''
        self.font = font
        self.font_color = font_color
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = True
            else:
                self.active = False
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    self.active = False
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect, 2 if self.active else 1)
        text_surf = self.font.render(self.text, True, self.font_color)
        screen.blit(text_surf, (self.rect.x + 5, self.rect.y + (self.rect.height - text_surf.get_height()) / 2))

class RadioButton:
    def __init__(self, x, y, radius, text, font, font_color, group):
        self.x = x
        self.y = y
        self.radius = radius
        self.text = text
        self.font = font
        self.font_color = font_color
        self.selected = False
        self.group = group
        group.add_button(self)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if (self.x - event.pos[0]) ** 2 + (self.y - event.pos[1]) ** 2 < self.radius ** 2:
                self.group.select(self)

    def draw(self, screen):
        pygame.draw.circle(screen, self.font_color, (self.x, self.y), self.radius, 2)
        if self.selected:
            pygame.draw.circle(screen, self.font_color, (self.x, self.y), self.radius - 4)
        text_surf = self.font.render(self.text, True, self.font_color)
        screen.blit(text_surf, (self.x + self.radius + 5, self.y - text_surf.get_height() / 2))

class RadioButtonGroup:
    def __init__(self):
        self.buttons = []

    def add_button(self, button):
        self.buttons.append(button)

    def select(self, selected_button):
        for button in self.buttons:
            button.selected = (button == selected_button)

class GameMenu:
    def __init__(self, screen, game_font="Open Sans", font_color=(255, 255, 255)):
        self.screen = screen
        self.font = pygame.font.SysFont(game_font, 36, bold=True)
        self.game_over_font = pygame.font.SysFont(game_font, 18, bold=True)
        self.instr_font = pygame.font.SysFont(game_font, 20)
        self.font_color = font_color
        self.current_page = 'main'
        self.car_images = []
        self.load_car_images()
        self.selected_car_index = 0  # Index of the currently selected car

        # Load a fancy block font for the title
        self.title_font = pygame.font.Font('../assets/fonts/game-font.ttf', 72)

        # Load background image
        self.background_image = pygame.image.load('../assets/background/bg.webp')
        self.background_image = pygame.transform.scale(self.background_image, (Macros.WINDOW_WIDTH, Macros.WINDOW_HEIGHT))

        # Load play button image
        play_button_image = pygame.image.load('../assets/icons/play.png')

        # Load battery sprite
        # self.battery_sprite = Sprite('../assets/icons/battery_state.png', self.screen, 800, 800, 100, 100)
        
        # Ensure the play button is square and not stretched
        button_size = 100  # Define the desired button size
        self.buttons = [
            Button(Macros.WINDOW_WIDTH / 2 - button_size / 2, Macros.WINDOW_HEIGHT / 2 - button_size / 2, button_size, button_size, play_button_image, action=self.goto_car_drop_selection)
        ]

        # Text Inputs for Car 
        self.car_input = TextInput(Macros.WINDOW_WIDTH / 2 - 150, Macros.WINDOW_HEIGHT / 2 - 150, 300, 40, self.font, self.font_color)

        # Text inputs for location
        self.start_location_input = TextInput(Macros.WINDOW_WIDTH / 2 - 150, Macros.WINDOW_HEIGHT / 2 - 100, 300, 40, self.font, self.font_color)
        self.end_location_input = TextInput(Macros.WINDOW_WIDTH / 2 - 150, Macros.WINDOW_HEIGHT / 2, 300, 40, self.font, self.font_color)

        # Radio buttons for level of detail
        self.detail_group = RadioButtonGroup()
        self.radio_buttons = [
            RadioButton(Macros.WINDOW_WIDTH / 2 - 100, Macros.WINDOW_HEIGHT / 2 + 100, 15, "Low", self.font, self.font_color, self.detail_group),
            RadioButton(Macros.WINDOW_WIDTH / 2, Macros.WINDOW_HEIGHT / 2 + 100, 15, "Medium", self.font, self.font_color, self.detail_group),
            RadioButton(Macros.WINDOW_WIDTH / 2 + 100, Macros.WINDOW_HEIGHT / 2 + 100, 15, "High", self.font, self.font_color, self.detail_group)
        ]

    def run(self):
        while True:
            self.screen.fill((0, 0, 0))  # background color

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
                    self.handle_event(event)

            if self.current_page == 'main':
                self.draw_main_menu()
            elif self.current_page == 'select_car':
                self.draw_car_selection()
            elif self.current_page == 'input_location':
                self.draw_location_input()
            elif self.current_page == 'select_car_dropdown':
                self.draw_current_car_selection()
            elif self.current_page == 'game':
                self.run_game()
            elif self.current_page == 'game_over':
                self.draw_game_over()

            pygame.display.flip()

    def draw_main_menu(self):
        self.screen.blit(self.background_image, (0, 0))  # Draw the background image
        title_text = self.title_font.render('Rivian Hill Climber', True, self.font_color)
        self.screen.blit(title_text, (Macros.WINDOW_WIDTH / 2 - title_text.get_width() / 2, Macros.WINDOW_HEIGHT / 4))
        for button in self.buttons:
            button.draw(self.screen)
    
    def goto_car_drop_selection(self):
        self.current_page = 'select_car_dropdown'
        self.buttons = [
            TextButton(Macros.WINDOW_WIDTH / 2 - 100, Macros.WINDOW_HEIGHT / 2 + 100, 300, 50, "Confirm Selection", self.font, self.font_color, action=self.goto_car_selection)
        ]


    def draw_current_car_selection(self):
        self.screen.blit(self.background_image, (0, 0))  # Draw the background image

        # Draw dropdown label
        label = self.font.render("Choose your current vehicle:", True, self.font_color)
        self.screen.blit(label, (Macros.WINDOW_WIDTH / 2 - label.get_width() / 2, Macros.WINDOW_HEIGHT / 2 - 250))

        # Draw dropdown menu
        self.car_input.draw(self.screen)

        # Draw buttons
        for button in self.buttons:
            button.draw(self.screen)

    def goto_car_selection(self):
        self.current_page = 'select_car'
        
        # Load button images
        left_button_image = pygame.image.load('../assets/icons/left.png')
        right_button_image = pygame.image.load('../assets/icons/right.png')
        start_button_image = pygame.image.load('../assets/icons/select_car.png')

        self.buttons = [
            Button(50, Macros.WINDOW_HEIGHT / 2 - 25, 50, 50, left_button_image, action=self.scroll_left),
            Button(Macros.WINDOW_WIDTH - 100, Macros.WINDOW_HEIGHT / 2 - 25, 50, 50, right_button_image, action=self.scroll_right),
            Button(Macros.WINDOW_WIDTH / 2 - 100, Macros.WINDOW_HEIGHT - 200, 200, 200, start_button_image, action=self.goto_location_input)
        ]

    def load_car_images(self):
        # Load and scale images from the assets folder
        assets_folder = os.path.join('../assets', 'cars')
        for img_name in sorted(os.listdir(assets_folder)):
            if img_name.endswith('.webp'):
                img_path = os.path.join(assets_folder, img_name)
                img = pygame.image.load(img_path)
                scaled_img = pygame.transform.scale(img, (int(img.get_width() * 0.35), int(img.get_height() * 0.35)))  # Scale down by 50%
                self.car_images.append(scaled_img)

    def draw_car_selection(self):
        self.screen.blit(self.background_image, (0, 0))  # Draw the background image
        car_space = 100  # Space between cars
        start_x = Macros.WINDOW_WIDTH / 2 - self.car_images[self.selected_car_index].get_width() / 2

        # Draw the selected car image
        img = self.car_images[self.selected_car_index]
        img_rect = img.get_rect(topleft=(start_x, Macros.WINDOW_HEIGHT / 2 - img.get_height() / 2))
        self.screen.blit(img, img_rect)
        pygame.draw.rect(self.screen, (0, 0, 0), img_rect, 3)  # Black rectangle around the selected car

        # Draw buttons
        for button in self.buttons:
            button.draw(self.screen)

    def draw_location_input(self):
        self.screen.blit(self.background_image, (0, 0))  # Draw the background image

        # Add a slight tint
        tint = pygame.Surface((Macros.WINDOW_WIDTH, Macros.WINDOW_HEIGHT))
        tint.set_alpha(128)  # Set transparency level (0-255)
        tint.fill((0, 0, 0))  # Fill with a color (black in this case)
        self.screen.blit(tint, (0, 0))

        self.buttons = [
            TextButton(Macros.WINDOW_WIDTH / 2 - 100, Macros.WINDOW_HEIGHT / 2 + 200, 200, 50, "Start Game", self.font, self.font_color, action=self.start_game)
        ]

        # Draw labels for text input fields
        start_label = self.font.render('Starting point:', True, self.font_color)
        end_label = self.font.render('Ending point:', True, self.font_color)
        self.screen.blit(start_label, (self.start_location_input.rect.x, self.start_location_input.rect.y - 45))
        self.screen.blit(end_label, (self.end_location_input.rect.x, self.end_location_input.rect.y - 45))

        # Draw text input fields
        self.start_location_input.draw(self.screen)
        self.end_location_input.draw(self.screen)

        # Space and draw radio buttons
        detail_label = self.font.render('Select Detail Level:', True, self.font_color)
        self.screen.blit(detail_label, (Macros.WINDOW_WIDTH / 2 - detail_label.get_width() / 2, self.radio_buttons[0].y - 60))
        for i, radio_button in enumerate(self.radio_buttons):
            radio_button.x = Macros.WINDOW_WIDTH / 2 - 150 + i * 200
            radio_button.draw(self.screen)

        # Draw buttons
        for button in self.buttons:
            button.draw(self.screen)

    def scroll_left(self):
        if self.selected_car_index > 0:
            self.selected_car_index -= 1

    def scroll_right(self):
        if self.selected_car_index < len(self.car_images) - 1:
            self.selected_car_index += 1

    def goto_location_input(self):
        self.current_page = 'input_location'

    def start_game(self):
        self.car_selected = self.car_input.text

        co2 = read_and_merge()
        mapping = generate_mapping(co2)
        self.emission_val = calculate_emission(mapping[self.car_selected],2000)

        start_location = self.start_location_input.text
        end_location = self.end_location_input.text
        selected_detail = None
        for radio_button in self.radio_buttons:
            if radio_button.selected:
                selected_detail = radio_button.text
                break
                
        # Get Dropdown list of all cars


        # Placeholder logic to get coordinates, check distance, and get elevation data
        coordinates = get_route(start_location, end_location)
        data = check_distance(coordinates, selected_detail)
        final = get_elevation(data)

        # Extract elevations and other information
        elevations = [entry['elevation'] for entry in final]
        latitudes = [entry['latitude'] for entry in final]
        longitudes = [entry['longitude'] for entry in final]
        distances = [entry['distance'] for entry in final]
        instructions = [entry['instr'] for entry in final]

        # Expand elevations, distances, and instructions
        expanded_elevations = []
        expanded_latitudes = []
        expanded_longitudes = []
        expanded_distances = []
        expanded_instructions = []
        for lat, lon, elevation, distance, instruction in zip(latitudes, longitudes, elevations, distances, instructions):
            repetitions = 15
            expanded_latitudes.extend([lat] * repetitions)
            expanded_longitudes.extend([lon] * repetitions)
            expanded_elevations.extend([elevation] * repetitions)
            expanded_distances.extend([distance] * repetitions)
            expanded_instructions.extend([instruction] * repetitions)

        # Find the maximum value in the expanded elevations
        max_value = max(expanded_elevations)

        # Normalize each element in the expanded elevations
        normalized_elevations = [(elevation / max_value) * 150 for elevation in expanded_elevations]

        # Combine all the data
        final_data = list(zip(expanded_latitudes, expanded_longitudes, expanded_elevations, normalized_elevations, expanded_distances, expanded_instructions))



        # Set up the game
        # self.elevations = normalized_elevations
        # self.elevations = (
        #     [y for x in range(100, -40, -4) for y in (x//4,) * 8] +
        #     [y for x in range(-40, 100, 1) for y in (x//4,) * 2]
        # ) * 50
        
        self.elevations = normalized_elevations
        self.latitude = expanded_latitudes
        self.longitude = expanded_longitudes
        self.instructions = expanded_instructions


        self.car = Car('../assets/cars/R1T_GREY.png', acc=100, maxVelo=100, mileage=300, x=84, y=Macros.WINDOW_HEIGHT / 2, width=2000/15, height=900/15)

        self.platform = Platform(self.screen, self.elevations, 10, 20, instructions=self.instructions)
        self.offset_x = 0
        self.offset_y = 0
        self.change_in_velocity = 0
        self.clock = pygame.time.Clock()

        # Transition to game page
        self.current_page = 'game'

    def run_game(self):
        lat = self.latitude[self.car.x_pos]
        long = self.longitude[self.car.x_pos]
        local_hour = color_util.get_local_military_time(lat, long)
        screen_color = color_util.get_color_for_time(local_hour)

        # print("hit")
        
        while self.current_page == 'game':
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            keys = pygame.key.get_pressed()
            dt = self.clock.get_time() / 100

            self.offset_y = Macros.GRAVITY * (dt**2)

            if (keys[pygame.K_d] or keys[pygame.K_RIGHT]) and self.car.mileage > 0:
                self.change_in_velocity = math.ceil(self.car.acc * dt)
                self.car.mileage -= 1
            elif keys[pygame.K_a] or keys[pygame.K_LEFT]:
                self.change_in_velocity = -((math.ceil(self.car.acc * dt)) * 5)
                self.car.mileage += (.25 if self.offset_x > 3 else 0)
            else:
                self.change_in_velocity = -((math.ceil(self.car.acc * dt)) * .05)
                self.car.mileage += (.05 if self.offset_x > 3 else 0)
            
            # charging
            if (self.car.x_pos % 6000 > 0 and self.car.x_pos % 6000 < 40):
                self.car.mileage += 25

            if self.change_in_velocity != 0:
                tmp = self.car.velocity + self.change_in_velocity
                tmp = 0 if abs(tmp) < 2 else tmp
                if abs(tmp) <= self.car.maxVelo:
                    self.car.velocity = max(0, tmp)

                self.offset_x = math.ceil(self.car.velocity * dt)

                self.offset_x = math.ceil(self.car.velocity * dt)

            if self.offset_x != 0:
                self.platform.car_moved = True
            else:
                self.platform.car_moved = False

            # print("Mileage: ", self.car.mileage)

            # Get the local hour and color for the screen, TODO: log and lat need to be changed based on the current data 


            
            self.screen.fill(screen_color)  # Fill screen with black

            elevation_text = self.font.render(f'Current Elevation: {int(self.elevations[self.car.x_pos])}', True, self.font_color)
            self.screen.blit(elevation_text, (Macros.WINDOW_WIDTH / 2 - elevation_text.get_width() / 2, Macros.WINDOW_HEIGHT / 4))

            mileage_text = self.font.render(f'Mileage: {int(self.car.mileage)}', True, self.font_color)
            self.screen.blit(mileage_text, (Macros.WINDOW_WIDTH / 2 - mileage_text.get_width() / 2, Macros.WINDOW_HEIGHT / 4 + 50))

            try:
                self.platform.scroll(self.offset_x, self.offset_y, self.car.x_pos, self.car.rect)
                self.car.update(self.offset_x, self.platform)
                self.platform.draw(self.car.x_pos)
                self.car.draw(self.screen)
        

                for i in range (len(self.instructions[self.car.x_pos])//80 + 1):
                    instructions_text = self.instr_font.render(f'{self.instructions[self.car.x_pos][i*80:(i+1)*80]}', True, (255, 255, 255))
                    self.screen.blit(instructions_text, (Macros.WINDOW_WIDTH / 2 - instructions_text.get_width() / 2, Macros.WINDOW_HEIGHT / 4 + 400 + i*20))

                pygame.display.flip()
                self.clock.tick(60)
            except Exception as e:
                print("OOPS", e)
                self.current_page = 'game_over'
    
    def draw_game_over(self):
        self.screen.fill((0, 0, 0))  # Fill screen with black
        game_over_text = self.font.render('Drive Over', True, self.font_color)
        self.screen.blit(game_over_text, (Macros.WINDOW_WIDTH / 2 - game_over_text.get_width() / 2, Macros.WINDOW_HEIGHT / 4))
        
        # Example stats
        score_text = self.game_over_font.render(f'Mileage left: {self.car.mileage}', True, self.font_color)
        self.screen.blit(score_text, (Macros.WINDOW_WIDTH / 2 - score_text.get_width() / 2, Macros.WINDOW_HEIGHT / 2 + 100))
        
        # Miles Driven
        # Emission Saved
        
        em_text = f'Congrats on Driving a Rivian! You saved on {self.emission_val/1000} kg CO2 emissions compared to your {self.car_selected}'

        for i in range (len(em_text)//60 + 1):
            score_text = self.game_over_font.render(em_text[i*60:(i+1)*60], True, (255, 255, 255))
            self.screen.blit(score_text, (Macros.WINDOW_WIDTH / 2 - score_text.get_width() / 2, Macros.WINDOW_HEIGHT  / 2 + i*40))


        # retry_button = TextButton(Macros.WINDOW_WIDTH / 2 - 100, Macros.WINDOW_HEIGHT / 2 + 100, 200, 50, 'Retry', self.font, self.font_color, action=self.retry_game)
        # retry_button.draw(self.screen)

    def retry_game(self):
        print("retry please")
        self.current_page = 'main'
        # Reset the game state to start over
        self.elevations = []
        self.car = None
        self.platform = None
        self.offset_x = 0
        self.offset_y = 0
        self.change_in_velocity = 0
        self.clock = pygame.time.Clock()
        self.load_car_images()
        self.buttons = [
            Button(Macros.WINDOW_WIDTH / 2 - 50, Macros.WINDOW_HEIGHT / 2 - 50, 100, 100, pygame.image.load('../assets/icons/play.png'), action=self.goto_car_selection)
        ]

    def handle_event(self, event):
        self.car_input.handle_event(event)
        self.start_location_input.handle_event(event)
        self.end_location_input.handle_event(event)
        for radio_button in self.radio_buttons:
            radio_button.handle_event(event)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                self.handle_click(pygame.mouse.get_pos())

    def handle_click(self, pos):
        for button in self.buttons:
            if button.is_over(pos) and button.action:
                button.action()

if __name__ == "__main__":
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load('../assets/music/speedway-8bit.mp3')

    pygame.mixer.music.play(loops=-1)


    screen = pygame.display.set_mode((Macros.WINDOW_WIDTH, Macros.WINDOW_HEIGHT))
    menu = GameMenu(screen)
    menu.run()
