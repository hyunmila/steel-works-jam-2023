import pygame
from pygame.math import Vector2
from time import perf_counter

import core.math
from core.math import BBox
from core.window import Window
from core.camera import Camera

from components.map import Map

# Player size in pixels
PIXEL_SIZE = 16


class Player:
    def __init__(self, follow_camera: Camera, collision_map: Map) -> None:
        self.follow_camera = follow_camera
        self.collision_map = collision_map

        self.position = Vector2(0.0, 0.0)
        self.velocity = Vector2(0.0, 0.0)

    def update(self, window: Window):
        # Handle input.
        self.velocity.x = (
            window.get_input().get_action_value(action="right", clamp=True) * 10
        )
        if window.get_input().is_action_just_pressed("jump"):
            self.velocity.y = -15

        # Attempt to move horizontally.
        dx = self.velocity.x * window.get_delta()
        self.position[0] += dx
        if self.collision_map.rect_collision(
            bbox=BBox(self.position.x, self.position.y, 1, 1)
        ):
            self.position[0] -= dx
            self.velocity.x = 0

        # Attempt to move vertically.
        dy = self.velocity.y * window.get_delta()
        self.position[1] += dy
        if self.collision_map.rect_collision(
            bbox=BBox(self.position.x, self.position.y, 1, 1)
        ):
            self.position[1] -= dy
            self.velocity.y = 0

        # Apply gravity.
        self.velocity.y += 40.0 * window.get_delta()

        # Make camera follow the player.
        self.follow_camera.position = (
            core.math.lerp(
                self.follow_camera.position[0],
                (self.position[0] + 0.5) * PIXEL_SIZE,
                5.0 * window.get_delta(),
            ),
            core.math.lerp(
                self.follow_camera.position[1],
                (self.position[1] + 0.5) * PIXEL_SIZE,
                5.0 * window.get_delta(),
            ),
        )

    def draw(self, camera: Camera) -> None:
        surface = pygame.Surface((PIXEL_SIZE, PIXEL_SIZE))
        pygame.draw.polygon(
            surface,
            (255, 0, 0),
            (
                (0, 0),
                (PIXEL_SIZE, 0),
                (PIXEL_SIZE, PIXEL_SIZE),
                (0, PIXEL_SIZE),
            ),
        )
        camera.blit(
            surface=surface,
            offset=(
                self.position[0] * PIXEL_SIZE,
                self.position[1] * PIXEL_SIZE,
            ),
        )
