from pygame import Vector2
import pygame
from components.map import Map, Tile
from components.player import Player
from enemy import EnemyManager
from common.item import Item, ItemType
from components.bullet import BulletManager
from components.dialog_box import DialogBox
from components.npc import NPC
from components.parallax import Parallax
from components.weapon import WeaponManager
from core.animation import Animation
from core.camera import Camera
from core.color import Color
from core.viewport import Viewport
from core.window import Window
from levels.npc_preset import get_npc
from levels.item_preset import get_item


class Game:
    def __init__(self, levels, initial_level: str):
        self._init()

        self._levels = levels
        self._current_level = None
        self._current_level_id = ""
        self.set_level(initial_level)

        while self.window.is_open():
            self.window.process_events()

            self._update()
            self._draw()

            self.window.swap_buffers()

        pygame.mixer.stop()
        self._close()

    def _init(self):
        self.window = Window(
            title="SteelWorksJam 2023", size=(1280, 720), frame_rate=60
        )

        self._init_input()

        # viewport that scales when the side that is too long to keep 16x9 ratio is resized
        self.viewport = Viewport(window=self.window, width=1280, height=720)
        self.camera = Camera(viewport=self.viewport)

        # viewport that only scales when window height changes
        self.ui_viewport = Viewport(window=self.window, width=1000000, height=720)
        self.ui_camera = Camera(viewport=self.ui_viewport)

        self.dialog_box = DialogBox(typing_delay=0.1)

        self._init_map()

        self.weapon_manager = WeaponManager()
        self.bullet_manager = BulletManager(collision_map=self.map)
        self.enemy_manager = EnemyManager(collision_map=self.map)

        self.player = Player(
            follow_camera=self.camera,
            collision_map=self.map,
            weapon_manager=self.weapon_manager,
            bullet_manager=self.bullet_manager,
            dialog_box=self.dialog_box,
        )

        self.city_parallax = Parallax(
            path="res/miasteczko-agh.png",
            height=722,
            offset=(0, -361),
            movement_scale=Vector2(0.8, 1),
        )

    def _init_input(self):
        input = self.window.get_input()
        input.add_action_key(action="crafting", key=pygame.K_q, scale=1)
        input.add_action_key(action="interact", key=pygame.K_e, scale=1)
        input.add_action_key(action="right", key=pygame.K_d, scale=1)
        input.add_action_key(action="left", key=pygame.K_a, scale=-1)
        input.add_action_key(action="right", key=pygame.K_RIGHT, scale=1)
        input.add_action_key(action="left", key=pygame.K_LEFT, scale=-1)
        input.add_action_key(action="jump", key=pygame.K_SPACE)
        input.add_action_key(action="jump", key=pygame.K_w)
        input.add_action_key(action="jump", key=pygame.K_UP)
        input.add_action_key(action="inventory", key=pygame.K_q)
        input.add_action_key(action="fire", key=1)  # left mouse button

    def _init_map(self):
        turbokserokopiarka = Item(
            name="turbokserokopiarka",
            img=pygame.image.load("res/turbokserokopiarka.png").convert_alpha(),
            item_type=ItemType.GUN,
            ammo_type="dupa2",
            weight=10.0,
            shape=(3, 3),
            color=(255, 255, 255),
        )

        ultraekspres = Item(
            name="ultraekspres",
            img=pygame.image.load("res/ultraekspres.png").convert_alpha(),
            item_type=ItemType.GUN,
            ammo_type="dupa2",
            weight=2.0,
            shape=(2, 2),
            color=(255, 0, 255),
        )
        self.map = Map(
            tiles={
                Color.WHITE: Tile("", False),
                Color.BLACK: Tile("", True),
                **get_item(),
                **get_npc(self.dialog_box)
                # Color.RED: Tile(
                #     "res/turbokserokopiarka.png",
                #     collision=False,
                #     item=turbokserokopiarka,
                # ),
                # Color.GREEN: Tile(
                #     "res/ultraekspres.png", collision=False, item=ultraekspres
                # ),
                # Color.BLUE: Tile(
                #     "",
                #     collision=False,
                #     interactible=NPC(
                #         dialog_box=self.dialog_box,
                #         animation=Animation(
                #             sheet=pygame.image.load("res/jola.png").convert_alpha(),
                #             cols=4,
                #             frame_rate=5,
                #         ),
                #         text=[
                #             "Lubie\nplacki",
                #             "AAAaaaaAAAaaaaAAAaaaaAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAaA",
                #             "turbosprezarka",
                #         ],
                    # ),
                # ),
            },
            tile_size=64,
        )

    def _update(self):
        if self.window.just_resized():
            print(self.viewport.get_size())

        self.map.update(window=self.window)
        self.enemy_manager.update(
            self.window, self.player.position, self.bullet_manager
        )  # TODO: those extra arguments should be provided during initialization
        self.player.update(window=self.window)
        self.player.combat(self.enemy_manager)
        self.bullet_manager.update(window=self.window)
        self.dialog_box.update(window=self.window)
        self.weapon_manager.update(window=self.window)

        if self._current_level is not None and hasattr(self._current_level, "update"):
            self._current_level.update()

    def _draw(self):
        self.city_parallax.draw(camera=self.camera)

        if self._current_level is not None and hasattr(self._current_level, "draw_bg"):
            self._current_level.draw_bg()

        self.map.draw(camera=self.camera)
        self.enemy_manager.draw(camera=self.camera)
        self.player.draw(camera=self.camera, ui_camera=self.ui_camera)
        self.bullet_manager.draw(camera=self.camera)

        if self._current_level is not None and hasattr(self._current_level, "draw_fg"):
            self._current_level.draw_fg()

        self.dialog_box.draw(camera=self.ui_camera)
        self.weapon_manager.draw(camera=self.ui_camera)

    def _close(self):
        if self._current_level is not None and hasattr(self._current_level, "close"):
            self._current_level.close()

    def set_level(self, level_id: str):
        if self._current_level is not None and hasattr(self._current_level, "close"):
            self._current_level.close()
        self._current_level = self._levels[level_id]()

        if hasattr(self._current_level, "open"):
            self._current_level.open(game=self, prev_level_id=self._current_level_id)

        self._current_level_id = level_id
