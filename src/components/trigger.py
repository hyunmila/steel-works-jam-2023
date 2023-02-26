import math
from typing import Callable, Optional, Tuple
import pygame
from pygame import Vector2

from core.window import Window
from core.camera import Camera
from core.math import BBox
from components.player import Player


class Trigger:
    def __init__(
        self,
        player: Player,
        bbox: BBox,
        on_enter: Optional[Callable] = None,
        on_leave: Optional[Callable] = None,
    ) -> None:
        self.player = player
        self.bbox = bbox
        self.on_enter = on_enter
        self.on_leave = on_leave
        self._colliding = False

    def update(self, window: Window) -> None:
        bbox2 = self.player.get_bbox()

        # We must multiply by some big number because pygame works with integers.
        r1 = pygame.Rect(
            self.bbox.x * 100, self.bbox.y * 100, self.bbox.w * 100, self.bbox.h * 100
        )
        r2 = pygame.Rect(bbox2.x * 100, bbox2.y * 100, bbox2.w * 100, bbox2.h * 100)

        if r1.colliderect(r2):
            if not self._colliding:
                if self.on_enter is not None:
                    self.on_enter()
                self._colliding = True
        else:
            if self._colliding:
                if self.on_leave is not None:
                    self.on_leave()
                self._colliding = False

    def draw(self, camera: Camera) -> None:
        camera.blit(self._img, self.offset)
