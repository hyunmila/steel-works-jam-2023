import pygame
import random
from math import sqrt
from pygame.math import Vector2 as Vec2
from core.color import Color
import abc
from core.camera import Camera
from core.window import Window
from components.map import Map
from core.math import BBox, lerp
from typing import List
from time import perf_counter
from core.animation import Animation
from components.bullet import BulletManager, Bullet


class Box:
    def __init__(self, pos, size):
        self.pos = pos
        self.size = size
        self.vel = Vec2(0.0, 0.0)

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
    #     self.pos += self.vel * dt


PIXEL_SIZE = 64
DAMGE = 1
# kolizje sprawdzamy w Enemy


class Enemy(metaclass=abc.ABCMeta):
    def __init__(self, pos: Vec2, collision_map: Map):
        self.rect = pos
        self.vel = Vec2(0.0, 0.0)
        self.dist = 5
        self.collision_map = collision_map
        self.health = 3
        self.ticks = 0
        self.is_jumping = False
        self.is_able_to_jump = False
        self.t_start = perf_counter()
        self.t_stop = perf_counter()
        self.inertia = 1

    def activate(self, pos):
        return Vec2(pos.x - self.rect.x, pos.y - self.rect.y).length()

    def air_check(self, pos, vec: Vec2):  # true if there is no colision
        return not self.collision_map.get_tile(
            int(pos.x + vec.x), int(pos.y + vec.y)
        ).collision

    def move(self, player_pos, dt):
        old_position = self.rect.copy()

        x_val = 2000
        y_val = 2000
        fy = 0.7

        acceleration = Vec2(0.0, y_val)
        # ------------------------------------------------------------

        if player_pos.x > self.rect.x:  # warunek chodzenia w prawo
            acceleration.x += x_val
        if player_pos.x < self.rect.x:  # warunek dla chodzenia w lewo
            acceleration.x -= x_val

        if player_pos.y < self.rect.y:  # warunek skoku
            if self.is_jumping == False and self.is_able_to_jump == True:
                self.t_start = perf_counter()
                self.is_jumping = True
                self.is_able_to_jump = False
            if self.is_jumping == True:
                self.t_stop = perf_counter()
                if (self.t_stop - self.t_start) <= 0.65:
                    acceleration.y = -y_val * 2
                else:
                    self.is_jumping = False
        else:
            self.is_jumping = False

        # print(acceleration)
        if self.is_jumping == False and self.is_able_to_jump == False:
            acceleration.y += 1.50 * y_val

        fx = 0.70  # 0<f<1
        fy = 0.70  # 0<f<1
        if abs(acceleration.x) > 0:
            self.vel.x = lerp(
                self.vel.x,
                self.vel.x + (acceleration.x * self.inertia * dt),
                fx,
            )
        else:
            self.vel.x = lerp(self.vel.x, 0.0, fx)

        if abs(acceleration.y) > 0:
            self.vel.y = lerp(
                self.vel.y,
                self.vel.y + (acceleration.y * self.inertia * dt),
                fy,
            )
        else:
            self.vel.y = lerp(self.vel.y, 0.0, fy)

        if self.vel.x > 0:
            self.facing = "right"
        elif self.vel.x < 0:
            self.facing = "left"

        max_speed = random.randint(3, 20)
        if self.vel.length() > max_speed:
            self.vel = self.vel.normalize() * max_speed

        old_position = self.rect.copy()
        # self.position = self.position.lerp(self.position + (self.vel * dt), f)

        # print("PRE", self.vel, self.position)

        self.rect.y = lerp(self.rect.y, self.rect.y + (self.vel.y * dt), fy)

        if self.collision_map.rect_collision(
            bbox=BBox(self.rect.x + 0.2, self.rect.y + 0.1, 0.6, 0.9)
        ):
            if old_position.y < self.rect.y:
                self.is_able_to_jump = True
            else:
                self.is_jumping = False

            self.rect.y = old_position.y
            self.vel.y = 0

        self.rect.x = lerp(self.rect.x, self.rect.x + (self.vel.x * dt), fx)

        if self.collision_map.rect_collision(
            bbox=BBox(self.rect.x + 0.2, self.rect.y + 0.1, 0.6, 0.9)
        ):
            # print("x1", self.position.x)
            self.rect.x = old_position.x
            # print("x2", self.position.x)
            self.vel.x = 0

    def gravity(self, dt):
        f = 0.2
        old_position = self.rect.copy()

        y_val = 300
        fy = 0.50

        acceleration = Vec2(0.0, y_val)

        if self.is_jumping == False and self.is_able_to_jump == False:
            acceleration.y += 1.50 * y_val

        fx = 0.45  # 0<f<1
        fy = 0.50  # 0<f<1
        if abs(acceleration.x) > 0:
            self.vel.x = lerp(
                self.vel.x,
                self.vel.x + (acceleration.x * self.inertia * dt),
                fx,
            )
        else:
            self.vel.x = lerp(self.vel.x, 0.0, fx)

        if abs(acceleration.y) > 0:
            self.vel.y = lerp(
                self.vel.y,
                self.vel.y + (acceleration.y * self.inertia * dt),
                fy,
            )
        else:
            self.vel.y = lerp(self.vel.y, 0.0, fy)

        if self.vel.x > 0:
            self.facing = "right"
        elif self.vel.x < 0:
            self.facing = "left"

        max_speed = 5
        if self.vel.length() > max_speed:
            self.vel = self.vel.normalize() * max_speed

        old_position = self.rect.copy()
        # self.position = self.position.lerp(self.position + (self.vel * dt), f)

        # print("PRE", self.vel, self.position)

        self.rect.y = lerp(self.rect.y, self.rect.y + (self.vel.y * dt), fy)

        if self.collision_map.rect_collision(
            bbox=BBox(self.rect.x + 0.2, self.rect.y + 0.1, 0.6, 0.9)
        ):
            if old_position.y < self.rect.y:
                self.is_able_to_jump = True
            else:
                self.is_jumping = False

            self.rect.y = old_position.y
            self.vel.y = 0

        self.rect.x = lerp(self.rect.x, self.rect.x + (self.vel.x * dt), fx)

        if self.collision_map.rect_collision(
            bbox=BBox(self.rect.x + 0.2, self.rect.y + 0.1, 0.6, 0.9)
        ):
            # print("x1", self.position.x)
            self.rect.x = old_position.x
            # print("x2", self.position.x)
            self.vel.x = 0

    # to update all status about enemy
    def update(self, player_pos, window: Window, dt):
        pass

    def draw(self, camera: Camera, animation):
        camera.blit(animation.get_frame(), self.rect * PIXEL_SIZE)

    def get_class(self):
        pass

    def combat(self, bullets: List[Bullet]):
        pass

    def getRect(self):
        return pygame.Rect(
            self.rect.x * PIXEL_SIZE, self.rect.y * PIXEL_SIZE, PIXEL_SIZE, PIXEL_SIZE
        )


