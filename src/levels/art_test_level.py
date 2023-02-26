from pygame import Vector2
from components.text_box import TextBox
from core.color import Color
from core.music import Sound
from game import Game
from components.sprite import Sprite


class ArtTestLevel:
    def open(self, game: Game) -> None:
        self.game = game

        self.game.map.load_from_file("res/art-test-map.png")
        self.game.player.position = Vector2(5, 5)

        self.level_art = Sprite(path="res/art-test-level.png", scale=4)

        self.spatial_text_box = TextBox(
            font_path="res/uwu-font.ttf",
            font_size=32,
            font_color=Color.WHITE,
            line_height_factor=1.5,
        )
        self.spatial_text_box.set_text("NAP Game - Not A Platformer Game")
        self.spatial_text_box.offset = (100, 400)

    def close(self) -> None:
        self.game.map.clear()
        self.game.player.position = Vector2(0, 0)

    def update(self):
        pass

    def draw_bg(self):
        self.level_art.draw(camera=self.game.camera)

    def draw_fg(self):
        self.spatial_text_box.draw(camera=self.game.camera)
