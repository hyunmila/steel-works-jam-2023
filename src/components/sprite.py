import math
from typing import Tuple
import pygame
from pygame import Vector2

from core.window import Window
from core.camera import Camera


class Sprite:
    def __init__(
        self,
        path: str,
        scale: float,
        offset: Tuple[int, int] = (0, 0),
    ) -> None:
        self._img = pygame.image.load(path).convert_alpha()

        self._img = pygame.transform.scale(
            self._img,
            (int(self._img.get_width() * scale), int(self._img.get_height() * scale)),
        )

        self.offset = offset

    def draw(self, camera: Camera) -> None:
        camera.blit(self._img, self.offset)