class Warrior(Enemy):
    # def __init__(self, path, pos, dist, vel, collision_map):
    #     super().__init__(path, pos, dist, vel, collision_map)
    #     self.strong_attack = False
    # self.cooldown = cooldown
    def __init__(self, pos: Vec2, collision_map: Map):
        super().__init__(pos, collision_map)

    def update(self, window: Window, animation: Animation, player_pos):
        f = 0.2
        old_vel = self.vel

        if 0.7 < self.activate(player_pos) < self.dist:
            self.move(player_pos, window.get_delta())
        else:
            self.gravity(window.get_delta())

        animation.update(window)

    def get_class(self) -> str:
        return "warrior"

    def is_dead(self) -> bool:
        if self.health <= 0:
            return True
        return False

    def combat(self, bullet_manager: BulletManager) -> bool:
        bullets = bullet_manager.get_bullets()
        for bullet in bullets:
            bullet_box = bullet.getRect()

            tmp_rect = pygame.Rect(
                bullet_box.x * PIXEL_SIZE,
                bullet_box.y * PIXEL_SIZE,
                bullet_box.w * PIXEL_SIZE,
                bullet_box.h * PIXEL_SIZE,
            )
            print(self.getRect(), tmp_rect)
            if self.getRect().colliderect(tmp_rect):
                bullet_manager.remove_bullet(bullet)
                print("OK")
                self.health -= 1
                if self.is_dead():
                    return self
        return None


