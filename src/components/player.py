import pygame
from pygame.math import Vector2 as Vec2
from time import perf_counter

import core.math
from core.math import BBox
from core.window import Window
from core.camera import Camera

from components.map import Map

PIXEL_SIZE = 16

def bfs():
    pass


def lerp(a, b, t):
    return a + (b-a)*t
class Player:
    def __init__(self, follow_camera: Camera, collision_map: Map) -> None:
        self.inertia = 1.0 
        self.position = Vec2(0.0, 0.0)
        self.velocity = Vec2(0.0, 0.0)
        self.t_start = perf_counter()
        self.t_stop = perf_counter()
        self.is_jumping = False
        self.is_able_to_jump = False

        self.follow_camera = follow_camera
        self.collision_map = collision_map
        # self.acceleration = Vec2(0.0, -10.0)

    def update(self, window: Window):
        y_val = 200
        x_val = 200
        dt = window.get_delta()

        # print(f"self.is_able_to_jump={self.is_able_to_jump}")

        acceleration = Vec2(0.0, y_val)

        if window.get_input().is_action_pressed('right'):
        # if pressed_keys[pygame.K_d]:
            acceleration.x += x_val

        if window.get_input().is_action_pressed('jump'):
        # if pressed_keys[pygame.K_w]:
            if self.is_jumping == False and self.is_able_to_jump == True:
                self.t_start = perf_counter()
                self.is_jumping = True
                self.is_able_to_jump = False
            if self.is_jumping == True:
                self.t_stop = perf_counter()
                if (self.t_stop - self.t_start) <= 1.0:
                    acceleration.y = -y_val
                else:
                    self.is_jumping = False
        else:
            self.is_jumping = False

        if window.get_input().is_action_pressed('left'):
        # if pressed_keys[pygame.K_a]:
            acceleration.x -= x_val

        #print(acceleration)

        
        # if pressed_keys[pygame.K_s]:
        #         acceleration.y += y_val
        f = 0.2 # 0<f<1
        if abs(acceleration.x) > 0:
            self.velocity.x = lerp(self.velocity.x, self.velocity.x + (acceleration.x * self.inertia * dt), f)
        else:
            self.velocity.x = lerp(self.velocity.x, 0.0, f)

        if abs(acceleration.y) > 0:
            self.velocity.y = lerp(self.velocity.y, self.velocity.y + (acceleration.y * self.inertia * dt), f)
        else:
            self.velocity.y = lerp(self.velocity.y, 0.0, f)

        
        max_speed = 60
        if self.velocity.length() > max_speed:
            self.velocity = self.velocity.normalize()*max_speed

        old_position = self.position.copy()
        # self.position = self.position.lerp(self.position + (self.velocity * dt), f)

        # print("PRE", self.velocity, self.position)
        # print("PRE", self.position)

        self.position.y = lerp(self.position.y, self.position.y + (self.velocity.y * dt), f)

        if self.collision_map.rect_collision(
            bbox=BBox(self.position.x, self.position.y, 1, 1)
        ):
            if old_position.y < self.position.y:
                 
                self.is_able_to_jump = True
            else:
                self.is_jumping = False

            self.position.y = old_position.y
            self.velocity.y = 0

        self.position.x = lerp(self.position.x, self.position.x + (self.velocity.x * dt), f)

        if self.collision_map.rect_collision(
            bbox=BBox(self.position.x, self.position.y, 1, 1)
        ):
            # print("x1", self.position.x)
            self.position.x = old_position.x
            # print("x2", self.position.x)
            self.velocity.x = 0

        # print("POST", self.velocity, self.position)


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