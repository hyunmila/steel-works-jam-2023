from pygame import Vector2
from components.text_box import TextBox
from core.color import Color
from core.music import Sound
from game import Game


class TestLevel:
    def open(self, game: Game) -> None:
        self.game = game

        self.game.map.load_from_file("res/test-map.png")
        self.game.player.position = Vector2(5, 5)
        self.game.enemy_manager.add_enemy("warrior", Vector2(9, 12))
        self.game.enemy_manager.add_enemy("warrior", Vector2(9, 12))

        self.spatial_text_box = TextBox(
            font_path="res/uwu-font.ttf",
            font_size=32,
            font_color=Color.WHITE,
            line_height_factor=1.5,
        )
        self.spatial_text_box.set_text("NAP Game - Not A Platformer Game")
        self.spatial_text_box.offset = (100, 100)

        self.main_song = Sound("res/main.wav", loop=True, volume=0.4)
        self.main_song.play()

    def close(self) -> None:
        self.game.map.clear()
        self.game.player.position = Vector2(0, 0)
        self.game.enemy_manager.clear()
        self.main_song.stop()

    def update(self):
        pass

    def draw_fg(self):
        self.spatial_text_box.draw(camera=self.game.camera)
