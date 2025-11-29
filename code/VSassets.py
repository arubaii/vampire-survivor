import pygame as pg
import os
from os.path import join 
from pytmx.util_pygame import load_pygame
from VSsetup import DISPLAY_WIDTH, DISPLAY_HEIGHT

'''All of the asset management is handeled in this file'''

pg.init()
pg.mixer.init()

# Check OS to set base path
if os.name == 'posix':
    BASE_PATH = "/Users/ahmadrubaii/Library/CloudStorage/OneDrive-Personal/main/pyGame/5games-main/vampire-survivor"
elif os.name == 'nt':
    BASE_PATH = r"C:\Users\Ahmad\OneDrive\main\pyGame\5games-main\vampire-survivor"
else:
    BASE_PATH = ""
    print("Unsupported OS")

# Image Assets _______________________________________________________________________________________________________________________________________________________________________________________________________________________
IMAGE_PATHS = {
    "left"      : [join(BASE_PATH, "images", "player", "left", f"{image}.png") for image in range(3)],
    "right"     : [join(BASE_PATH, "images", "player", "right", f"{image}.png") for image in range(3)],
    "up"        : [join(BASE_PATH, "images", "player", "up", f"{image}.png") for image in range(3)],
    "down"      : [join(BASE_PATH, "images", "player", "down", f"{image}.png") for image in range(3)],
    "bat"       : [join(BASE_PATH, "images", "enemies", "bat", f"{image}.png") for image in range(3)],
    "blob"      : [join(BASE_PATH, "images", "enemies", "blob", f"{image}.png") for image in range(3)],
    "skeleton"  : [join(BASE_PATH, "images", "enemies", "skeleton", f"{image}.png") for image in range(3)],
    "map"       : (join(BASE_PATH, 'data', 'maps', 'world.tmx')),
    "gun"       : pg.image.load(join(BASE_PATH, "images", "gun", "gun.png")),
    "bullet"    : pg.image.load(join(BASE_PATH, "images", "gun", "bullet.png")),
}

# Audio Assets ______________________________________________________________________________________________________________________________________________________________________________________________
AUDIO_PATHS = {
    "shoot_sound"   : pg.mixer.Sound(join(BASE_PATH, 'audio', 'shoot.wav')),
    "impact_sound"  : pg.mixer.Sound(join(BASE_PATH, 'audio', 'impact.ogg')),
    "music"         : pg.mixer.Sound(join(BASE_PATH, 'audio', 'music.wav')),   
}


def load_assets(Game):
    # Load player frames
    Game.player_left = [pg.image.load(path).convert_alpha() for path in IMAGE_PATHS["left"]]
    Game.player_right = [pg.image.load(path).convert_alpha() for path in IMAGE_PATHS["right"]]
    Game.player_up = [pg.image.load(path).convert_alpha() for path in IMAGE_PATHS["up"]]
    Game.player_down = [pg.image.load(path).convert_alpha() for path in IMAGE_PATHS["down"]]
    # Load enemies
    Game.bat = [pg.image.load(path).convert_alpha() for path in IMAGE_PATHS["bat"]]
    Game.blob = [pg.image.load(path).convert_alpha() for path in IMAGE_PATHS["blob"]]
    Game.skeleton = [pg.image.load(path).convert_alpha() for path in IMAGE_PATHS["skeleton"]]

    # Load audio
    Game.music = AUDIO_PATHS['music']
    Game.shoot_sound = AUDIO_PATHS['shoot_sound']
    Game.impact_sound = AUDIO_PATHS['impact_sound']

    # Load map 
    Game.map = load_pygame(IMAGE_PATHS["map"])

    # Return player start pos
    return entity(Game)

def entity(Game) -> tuple:
    for entity in Game.map.get_layer_by_name('Entities'):
        # Grabs the starting position of the player entity in the tile map
        if entity.name == 'Player':
            start_pos = (entity.x, entity.y)
        else:
            Game.enemy_spawn_positions.append((entity.x, entity.y))

    return start_pos

