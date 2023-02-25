import pygame
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
input.add_action_key(action="right", key=pygame.K_a, scale=-1)
input.add_action_key(action="right", key=pygame.K_RIGHT, scale=1)
input.add_action_key(action="right", key=pygame.K_LEFT, scale=-1)
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

# game map
map = Map(
    tiles={
        Color.WHITE: Tile("", False),
        Color.BLACK: Tile("res/metalowa-podłoga-2.png", True),
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

# text in 3D space
spatial_text_box = TextBox(
    font_path="res/uwu-font.ttf",
    font_size=8,
    font_color=Color.WHITE,
    line_height_factor=1.5,
)
spatial_text_box.set_text("tekst w przestrzeni")
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
# )

# weapon.add_item(item)


# main game loop
while window.is_open():
    window.process_events()

    if input.is_action_just_pressed(action="debug-delta"):
        print(f"delta = {window.get_delta()}")

    player.update(window=window)
    text_box.offset = (-ui_viewport.get_width() / 2, -ui_viewport.height / 2)

    spatial_text_box.draw(camera=camera)
    map.draw(camera=camera)
    player.draw(camera=camera)
    text_box.draw(camera=ui_camera)

    # ui_camera.blit(
    #     weapon.process(Vector2(input.get_mouse_pos())),
    #     (-ui_viewport.get_width() / 2, -ui_viewport.height / 2),
    # )

    window.swap_buffers()