class Sorcerer(Enemy):
    def __init__(self, pos: Vec2, collision_map: Map):
        super().__init__(pos, collision_map)

    def shoot(self, player_pos):
        if self.can_shoot(player_pos):
            print("OK")

    def update(self, player_pos, camera: Camera, dt):
        flag = False
        pressed_keys = pygame.key.get_pressed()

        if pressed_keys[pygame.K_k]:
            flag = True
        if flag:
            self.bullets.append(
                Bullet(
                    "res/plant.png",
                    self.rect,
                    Vec2(2, 2),
                    Vec2(0, 1),
                    self.collision_map,
                )
            )
        new_bullets = []

        for bullet in self.bullets:
            if bullet.update(camera, dt):
                new_bullets.append(bullet)
        self.bullets = new_bullets

        self.ticks += dt
        if self.ticks > 2:
            self.shoot(player_pos)
            self.ticks = 0
        f = 0.2

        old_vel = self.vel

        if 3 < self.activate(player_pos) < self.dist:
            self.move(player_pos, dt)

        new_bullets = []

        self.draw(
            camera, self.image, (self.rect.x * PIXEL_SIZE, self.rect.y * PIXEL_SIZE)
        )
        self.vel = old_vel

    def can_shoot(self, player_pos):
        if self.activate(player_pos) < self.dist - 1:
            return True
        return False

    def get_class(self):
        return "sorcerer"


warrior_anim = Animation(
    pygame.transform.scale(pygame.image.load("res/wojownik-sheet.png"), (64 * 2, 64)),
    cols=2,
    frame_rate=8,
)


# sorcer_anim = Animation(pygame.transform.scale(pygame.image.load("path..."), (64, 64))
#                           , cols=-1, frame_rate= 8)
class EnemyManager:
    def __init__(self, collision_map: Map):
        self._enemies = []
        self.collision_map = collision_map
        self._classes = {"warrior": Warrior, "sorcerer": Sorcerer}
        # self._animations = {"warrior" :  warrior_anim, "sorcerer": sorcer_anim} # fill with path
        self._animations = {"warrior": warrior_anim}  # fill with path

    def get_enemies(self) -> List[Enemy]:
        return self._enemies

    def add_enemy(self, enemy_class: str, possition: Vec2):
        self._enemies.append(self._classes[enemy_class](possition, self.collision_map))

    def remove_enemy(self, enemy: Enemy):
        self._enemies.remove(enemy)

    def clear(self):
        self._enemies = []

    def update(self, window: Window, player_pos: Vec2, bullets_manager: BulletManager):
        for enemy in self._enemies:
            to_delete = enemy.combat(bullets_manager)
            enemy.update(window, self._animations[enemy.get_class()], player_pos)

            if to_delete is not None:
                self.remove_enemy(to_delete)

    def draw(self, camera: Camera):
        for enemy in self._enemies:
            enemy.draw(camera, self._animations[enemy.get_class()])


enemies = []
enum = {"warrior": Warrior, "sorcerer": Sorcerer}


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


# def add_enemy(type_of_enemy, path, position, distance, vel_of_chase, collision_map):
#     if type_of_enemy == "warrior":
#         enemies.append(
#             enum["warrior"](path, position, distance, vel_of_chase, collision_map)
#         )

#     if type_of_enemy == "sorcerer":
#         enemies.append(
#             enum["sorcerer"](path, position, distance, vel_of_chase, collision_map)
#         )


def update_all(player_pos, camera, timer):
    for enemy in enemies:
        enemy.update(player_pos, camera, timer)


if __name__ == "__main__":
    pass


# update
# draw

# zhardcodzic path do zfd
