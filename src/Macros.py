from enum import Enum
import math
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
FONT_NAME = "Open Sans"
FONT_SIZE_L = 32
FONT_SIZE_M = 24
FONT_SIZE_S = 16
GRAVITY = 500
TERMINAL_VELOCITY = 20

NUM_PLATFORMS = 8000
class GameMenuCode(Enum):
    MENU_EXIT_OK = 0
    MENU_ERROR = 1

def shadow_scale(time_hr):
    return (10 / (4 * math.sqrt(2*math.pi))) * math.exp((-0.5)* (((time_hr - 12) / 4)**2)) 
