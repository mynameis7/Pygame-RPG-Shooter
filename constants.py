__author__ = 'Andrew'

class COLOR:
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)

FPS = 0
SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 900
DISPLAYSURF = None
DISPLAY_RECT = None

GAME_WIDTH = SCREEN_WIDTH*.8
GAME_HEIGHT = SCREEN_HEIGHT
GAME_RECT = None
GAME_SURF = None

UI_WIDTH = SCREEN_WIDTH*.2
UI_HEIGHT = SCREEN_HEIGHT
UI_RECT = None
UI_SURF = None

ENEMIES = None
EFFECTS = None

KILL_RECT = None

def load_config(filepath):
    with open(filepath) as f:
        for i in f:
            exec(i)