import pygame as pg
pg.init()
pg.mixer.init()

clock = pg.time.Clock()

# ------ Кольори ------
YELLOW = (200, 200, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
LIGHT_PURPLE = (200, 160, 255)
DARK_ORANGE = (255, 140, 0)

# ------ Логічни змінні ------
game_part = "menu"
sound_loud = 1.0
FPS = 60
WEIGHT, HEIGHT = 900, 600
SETTINGS_PATH = "data/settings/settings.json"

# ------
