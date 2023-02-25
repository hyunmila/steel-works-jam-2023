import pygame
from pygame.math import Vector2 as Vec2
from color import Color
from src.components.map import BBox, MapEngine, Tile
from src.components.player import Player
from src.components.text_box import TextBox
from weapon import Weapon
from item import Item, ItemType

pygame.init()

WIDTH, HEIGHT = 1280, 720
CENTER = pygame.math.Vector2(300, 300)
__screen = pygame.display.set_mode([WIDTH, HEIGHT], pygame.RESIZABLE)
screen = __screen.copy()

pygame.display.set_caption("SteelWorksJam 2023")

screen.fill(Color.BLACK)
clock = pygame.time.Clock()

map_engine = MapEngine(
    tiles={
        Color.WHITE: Tile("", False),
        Color.BLACK: Tile("res/metalowa-podłoga-2.png", True),
    },
    tile_size=64,
)

map_engine.load_from_file("res/test-map.png")

player_pos = Vec2(0, 0)
player_speed = Vec2(0, 0)

# mila's player
player = Player()

text_box = TextBox(font_path="res/uwufont.ttf", font_size=16, font_color=Color.BLUE)
text_box.set_text(
    "Jak to jest byc skryba, dobrze?\nTo nie ma tak, ze dobrze czy niedobrze\nGdybym mial powiedziec"
)

# igor's item system
weapon = Weapon()

item = Item(
    name="dupa",
    item_type=ItemType.GUN,
    weight=69.0,
    shape=(2, 3),
    ammo_type="dupa2",
    img=pygame.image.load("res/test.png"),
)

weapon.add_item(item)

while True:
    delta = clock.tick(60) / 1000

    scale_width = __screen.get_width() / screen.get_width()
    scale_height = __screen.get_height() / screen.get_height()
    relative_mouse = Vec2(pygame.mouse.get_pos())
    relative_mouse.x /= scale_width
    relative_mouse.y /= scale_height

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player_speed.y = -15

    pressed_keys = pygame.key.get_pressed()

    pygame.draw.circle(screen, Color.WHITE, Vec2(200, 200), 50)

    if pressed_keys[pygame.K_w]:
        print(f"delta = {delta}")

    # epicki gracz Mili
    player.update(pressed_keys, delta * 1000)

    # Rendering
    # screen.blit(weapon.process(relative_mouse), (0, 0))
    text_box.draw(screen=screen, offset=(100, 100))
    map_engine.draw(screen=screen, offset=(0, 0))
    pygame.draw.polygon(
        screen,
        (255, 0, 0),
        (
            (64 * player_pos[0], 64 * player_pos[1]),
            (64 * (player_pos[0] + 1), 64 * player_pos[1]),
            (64 * (player_pos[0] + 1), 64 * (player_pos[1] + 1)),
            (64 * player_pos[0], 64 * (player_pos[1] + 1)),
        ),
    )

    __scaled = pygame.transform.scale(
        screen, (__screen.get_width(), __screen.get_height())
    )
    __screen.blit(__scaled, (0, 0))
    pygame.display.flip()
