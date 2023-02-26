from pygame import Vector2
from components.text_box import TextBox
from game import Game
from components.sprite import Sprite
from components.trigger import Trigger
from core.math import BBox


class NextTestLevel:
    def open(self, game: Game, prev_level_id: str) -> None:
        self.game = game

        self.game.map.load_from_file("res/next-test-level-map.png")

        if prev_level_id == "art-test-level":
            self.game.player.position = Vector2(0, 10.9)
        else:
            self.game.player.position = Vector2(5, 8)
        self.game.camera.position = (
            self.game.player.position * self.game.map.get_tile_size()
        )

        self.level_art = Sprite(path="res/next-test-level-art.png", scale=4)

        self.trigger = Trigger(
            player=self.game.player,
            bbox=BBox(x=0, y=10, w=0.1, h=2),
            on_enter=lambda: self.game.set_level(level_id="art-test-level"),
        )

    def update(self):
        self.trigger.update(window=self.game.window)

    def draw_bg(self):
        self.level_art.draw(camera=self.game.camera)
