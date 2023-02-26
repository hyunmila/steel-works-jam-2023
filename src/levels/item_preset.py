import pygame
from components.map import Tile
from core.color import Color
from common.item import Item

turboclipper = None
extraphotocopier = None
coffee_supermaker = None
ultracan = None
fastplant = None
hiperlaptop = None
neopen = None
technopapers = None
app_le = None

all_items = None


def get_item():
    global turboclipper, extraphotocopier, coffee_supermaker, ultracan, fastplant, hiperlaptop, neopen, technopapers, app_le, all_items
    if turboclipper is None:
        turboclipper = Item(
            name="turboclipper",
            img=pygame.image.load("res/cyberspinacz.png").convert_alpha(),
            shape=(1, 1),
        )
        extraphotocopier = Item(
            name="extraphotocopier",
            img=pygame.image.load("res/turbokserokopiarka.png").convert_alpha(),
            shape=(3, 3),
        )
        coffee_supermaker = Item(
            name="coffee supermaker",
            img=pygame.image.load("res/ultraekspres.png").convert_alpha(),
            shape=(2, 2),
        )
        ultracan = Item(
            name="ultracan",
            img=pygame.image.load("res/puszka.png").convert_alpha(),
            shape=(1, 1),
        )
        fastplant = Item(
            name="fastplant",
            img=pygame.image.load("res/plant.png").convert_alpha(),
            shape=(2, 2),
        )
        hiperlaptop = Item(
            name="hiperlaptop",
            img=pygame.image.load("res/laptop.png").convert_alpha(),
            shape=(3, 3),
        )
        neopen = Item(
            name="neopen",
            img=pygame.image.load("res/dlugopis.png").convert_alpha(),
            shape=(1, 1),
        )
        technopapers = Item(
            name="technopapers",
            img=pygame.image.load("res/teczkazpapierami.png").convert_alpha(),
            shape=(2, 2),
        )
        app_le = Item(
            name="app-le",
            img=pygame.image.load("res/japko.png").convert_alpha(),
            shape=(2, 2),
        )

        all_items = [
            (turboclipper, "res/cyberspinacz.png"),
            (extraphotocopier, "res/turbokserokopiarka.png"),
            (coffee_supermaker, "res/ultraekspres.png"),
            (ultracan, "res/puszka.png"),
            (fastplant, "res/plant.png"),
            (hiperlaptop, "res/laptop.png"),
            (neopen, "res/dlugopis.png"),
            (technopapers, "res/teczkazpapierami.png"),
            (app_le, "res/japko.png"),
        ]

    items = {}
    for i, (name, path) in enumerate(all_items, start=1):
        items[(i, i, i)] = Tile(path, collision=False, item=name)
    return {**items}
