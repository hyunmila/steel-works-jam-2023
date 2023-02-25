import pygame
from pygame.math import Vector2 as Vec2
from time import perf_counter


class Player:
    def __init__(self, inertia=1.0) -> None:
        self.inertia = inertia 
        self.position = Vec2(0.0, 0.0)
        self.velocity = Vec2(0.0, 0.0)
        self.t_start = perf_counter()
        self.t_stop = perf_counter()
        self.is_jumping = False
        # self.acceleration = Vec2(0.0, -10.0)

    def update(self, pressed_keys, dt):
        y_val = 0.1
        x_val = 0.1
        acceleration = Vec2(0.0, y_val)
        if pressed_keys[pygame.K_d]:
            acceleration.x += x_val
        if pressed_keys[pygame.K_w]:
            if self.is_jumping == False:
                self.t_start = perf_counter()
                self.is_jumping = True
            if self.is_jumping == True:
                self.t_stop = perf_counter()
                if (self.t_stop - self.t_start) <= 1.0:
                    acceleration.y = -y_val
                else:
                    self.is_jumping = False
        else:
            self.is_jumping = False

        if pressed_keys[pygame.K_a]:
            acceleration.x -= x_val
        if pressed_keys[pygame.K_s]:
                acceleration.y += y_val
        f = 0.2 # 0<f<1
        if acceleration.length() > 0:
            self.velocity = self.velocity.lerp(self.velocity + (acceleration * self.inertia * dt), f)
        else:
            self.velocity = self.velocity.lerp(Vec2(0.0, 0.0), f)
        max_speed = 5
        if self.velocity.length() > max_speed:
            self.velocity = self.velocity.normalize()*max_speed

        self.position = self.position.lerp(self.position + (self.velocity * dt), f)

