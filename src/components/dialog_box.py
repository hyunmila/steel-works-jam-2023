from typing import List
import pygame
from core.camera import Camera
from core.window import Window
from components.text_box import TextBox
from core.color import Color

BOX_WIDTH = 920


class DialogBox:
    def __init__(self, typing_delay: float = 0.1) -> None:
        self.text_box = TextBox(
            font_path="res/uwu-font.ttf",
            font_size=24,
            font_color=Color.WHITE,
            line_height_factor=1.5,
        )
        self.typing_delay = typing_delay
        self._typing_timer = 0.0
        self._target_text = ""
        self._text = ""
        self._shown = False
        self._empty = True
        self._dialog_queue = []

    def show(self, messages: List[str]) -> None:
        self._dialog_queue = messages

    def is_shown(self) -> bool:
        return self._shown

    def update(self, window: Window) -> None:
        if self._empty:
            if len(self._dialog_queue) > 0:
                self._shown = True
                self._start_writing(self._dialog_queue.pop(0))
            else:
                self._shown = False

        if window.get_input().is_any_key_just_pressed():
            self._empty = True

        if self._text != self._target_text:
            self._typing_timer += window.get_delta()
            if self._typing_timer < self.typing_delay:
                return
            self._typing_timer = 0.0

            self._text += self._target_text[len(self._text)]
            self.text_box.set_text(self._text)

    def draw(self, camera: Camera) -> None:
        if not self._shown:
            return

        # Draw black rectangle with white border
        box_height = self.text_box.get_size()[1] + 50
        surface = pygame.Surface((BOX_WIDTH, box_height))
        pygame.draw.rect(
            surface,
            Color.WHITE,
            rect=(0, 0, BOX_WIDTH, box_height),
        )
        pygame.draw.rect(
            surface,
            Color.BLACK,
            rect=(5, 5, BOX_WIDTH - 10, box_height - 10),
            border_radius=2,
        )

        box_offset = (
            -BOX_WIDTH / 2,
            camera.viewport.height / 2 - box_height,
        )
        camera.blit(surface, box_offset)

        self.text_box.offset = (box_offset[0] + 30, box_offset[1] + 30)
        self.text_box.draw(camera=camera)

    def _start_writing(self, text: str) -> None:
        self._target_text = text
        self._text = ""
        self._typing_timer = 0.0
        self._empty = False
