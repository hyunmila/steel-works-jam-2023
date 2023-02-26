import math
from typing import Callable, List
from pygame import Vector2
import pygame
from core.camera import Camera
from core.window import Window
from components.map import Map
from core.math import BBox

from core.animation import Animation


pygame.init()

PIXELS_IN_UNIT = 64
explosion_img = None


class Explosion:
    def __init__(
        self,
        position: Vector2,
    ):
        global explosion_img
        if explosion_img is None:
            explosion_img = pygame.image.load("res/explosion.png").convert_alpha()
            explosion_img = pygame.transform.scale(explosion_img, (128 * 12, 128))

        self.explosion_anim = Animation(explosion_img, 12, frame_rate=24)

        self.position = position.copy()
        self._finished = False

    def is_finished(self) -> bool:
        return self._finished

    def update(self, window: Window) -> None:
        self.explosion_anim.update(window=window)
        if self.explosion_anim.get_frame() == self.explosion_anim.get_frame_count() - 1:
            self._finished = True

    def draw(self, camera: Camera) -> None:
        img = self.explosion_anim.rasterize()
        camera.blit(img, self.position * PIXELS_IN_UNIT)


class ExplosionManager:
    def __init__(self):
        self._explosions = []

    def play_explosion(self, position: Vector2) -> None:
        explosion = Explosion(position)
        self._explosions.append(explosion)

    def update(self, window: Window) -> None:
        for explosion in self._explosions:
            explosion.update(window)

        # Remove finished explosions
        self._explosions = [
            explosion for explosion in self._explosions if not explosion.is_finished()
        ]

    def draw(self, camera: Camera) -> None:
        for explosion in self._explosions:
            explosion.draw(camera)
