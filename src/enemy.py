import pygame
import random
from math import sqrt
from pygame.math import Vector2 as Vec2
from core.color import Color
import abc
from core.camera import Camera
from components.map import Map
from core.math import BBox, lerp
from typing import List


class Box:
    def __init__(self, pos, size):
        self.pos = pos
        self.size = size
        self.velocity = Vec2(0.0, 0.0)

    def get_points(self):
        l = Vec2(0, self.size.y / 2)
        t = Vec2(self.size.x / 2, 0)

        return (
            ((self.pos + l + t).x, (self.pos + l + t).y),
            ((self.pos + l - t).x, (self.pos + l - t).y),
            ((self.pos - l - t).x, (self.pos - l - t).y),
            ((self.pos - l + t).x, (self.pos - l + t).y),
        )

    # def move(self, dt):
    #     self.pos += self.velocity * dt


PIXEL_SIZE = 64


class Enemy(metaclass=abc.ABCMeta):
    def __init__(self, path, pos: Vec2, dist, vel: Vec2, collision_map: Map):
        self.image = pygame.image.load(path)
        self.image = pygame.transform.scale(self.image, (PIXEL_SIZE, PIXEL_SIZE))
        # self.rect = self.image.get_rect(center=(pos[0] * PIXEL_SIZE, pos[1] * PIXEL_SIZE))
        self.rect = pos
        self.gravity = 0
        self.vel = vel
        self.dist = dist
        self.collision_map = collision_map
        self.health = 3
        self.ticks = 0

    # when player is too close to enemy, then enemy is starting chaise him
    def activate(self, pos):
        return Vec2(pos.x - self.rect.x, pos.y - self.rect.y).length()

    # to update all status about enemy
    def update(self, player_pos, camera: Camera, dt):
        pass

    def range_attack(self):
        pass

    # @abc.abstractmethod
    # def chase(self, pos):
    #     pass

    # @abc.abstractmethod
    # def ability(self, cooldown):
    #     pass

    def draw(self, camera: Camera, surface, pos):
        camera.blit(surface, pos)

    def getRect(self) -> pygame.Rect:
        return self.rect

    def setPosX(self, pos):
        self.rect.x += pos

    def setPosY(self, pos):
        self.rect.y += pos


class Warrior(Enemy):
    def __init__(self, path, pos, dist, vel, collision_map):
        super().__init__(path, pos, dist, vel, collision_map)
        self.strong_attack = False
        # self.cooldown = cooldown

    def update(self, player_pos, camera: Camera, dt):
        f = 0.2
        old_vel = self.vel
        old_position = self.rect.copy()
        # self.position = self.position.lerp(self.position + (self.velocity * dt), f)

        # print("PRE", self.velocity, self.position)
        # print("PRE", self.position)

        if 0.7 < self.activate(player_pos) < self.dist:
            if self.rect.y < player_pos.y:
                self.rect.y = lerp(self.rect.y, self.rect.y + (self.vel.y * dt), f)
            else:
                self.rect.y = lerp(self.rect.y, self.rect.y + (-self.vel.y * dt), f)

            if self.collision_map.rect_collision(
                bbox=BBox(self.rect.x, self.rect.y, 1, 1)
            ):
                if old_position.y < self.rect.y:
                    self.is_able_to_jump = True
                else:
                    self.is_jumping = False

                self.rect.y = old_position.y

            if self.rect.x < player_pos.x:
                self.rect.x = lerp(self.rect.x, self.rect.x + (self.vel.x * dt), f)
            else:
                self.rect.x = lerp(self.rect.x, self.rect.x + (-self.vel.x * dt), f)

            if self.collision_map.rect_collision(
                bbox=BBox(self.rect.x, self.rect.y, 1, 1)
            ):
                self.rect.x = old_position.x

        # self.ability(5)
        self.draw(
            camera, self.image, (self.rect.x * PIXEL_SIZE, self.rect.y * PIXEL_SIZE)
        )
        self.vel = old_vel

    # def ability(self, cooldown):  # super attack
    #     return cooldown - time.time()


