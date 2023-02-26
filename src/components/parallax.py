from typing import Tuple
import pygame
from pygame import Vector2

from core.window import Window
from core.camera import Camera


class Parallax:
    def __init__(
        self,
        path: str,
        height: int,
        offset: Tuple[int, int] = (0, 0),
        movement_scale: Vector2 = Vector2(1, 1),
    ) -> None:
        self.img = pygame.image.load(path)

        scale = height / self.img.get_height()
        self.img = pygame.transform.scale(
            self.img, (int(self.img.get_width() * scale), height)
        )

        self.offset = offset
        self.movement_scale = movement_scale

    def draw(self, camera: Camera) -> None:
        pos = Vector2(camera.position)
        offset = Vector2(pos.x * self.movement_scale.x, pos.y * self.movement_scale.y)
        offset.x = offset.x % self.img.get_width()
        offset.y = offset.y % self.img.get_height()

        camera.blit(self.img, (offset.x, offset.y))
        camera.blit(self.img, (offset.x - self.img.get_width(), offset.y))
        camera.blit(self.img, (offset.x, offset.y - self.img.get_height()))
        camera.blit(
            self.img,
            (offset.x - self.img.get_width(), offset.y - self.img.get_height()),
        )
