from pygame import Vector2
from components.text_box import TextBox
from core.color import Color
from core.music import Sound
from game import Game
from components.sprite import Sprite
from components.trigger import Trigger
from core.math import BBox
from levels.test_level import TestLevel
from levels.next_test_level import NextTestLevel


class ArtTestLevel:
    def open(self, game: Game, prev_level_id: str) -> None:
        self.game = game

        self.game.map.load_from_file("res/art-test-level-map.png")

        if prev_level_id == "next-test-level":
            # self.game.enemy_manager.add_enemy("sorcerer", Vector2(15, 6.9))
            self.game.player.position = Vector2(19, 6.9)
        else:
            self.game.player.position = Vector2(10, 6.9)

            self.game.dialog_box.show(
                [
                    "Howdy! This is the new test level.",
                    "Go to the left to find\nthe old test level.\nThere's no way back from there.",
                    "Also,",
                    "Collision tiles are\ninvisible for now.",
                    "Anyways,\nGo to the right to\nvisit the next level.",
                    "123456789012345678901234567890123456\n123456789012345678901234567890123456"
                ]
            )
        self.game.camera.position = (
            self.game.player.position * self.game.map.get_tile_size()
        )

        self.level_art = Sprite(path="res/art-test-level-art.png", scale=4)
        self.level_shading = Sprite(path="res/art-test-level-shading.png", scale=4)

        self.spatial_text_box = TextBox(
            font_path="res/uwu-font.ttf",
            font_size=32,
            font_color=Color.WHITE,
            line_height_factor=1.5,
        )
        self.spatial_text_box.set_text("Art Test Level")
        self.spatial_text_box.offset = (
            (
                self.game.map.get_map_size()[0] * self.game.map.get_tile_size()
                - self.spatial_text_box.get_size()[0]
            )
            / 2,
            600,
        )

        self.trigger = Trigger(
            player=self.game.player,
            bbox=BBox(x=0, y=5, w=0.1, h=3),
            on_enter=lambda: self.game.set_level("test-level"),
        )

        self.trigger2 = Trigger(
            player=self.game.player,
            bbox=BBox(x=19.9, y=5, w=0.1, h=3),
            on_enter=lambda: self.game.set_level("next-test-level"),
        )

    def update(self):
        self.trigger.update(window=self.game.window)
        self.trigger2.update(window=self.game.window)

    def draw_bg(self):
        self.level_art.draw(camera=self.game.camera)

    def draw_fg(self):
        self.level_shading.draw(camera=self.game.camera)
        self.spatial_text_box.draw(camera=self.game.camera)
