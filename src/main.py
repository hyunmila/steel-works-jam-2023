import pygame
import os
from pygame import Vector2
from core.viewport import Viewport
from core.window import Window
from core.camera import Camera
from core.color import Color
from components.player import Player
from components.text_box import TextBox
from components.map import Map, Tile

from item import Item, ItemType
from weapon import Weapon

window = Window(title="SteelWorksJam 2023", size=(1280, 720), frame_rate=60)

# input mappings for easier scripting
input = window.get_input()
input.add_action_key(action="debug-delta", key=pygame.K_p)
input.add_action_key(action="right", key=pygame.K_d, scale=1)
input.add_action_key(action="left", key=pygame.K_a, scale=-1)
input.add_action_key(action="right", key=pygame.K_RIGHT, scale=1)
input.add_action_key(action="left", key=pygame.K_LEFT, scale=-1)
input.add_action_key(action="jump", key=pygame.K_SPACE)
input.add_action_key(action="jump", key=pygame.K_w)
input.add_action_key(action="jump", key=pygame.K_UP)

# main low-resolution viewport for the game world
viewport = Viewport(window=window, height=180)
camera = Camera(viewport=viewport)
# TODO: Up-scaling from lower resolution is not an optimal idea.
# For optimal quality, we should always draw at native resolution.
# Example drawback: gaps between tiles.

# higher resolution UI viewport for the UI elements
ui_viewport = Viewport(window=window, height=360)
ui_camera = Camera(viewport=ui_viewport)

# Weapon menu viewport
weapon_viewport = Viewport(window=window, height=720)
weapon_camera = Camera(viewport=weapon_viewport)


turbokserokopiarka = Item(
    name="turbokserokopiarka",
    img = pygame.image.load("res/turbokserokopiarka.png"),
    item_type = ItemType.GUN,
    ammo_type="dupa2",
    weight=10.0,
    shape=(3, 3),
    color=(255, 255, 255)
)

ultraekspres = Item(
    name="ultraekspres",
    img = pygame.image.load("res/ultraekspres.png"),
    item_type = ItemType.GUN,
    ammo_type="dupa2",
    weight=2.0,
    shape=(2, 2),
    color=(255, 0, 255)
)

# game map
map = Map(
    tiles={
        Color.WHITE: Tile("", False),
        Color.BLACK: Tile("res/metalowa-podłoga-2.png", True),
        Color.RED: Tile("res/turbokserokopiarka.png", collision=False, item=turbokserokopiarka),
        Color.GREEN: Tile("res/ultraekspres.png", collision=False, item=ultraekspres), 
    },
    tile_size=16,
)
map.load_from_file("res/test-map.png")

# player controller with camera following
player = Player(follow_camera=camera, collision_map=map)
player.position = Vector2(5, 5)

# UI text
text_box = TextBox(
    font_path="res/uwu-font.ttf",
    font_size=8,
    font_color=Color.WHITE,
    line_height_factor=1.5,
)
text_box.set_text(
    "Jak to jest byc skryba, dobrze?\nTo nie ma tak, ze dobrze czy niedobrze\nGdybym mial powiedziec"
)
# text_box.offset = (50,0)

# text in 3D space
spatial_text_box = TextBox(
    font_path="res/uwu-font.ttf",
    font_size=8,
    font_color=Color.WHITE,
    line_height_factor=1.5,
)
spatial_text_box.set_text("NAP Game- Not A Platformer Game")
spatial_text_box.offset = (100, 100)



# # TESTING: igor's item system
# weapon = Weapon()

# item = Item(
#     name="dupa",
#     item_type=ItemType.GUN,
#     weight=69.0,
#     shape=(2, 3),
#     ammo_type="dupa2",
#     img=pygame.image.load("res/test.png"),
#     color=Color.RED
# )

# item2 = Item(
#     name='dupa2',
#     item_type=ItemType.AMMO,
#     weight=42.0,
#     shape=(4,1),
#     ammo_type="",
#     img=pygame.image.load("res/jola.png"),
#     color=Color.GREEN
# )

# item3 = Item(
#     name='dupa3',
#     item_type=ItemType.CONNECT,
#     weight=45.0,
#     shape=(2,1),
#     ammo_type="",
#     img=pygame.image.load("res/wojownik-atakuje.png"),
#     color=Color.BLUE
# )

# weapon.add_item(item)

# for _ in range(2):
#     weapon.add_item(item2)
# for _ in range(4):
#     weapon.add_item(item3)

flag = False

# main game loop
while window.is_open():
    window.process_events()
    # print(os.environ.get('NAP_GAME_MODE_SELECT_69'))
    if input.is_action_just_pressed(action="debug-delta"):
        print(f"delta = {window.get_delta()}")

    player.update(window=window)
    text_box.offset = (-ui_viewport.get_width() / 5, -ui_viewport.height / 2)
    # text_box.offset = (0,0)
    spatial_text_box.draw(camera=camera)
    map.draw(camera=camera)
    player.draw(camera=camera, uicamera=ui_camera)
    text_box.draw(camera=ui_camera)

    if input.is_action_just_pressed(action="debug-delta"):
        flag = not flag

    if flag:
        weapon_camera.blit(
            player.weapon.process(Vector2(input.get_mouse_pos())),
            (-weapon_viewport.get_width() / 2, -weapon_viewport.height / 2),
        )

    window.swap_buffers()
