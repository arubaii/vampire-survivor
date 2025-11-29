import pygame as pg
import os
from os.path import join


# Global variables
DEBUG = True
FPS = 120
FPS_TOGGLE = True
TILE_SIZE = 64
DISPLAY_WIDTH, DISPLAY_HEIGHT = 1280, 720
BACKGROUND_COLOR = "black"

def initialize():
    pg.init()
    pg.mixer.init()

    os.environ['SDL_VIDEO_WINDOW_POS'] = "1800,200"
    display = pg.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT), flags=pg.SCALED, vsync=1)
    pg.display.set_caption("Vampire Survivor")

    return display