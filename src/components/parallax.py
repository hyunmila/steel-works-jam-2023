import math
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
        self._path = path
        self._height = height
        self._cover = None
        self._img_size = (0, 0)
        self.offset = offset
        self.movement_scale = movement_scale

    def draw(self, camera: Camera) -> None:
        if camera.viewport.window.just_resized() or self._cover is None:
            self._render_cover(camera.viewport.get_size())

        pos = Vector2(camera.position)
        offset = Vector2(pos.x * self.movement_scale.x, pos.y * self.movement_scale.y)

        offset.x += self.offset[0]
        offset.y += self.offset[1]

        # Offset cover imag eby multiple of sub-image size to fill the whole viewport.

        dx = offset.x - (camera.position[0] - camera.viewport.get_size()[0] / 2)
        offset.x -= math.ceil(dx / self._img_size[0]) * self._img_size[0]

        dy = offset.y - (camera.position[1] - camera.viewport.get_size()[1] / 2)
        offset.y -= math.ceil(dy / self._img_size[1]) * self._img_size[1]

        camera.blit(self._cover, (offset.x, offset.y))

    def _render_cover(self, viewport_size: Tuple[int, int]) -> None:
        img = pygame.image.load(self._path).convert_alpha()

        scale = self._height / img.get_height()
        img = pygame.transform.scale(img, (int(img.get_width() * scale), self._height))

        img_size = img.get_size()
        self._img_size = img_size

        n_w = int(viewport_size[0] / img_size[0]) + 2
        n_h = int(viewport_size[1] / img_size[1]) + 2

        self._cover = pygame.Surface(
            (img_size[0] * n_w, img_size[1] * n_h), pygame.SRCALPHA, 32
        )

        for x in range(n_w):
            for y in range(n_h):
                self._cover.blit(img, (x * img_size[0], y * img_size[1]))
