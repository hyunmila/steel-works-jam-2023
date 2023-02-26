import math
from typing import Callable, List
from pygame import Vector2
import pygame
from core.camera import Camera
from core.window import Window
from components.map import Map
from core.math import BBox

from core.animation import Animation
from components.explosion import ExplosionManager


pygame.init()

BULLET_SPEED = 5
PIXELS_IN_UNIT = 64
bullet_img = None


class Bullet:
    def __init__(
        self,
        position: Vector2,
        direction: Vector2,
        collision_map: Map,
        on_collision: Callable,
    ):
        global bullet_img
        if bullet_img is None:
            bullet_img = pygame.image.load("res/bullet.png").convert_alpha()
            bullet_img = pygame.transform.scale(bullet_img, (64 * 6, 64))

        self.bullet_anim = Animation(bullet_img, 6, frame_rate=8)

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

        bbox = self.getRect()
        if self.collision_map.rect_collision(bbox):
            self.on_collision()

        self.bullet_anim.update(window=window)

    def draw(self, camera: Camera) -> None:
        img = self.bullet_anim.rasterize()

        angle = -math.atan2(self._direction.y, self._direction.x) * 180 / math.pi - 90
        rotated_img = pygame.transform.rotate(img, angle)

        camera.blit(rotated_img, self.position * PIXELS_IN_UNIT)

    def getRect(self):
        return BBox(self.position.x + 0.3, self.position.y + 0.3, 0.4, 0.4)


class BulletManager:
    def __init__(self, collision_map: Map, explosion_manager: ExplosionManager):
        self._bullets = []
        self.collision_map = collision_map
        self.explosion_manager = explosion_manager

    def get_bullets(self) -> List[Bullet]:
        return self._bullets

    def add_bullet(self, position: Vector2, direction: Vector2) -> None:
        def on_collision():
            self.remove_bullet(bullet)

        bullet = Bullet(position, direction, self.collision_map, on_collision)
        self._bullets.append(bullet)

    def remove_bullet(self, bullet: Bullet) -> None:
        self.explosion_manager.play_explosion(bullet.position)
        self._bullets.remove(bullet)

    def update(self, window: Window) -> None:
        for bullet in self._bullets:
            bullet.update(window)

    def draw(self, camera: Camera) -> None:
        for bullet in self._bullets:
            bullet.draw(camera)
