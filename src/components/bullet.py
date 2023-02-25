import math
from typing import Callable
from pygame import Vector2
import pygame
from core.camera import Camera
from core.window import Window
from components.map import Map
from core.math import BBox

from core.animation import Animation


BULLET_SPEED = 5
PIXELS_IN_UNIT = 64

BULLET_IMG = pygame.image.load("res/bullet.png")
BULLET_IMG = pygame.transform.scale(BULLET_IMG, (64 * 6, 64))
bullet_anim = Animation(BULLET_IMG, 6, frame_rate=8)


class Bullet:
    def __init__(
        self,
        position: Vector2,
        direction: Vector2,
        collision_map: Map,
        on_collision: Callable,
    ):
        self.position = position.copy()
        self.set_direction(direction)
        self.collision_map = collision_map
        self.on_collision = on_collision

    def set_direction(self, direction: Vector2) -> None:
        self._direction = direction.normalize()

    def get_direction(self) -> Vector2:
        return self._direction

    def update(self, window: Window) -> None:
        self.position += self._direction * BULLET_SPEED * window.get_delta()

        bbox = BBox(self.position.x + 0.3, self.position.y + 0.3, 0.4, 0.4)
        if self.collision_map.rect_collision(bbox):
            self.on_collision()

        bullet_anim.update(window=window)

    def draw(self, camera: Camera) -> None:
        img = bullet_anim.get_frame()

        angle = -math.atan2(self._direction.y, self._direction.x) * 180 / math.pi - 90
        rotated_img = pygame.transform.rotate(img, angle)

        camera.blit(rotated_img, self.position * PIXELS_IN_UNIT)


class BulletManager:
    def __init__(self, collision_map: Map):
        self._bullets = []
        self.collision_map = collision_map

    def get_bullets(self) -> list[Bullet]:
        return self._bullets

    def add_bullet(self, position: Vector2, direction: Vector2) -> None:
        def on_collision():
            self._bullets.remove(bullet)

        bullet = Bullet(position, direction, self.collision_map, on_collision)
        self._bullets.append(bullet)

    def remove_bullet(self, bullet: Bullet) -> None:
        self._bullets.remove(bullet)

    def update(self, window: Window) -> None:
        for bullet in self._bullets:
            bullet.update(window)

    def draw(self, camera: Camera) -> None:
        for bullet in self._bullets:
            bullet.draw(camera)
