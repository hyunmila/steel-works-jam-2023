from pygame import Vector2
from components.text_box import TextBox
from game import Game
from components.sprite import Sprite
from components.trigger import Trigger
from core.math import BBox
from objective import Objective


class SeventhLevel:
    def open(self, game: Game, prev_level_id: str) -> None:
        self.game = game

        self.game.map.load_from_file("res/level7.png")


        self.game.enemy_manager.add_enemy("warrior", Vector2(5, 9))
        # self.game.enemy_manager.add_enemy("boss", Vector2(5, 9))
        # exit : Vector2(4, 8)
        self.game.player.position = Vector2(0, 8)
        self.game.camera.position = (
            self.game.player.position * self.game.map.get_tile_size()
        )

        self.level_art = Sprite(path="res/level7_resized.png", scale=4)

        self.objective = Objective(
            {"app-le": 1},
            kill_all=False
        )

        self.trigger = Trigger(
            player=self.game.player,
            bbox=BBox(x=4, y=8, w=0.1, h=2),
            on_enter=lambda: self.game.set_level(level_id="lvlboss"),
        )

    def update(self):
        if self.objective.satisfied(self.game.player, self.game.enemy_manager._enemies):
            self.trigger.update(window=self.game.window)

    def draw_bg(self):
        self.level_art.draw(camera=self.game.camera)
