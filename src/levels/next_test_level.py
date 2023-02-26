from pygame import Vector2
from components.text_box import TextBox
from game import Game
from components.sprite import Sprite
from components.trigger import Trigger
from core.math import BBox


class NextTestLevel:
    def open(self, game: Game, prev_level_id: str) -> None:
        self.game = game

        self.game.map.load_from_file("res/boss.png")
        # self.game.map.load_from_file("res/art-test-level-map.png")
        # self.game.map.load_from_file("res/next-test-level-map.png.png")
        # self.game.map.load_from_file("res/level3.png")
        # self.game.map.load_from_file("res/level7.png")
        # self.game.map.load_from_file("res/boss.png")


        self.game.enemy_manager.add_enemy("warrior", Vector2(5, 9))
        # self.game.enemy_manager.add_enemy("boss", Vector2(5, 9))
        # lvl 1 : Vector2(1, 8)
        # lvl 2 : Vector2(2, 11)
        # lvl 3 : Vector2(7, 37)
        # lvl 4 : 
        # lvl 7 : Vector2(0, 8)
        # boss : Vector2(0, 8)
        self.game.player.position = Vector2(0, 8)
        self.game.camera.position = (
            self.game.player.position * self.game.map.get_tile_size()
        )

        self.level_art = Sprite(path="res/boss_resized.png", scale=4)
        # self.level_art = Sprite(path="res/art-test-level-art.png", scale=4)
        # self.level_art = Sprite(path="res/next-test-level-art.png", scale=4)
        # self.level_art = Sprite(path="res/level3_resized.png", scale=4)
        # self.level_art = Sprite(path="res/level7_resized.png", scale=4)
        # self.level_art = Sprite(path="res/boss_resized.png", scale=4)



        self.trigger = Trigger(
            player=self.game.player,
            bbox=BBox(x=0, y=10, w=0.1, h=2),
            on_enter=lambda: self.game.set_level(level_id="art-test-level"),
        )

    def update(self):
        pass
        # self.trigger.update(window=self.game.window)

    def draw_bg(self):
        self.level_art.draw(camera=self.game.camera)
