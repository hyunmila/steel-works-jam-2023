import pygame
from components.npc import NPC
from core.animation import Animation
from components.map import Map, Tile
from item import Item, ItemType
from objective import Objective

class Level:
    pass

SPINACZ_COLOR = (10, 0, 0)
SPINACZ_IMAGE = "res/cyberspinacz.png"

KSERO_COLOR = (20, 0, 0)
KSERO_IMAGE = "res/turbokserokopiarka.png"

EKSPRES_COLOR = (30, 0, 0)
EKSPRES_IMAGE = "res/ultraekspres.png"


COMMON_ITEMS = {
    SPINACZ_COLOR: Tile(
        img_path=SPINACZ_IMAGE,
        collision=False,
        item=Item(
            img=pygame.image.load(SPINACZ_IMAGE),
            name="spinacz",
            item_type=ItemType.GUN,
            shape=(2, 1),
            color=SPINACZ_COLOR,
        ),
    ),
    KSERO_COLOR: Tile(
        img_path=KSERO_IMAGE,
        collision=False,
        item=Item(
            img=pygame.image.load(KSERO_IMAGE),
            name="ksero",
            item_type=ItemType.GUN,
            shape=(3, 3),
            color=KSERO_COLOR,
        ),
    ),
    EKSPRES_COLOR: Tile(
        img_path=EKSPRES_IMAGE,
        collision=False,
        item=Item(
            img=pygame.image.load(EKSPRES_IMAGE),
            name="ekspres",
            item_type=ItemType.GUN,
            shape=(2, 2),
            color=EKSPRES_COLOR,
        ),
    ),
}

COMMON_TILES = {}

class Level1(Level):
    def __init__(self):
        self.map = Map(
            tiles={
                **COMMON_TILES,

            },
            tile_size=64
        )
        map.load_from_file("res/test-map.png")

        self.objective = Objective() # empty objective


class Level2(Level):
    NPC = []

class Level3(Level):
    NPC = []

class Level4(Level):
    NPC = []

class Level5(Level):
    NPC = []

class Level6(Level):
    NPC = []

class Level6(Level):
    NPC = []

class Level7(Level):
    NPC = []

class BossLevel(Level):
    NPC = []

class EndingLevel(Level):
    NPC = []

LEVELS = [
    Level1,
    Level2,
    Level3,
    Level4,
    Level5,
    Level6,
    Level7,
    BossLevel,
    EndingLevel
]