class Bullet:
    def __init__(self, position: Vec2, vel: Vec2, direction: Vec2, collision_map: Map):
        self.vel = vel
        self.position = position
        self.direction = direction  # Vector2 like [0,-1] - normalized
        self.collision_map = collision_map
        self.rect = pygame.Rect(position.x * PIXEL_SIZE, position.y * PIXEL_SIZE, 3, 7)

    def draw(self):
        pass

    # def update(self, camera):
    #     if not self.collision_map.rect_collision(
    #         bbox=BBox(self.rect.x / PIXEL_SIZE, self.rect.y / PIXEL_SIZE, 3 / PIXEL_SIZE, 7 / PIXEL_SIZE)
    #         ):
    #         if bullet.x < 0:
    #             bullet.x = lerp(bullet.x, bullet.x + (-self.bullet_vel.x * dt), f)
    #         else:
    #             bullet.x = lerp(bullet.x, bullet.x + (self.bullet_vel.x * dt), f)

    #         if bullet.y < 0:
    #             bullet.y = lerp(bullet.y, bullet.y + (-self.bullet_vel.y * dt), f)
    #         else:
    #             bullet.y = lerp(bullet.y, bullet.y + (self.bullet_vel.y * dt), f)
    #         self.draw(camera ,self.image, bullet[1])
    #         new_bullets.append(bullet)

    #     self.bullets = new_bullets
    #     self.draw(camera, self.image, (self.rect.x * PIXEL_SIZE, self.rect.y * PIXEL_SIZE))


class Sorcerer(Enemy):
    def __init__(self, path, pos, dist, vel, collision_map):
        super().__init__(path, pos, dist, vel, collision_map)
        self.bullet_vel = Vec2(30, 30)
        self.bullets = []

    def shoot(self, player_pos):
        if self.shoots(player_pos):
            bullet = pygame.Rect(
                self.rect.x * PIXEL_SIZE, self.rect.y * PIXEL_SIZE, 10, 5
            )
            # self.bullets.append((bullet, Vec2(player_pos.x - self.rect.x, player_pos.y - self.rect.y))) # (bullet, direction_of_bullet - Vec2 normalized)
            self.bullets.append(
                bullet
            )  # (bullet, direction_of_bullet - Vec2 normalized)

    def update(self, player_pos, camera: Camera, dt):
        self.ticks += dt
        if self.ticks > 2:
            self.shoot(player_pos)
            self.ticks = 0
        f = 0.2

        old_vel = self.vel
        old_position = self.rect.copy()
        # self.position = self.position.lerp(self.position + (self.velocity * dt), f)

        # print("PRE", self.velocity, self.position)
        # print("PRE", self.position)

        if 3 < self.activate(player_pos) < self.dist:
            if self.rect.y < player_pos.y:
                self.rect.y = lerp(self.rect.y, self.rect.y + (self.vel.y * dt), f)
            else:
                self.rect.y = lerp(self.rect.y, self.rect.y + (-self.vel.y * dt), f)

            if self.collision_map.rect_collision(
                bbox=BBox(self.rect.x, self.rect.y, 1, 1)
            ):
                if old_position.y < self.rect.y:
                    self.is_able_to_jump = True
                else:
                    self.is_jumping = False

                self.rect.y = old_position.y

            if self.rect.x < player_pos.x:
                self.rect.x = lerp(self.rect.x, self.rect.x + (self.vel.x * dt), f)
            else:
                self.rect.x = lerp(self.rect.x, self.rect.x + (-self.vel.x * dt), f)

            if self.collision_map.rect_collision(
                bbox=BBox(self.rect.x, self.rect.y, 1, 1)
            ):
                self.rect.x = old_position.x

        new_bullets = []

        # update all bullets
        # for bullet in self.bullets:
        #     if not self.collision_map.rect_collision(
        #         bbox=BBox(bullet.x / PIXEL_SIZE, bullet.y / PIXEL_SIZE, 10 / PIXEL_SIZE, 5 / PIXEL_SIZE)
        #         ):
        #         if bullet.x < 0:
        #             bullet.x = lerp(bullet.x, bullet.x + (-self.bullet_vel.x * dt), f)
        #         else:
        #             bullet.x = lerp(bullet.x, bullet.x + (self.bullet_vel.x * dt), f)

        #         if bullet.y < 0:
        #             bullet.y = lerp(bullet.y, bullet.y + (-self.bullet_vel.y * dt), f)
        #         else:
        #             bullet.y = lerp(bullet.y, bullet.y + (self.bullet_vel.y * dt), f)
        #         self.draw(camera ,self.image, bullet[1])
        #         new_bullets.append(bullet)

        # self.bullets = new_bullets

        # ______________________________________________________

        # self.ability(5)
        self.draw(
            camera, self.image, (self.rect.x * PIXEL_SIZE, self.rect.y * PIXEL_SIZE)
        )
        self.vel = old_vel

    def shoots(self, player_pos):
        if self.activate(player_pos) < self.dist - 1:
            return True
        return False


