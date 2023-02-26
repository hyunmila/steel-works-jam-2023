import pygame

pygame.init()
pygame.mixer.init()

import os
from pygame.math import Vector2 as Vec2
from pygame import Vector2
from core.viewport import Viewport
from core.window import Window
from core.camera import Camera
from core.color import Color
from core.music import Sound
from components.player import Player
from components.text_box import TextBox
from components.map import Map, Tile

from enemy import EnemyMenager

from item import Item, ItemType
from components.weapon import WeaponManager
import enemy, time

from components.bullet import BulletManager
from components.dialog_box import DialogBox
from components.parallax import Parallax

window = Window(title="SteelWorksJam 2023", size=(1280, 720), frame_rate=60)

# input mappings for easier scripting
input = window.get_input()
input.add_action_key(action="crafting", key=pygame.K_p, scale=1)
input.add_action_key(action="right", key=pygame.K_d, scale=1)
input.add_action_key(action="left", key=pygame.K_a, scale=-1)
input.add_action_key(action="right", key=pygame.K_RIGHT, scale=1)
input.add_action_key(action="left", key=pygame.K_LEFT, scale=-1)
input.add_action_key(action="jump", key=pygame.K_SPACE)
input.add_action_key(action="jump", key=pygame.K_w)
input.add_action_key(action="jump", key=pygame.K_UP)
input.add_action_key(action="inventory", key=pygame.K_i)
input.add_action_key(action="fire", key=1)  # left mouse button

viewport = Viewport(window=window, height=720)
camera = Camera(viewport=viewport)

main_song = Sound("res/main.wav", loop=True, volume=0.4)
main_song.play()

beam_sound = Sound("res/beam.mp3")
duct_tape_sound = Sound("res/duct_tape.mp3", volume=0.5)

ui_camera = Camera(viewport=viewport)

turbokserokopiarka = Item(
    name="turbokserokopiarka",
    img=pygame.image.load("res/turbokserokopiarka.png"),
    item_type=ItemType.GUN,
    ammo_type="dupa2",
    weight=10.0,
    shape=(3, 3),
    color=(255, 255, 255),
)

ultraekspres = Item(
    name="ultraekspres",
    img=pygame.image.load("res/ultraekspres.png"),
    item_type=ItemType.GUN,
    ammo_type="dupa2",
    weight=2.0,
    shape=(2, 2),
    color=(255, 0, 255),
)

# game map
map = Map(
    tiles={
        Color.WHITE: Tile("", False),
        Color.BLACK: Tile("res/metalowa-podłoga-2.png", True),
        Color.RED: Tile(
            "res/turbokserokopiarka.png", collision=False, item=turbokserokopiarka
        ),
        Color.GREEN: Tile("res/ultraekspres.png", collision=False, item=ultraekspres),
    },
    tile_size=64,
)
map.load_from_file("res/test-map.png")

dialog_box = DialogBox(typing_delay=0.05)
dialog_box.show(
    [
        "Witaj w NAP Game!",
        "To jest testowy dialog.\nW dwóch liniach! UwU",
        "Zobaczysz go tylko raz!",
    ]
)
# TODO: introduction message for the player

weapon_manager = WeaponManager()
bullet_manager = BulletManager(collision_map=map)
enemy_manager = EnemyMenager(collision_map=map)

# player controller with camera following
player = Player(
    follow_camera=camera,
    collision_map=map,
    weapon_manager=weapon_manager,
    bullet_manager=bullet_manager,
    dialog_box=dialog_box,
)
player.position = Vector2(5, 5)

# UI text
text_box = TextBox(
    font_path="res/uwu-font.ttf",
    font_size=16,
    font_color=Color.WHITE,
    line_height_factor=1.5,
)
text_box.set_text("Get out of here.\nQuickly")
# text_box.offset = (50,0)

# text in 3D space
spatial_text_box = TextBox(
    font_path="res/uwu-font.ttf",
    font_size=32,
    font_color=Color.WHITE,
    line_height_factor=1.5,
)
spatial_text_box.set_text("NAP Game - Not A Platformer Game")
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

# ENEMY testing
# enemy.add_enemy(
#     "warrior", "res/wojownik.png", Vec2(9, 12), 10, Vec2(20, 20), collision_map=map ) 

enemy_manager.add_enemy("warrior", Vec2(9, 12))
enemy_manager.add_enemy("warrior", Vec2(9, 12))
# enemy.add_enemy("warrior", "res/wojownik.png", Vec2(0, 5), 5, Vec2(0.07,0.07))

parallax = Parallax(
    path="res/miasteczko-agh.png", height=720, movement_scale=Vector2(0, 0)
)

# main game loop
while window.is_open():
    window.process_events()

    if input.is_action_just_pressed(action="crafting"):
        print(f"delta = {window.get_delta()}")
        player.weapon.visible = not player.weapon.visible
        duct_tape_sound.play()

    weapon_manager.update(window=window)
    player.update(window=window)
    enemy_manager.update(window, player.position, bullet_manager)
    text_box.offset = (-viewport.get_width() / 5, -viewport.height / 2)
    bullet_manager.update(window=window)
    dialog_box.update(window=window)

    spatial_text_box.draw(camera=camera)
    map.draw(camera=camera)
    # enemy.update_all(player.position, camera, window.get_delta())
    player.draw(camera=camera, ui_camera=ui_camera)
    bullet_manager.draw(camera=camera)
    weapon_manager.draw(camera=ui_camera)
    enemy_manager.draw(camera=camera)
    text_box.draw(camera=ui_camera)
    dialog_box.draw(camera=ui_camera)
    # parallax.draw(camera=camera)

    window.swap_buffers()