enemies = []
bullets = []
dt = 0
enum = {"warrior": Warrior, "sorcerer": Sorcerer}
VEL = 5  # global velocity


def enemy_collision(enemies: List[Enemy]):
    n = len(enemies)
    dt = 10
    for _ in range(3):
        random.shuffle(enemies)
        for i in range(n - 1):
            for j in range(i + 1, n):
                # box1 = Box(
                #     Vec2(enemies[i].getRect().topright),
                #     Vec2(enemies[i].getRect().width, enemies[i].getRect().height),
                # )  # Rect()
                # box2 = Box(
                #     Vec2(enemies[j].getRect().topright),
                #     Vec2(enemies[j].getRect().width, enemies[j].getRect().height),
                # )  # Rect()

                box1 = Box(enemies[i].rect * PIXEL_SIZE, Vec2(PIXEL_SIZE, PIXEL_SIZE))
                box2 = Box(enemies[j].rect * PIXEL_SIZE, Vec2(PIXEL_SIZE, PIXEL_SIZE))

                # rect1 = enemies[i].getRect()
                # rect2 = enemies[j].getRect()

                l1 = box1.pos - box1.size / 2
                r1 = box1.pos + box1.size / 2
                l2 = box2.pos - box2.size / 2
                r2 = box2.pos + box2.size / 2

                x = min(r1.x, r2.x) - max(l1.x, l2.x)
                y = min(r1.y, r2.y) - max(l1.y, l2.y)

                if x <= 0 or y <= 0:
                    continue

                # vec1 = Vec2(
                #     (rect1.topleft[0] - rect1.center[0]) * 2,
                #     (rect1.topleft[1] - rect1.center[1]) * 2,
                # ).length()  # ????

                # vec = Vec2(
                #     rect1.center[0] - rect2.center[0], rect1.center[1] - rect2.center[1]
                # )
                # vec_len = vec.length()

                # if vec_len > 100:
                #     continue

                if x < y:
                    if box1.pos.x > box2.pos.x:
                        x *= -1
                    # rect1.pos.x -= x
                    enemies[i].setPosX(-x)
                    # rect2.pos.x += x
                    enemies[j].setPosX(x)

                else:
                    if box1.pos.y > box2.pos.y:
                        y *= -1
                    # rect1.pos.y -= y
                    enemies[i].setPosY(-y)
                    # rect2.pos.y += y
                    enemies[j].setPosY(y)

                # if x < y:
                #     if box1.pos.x > box2.pos.x: x *= -1
                #     box1.pos.x -= x
                #     box2.pos.x += x
                # else:
                #     if box1.pos.y > box2.pos.y: y *= -1
                #     box1.pos.y -= y
                #     box2.pos.y += y

                enemies[j].setPosX(random.random())
                enemies[j].setPosY(random.random())

                # enemies[i].setPosX(random.random())
                # enemies[i].setPosY(random.random())


def add_enemy(type_of_enemy, path, position, distance, vel_of_chase, collision_map):
    if type_of_enemy == "warrior":
        enemies.append(
            enum["warrior"](path, position, distance, vel_of_chase, collision_map)
        )

    if type_of_enemy == "sorcerer":
        enemies.append(
            enum["sorcerer"](path, position, distance, vel_of_chase, collision_map)
        )


def update_all(player_pos, camera, timer):
    # handle collisions of bullets

    for enemy in enemies:
        enemy.update(player_pos, camera, timer)

    # enemy_collision(enemies)


if __name__ == "__main__":
    pass
