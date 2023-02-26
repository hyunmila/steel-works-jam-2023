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
from components.explosion import ExplosionManager


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

warrior_img = None
warrior_anim = None
sorcerer_img = None


class Enemy(metaclass=abc.ABCMeta):
    def __init__(self, pos: Vec2, collision_map: Map):
        global warrior_img, warrior_anim, sorcerer_img
        if warrior_img is None:
            warrior_img = pygame.image.load("res/wojownik-sheet.png").convert_alpha()
            warrior_img = pygame.transform.scale(warrior_img, (64 * 2, 64))
            warrior_anim = Animation(warrior_img, cols=2, frame_rate=0.5)

            sorcerer_img = [
                pygame.transform.scale(
                    pygame.image.load("res/mutan_mage_ult.png").convert_alpha(),
                    (PIXEL_SIZE, PIXEL_SIZE),
                ),
                pygame.transform.scale(
                    pygame.image.load("res/mutant_mage.png").convert_alpha(),
                    (PIXEL_SIZE, PIXEL_SIZE),
                ),
            ]

        self.rect = pos
        self.facing = "left"
        self.vel = Vec2(0.0, 0.0)
        self.dist = 3
        self.collision_map = collision_map
        self.health = 3
        self.ticks = 3
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

    def is_dead(self):  # True if enemy is dead
        if self.health <= 0:
            return True
        return False

    def move(self, player_pos, dt):
        old_position = self.rect.copy()

        x_val = 50
        y_val = 200
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
    def update(self, window: Window, player_pos):
        pass

    def draw(self, camera: Camera):
        pass

    def get_class(self):
        pass

    def combat(self, bullet_meneger: BulletManager) -> bool:
        bullets = bullet_meneger.get_bullets()
        for bullet in bullets:
            bullet_box = bullet.getRect()

            tmp_rect = pygame.Rect(
                bullet_box.x * PIXEL_SIZE,
                bullet_box.y * PIXEL_SIZE,
                bullet_box.w * PIXEL_SIZE,
                bullet_box.h * PIXEL_SIZE,
            )

            if self.getRect().colliderect(tmp_rect):
                bullet_meneger.remove_bullet(bullet)
                self.health -= 1
                if self.is_dead():
                    return self
        return None

    def getRect(self):
        return pygame.Rect(
            self.rect.x * PIXEL_SIZE, self.rect.y * PIXEL_SIZE, PIXEL_SIZE, PIXEL_SIZE
        )

    def attack(
        self, possition
    ) -> bool:  # True - gdy atak dosięga gracza, False - w przeciwnym przypadku
        pass


class Warrior(Enemy):
    # def __init__(self, path, pos, dist, vel, collision_map):
    #     super().__init__(path, pos, dist, vel, collision_map)
    #     self.strong_attack = False
    # self.cooldown = cooldown
    def __init__(self, pos: Vec2, collision_map: Map):
        super().__init__(pos, collision_map)
        self.cooldown = 2

    def update(self, window: Window, player_pos):
        f = 0.2
        old_vel = self.vel
        self.ticks += window.get_delta()
        if player_pos.x > self.rect.x:
            self.facing = "right"
        else:
            self.facing = "left"
        if 0.7 < self.activate(player_pos) < self.dist:
            self.move(player_pos, window.get_delta())
        else:
            self.gravity(window.get_delta())

    def get_class(self) -> str:
        return "warrior"

    def attack(self, possition: Vec2):  # possition in meters ( has to multiply for 64)
        tmp_vec = Vec2(possition.x - self.rect.x, possition.y - self.rect.y)
        if self.ticks < self.cooldown:
            return False
        if tmp_vec.length() < 0.7:
            self.ticks = 0
            return True
        return False

    def draw(self, camera: Camera):
        img = warrior_anim.rasterize()
        if self.facing == "right":
            img = pygame.transform.flip(img, True, False)
        camera.blit(img, self.rect * PIXEL_SIZE)


class Sorcerer(Enemy):
    def __init__(self, pos: Vec2, collision_map: Map):
        super().__init__(pos, collision_map)
        self.explosion_manager = ExplosionManager()
        self.bullet_manager = BulletManager(
            collision_map, explosion_manager=self.explosion_manager
        )
        self.flag = True
        self.cooldown = 1
        self.animidx = 0
        self.shoot_ticks = 0

    def shoot(self, player_pos):
        if self.can_shoot(player_pos):
            print("OK")

    def move(self, player_pos, dt):
        old_position = self.rect.copy()

        x_val = 50
        y_val = 300
        fy = 0.7

        acceleration = Vec2(0.0, y_val)
        # ------------------------------------------------------------

        if player_pos.x > self.rect.x:  # warunek chodzenia w prawoa
            acceleration.x += x_val
        if player_pos.x < self.rect.x:  # warunek dla chodzenia w lewo
            acceleration.x -= x_val

        if (
            not self.is_able_to_shoot(player_pos)
            and player_pos.y < self.rect.y
            and self.collision_map.rect_collision(
                bbox=BBox(self.rect.x, self.rect.y, 1, 1)
            )
            or self.collision_map.rect_collision(
                bbox=BBox(self.rect.x, self.rect.y, 1, 1)
            )
        ):  # warunek skoku
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

    # def update(self, player_pos, camera: Camera, dt):
    #     flag = False
    #     pressed_keys = pygame.key.get_pressed()

    #     if pressed_keys[pygame.K_k]:
    #         flag = True
    #     if flag:
    #         self.bullets.append(
    #             Bullet(
    #                 "res/plant.png",
    #                 self.rect,
    #                 Vec2(2, 2),
    #                 Vec2(0, 1),
    #                 self.collision_map,
    #             )
    #         )
    #     new_bullets = []

    #     for bullet in self.bullets:
    #         if bullet.update(camera, dt):
    #             new_bullets.append(bullet)
    #     self.bullets = new_bullets

    #     self.ticks += dt
    #     if self.ticks > 2:
    #         self.shoot(player_pos)
    #         self.ticks = 0
    #     f = 0.2

    #     old_vel = self.vel

    #     if 3 < self.activate(player_pos) < self.dist:
    #         self.move(player_pos, dt)

    #     new_bullets = []

    #     self.draw(
    #         camera, self.image, (self.rect.x * PIXEL_SIZE, self.rect.y * PIXEL_SIZE)
    #     )
    #     self.vel = old_vel
    def update(self, window: Window, player_pos):
        f = 0.2
        if self.ticks > 0.1:
            self.animidx += 1
            self.ticks = 0

        self.ticks += window.get_delta()
        self.shoot_ticks += window.get_delta()

        if (
            self.can_shoot(player_pos)
            and self.is_able_to_shoot(player_pos)
            and self.shoot_ticks > 1
        ):
            self.shoot_ticks = 0
            direction = Vec2(player_pos - self.rect).normalize()
            self.bullet_manager.add_bullet(self.rect, direction)

        self.bullet_manager.update(window)
        self.explosion_manager.update(window)

        if player_pos.x > self.rect.x:
            self.facing = "right"
        else:
            self.facing = "left"

        if 0.7 < self.activate(player_pos) < self.dist:
            self.move(player_pos, window.get_delta())
        else:
            self.gravity(window.get_delta())

    def can_shoot(self, player_pos):
        if self.activate(player_pos) < self.dist - 1:
            return True
        return False

    def is_able_to_shoot(
        self, player_pos
    ) -> (
        bool
    ):  # można przyjąć jako wiąze światła - sprawdzanie czy dociera do celu jakim jest player_pos
        vect = Vec2(player_pos.x - self.rect.x, player_pos.y - self.rect.y)
        sample_vect = Vec2(vect.x / 50, vect.y / 50)
        samples = [self.rect + sample_vect * i for i in range(50)]
        for sample in samples:
            if self.collision_map.rect_collision(
                bbox=BBox(sample.x, sample.y, 0.05, 0.05)
            ):
                return False
        return True

    def get_class(self):
        return "sorcerer"

    def draw(self, camera: Camera):
        self.bullet_manager.draw(camera)
        self.explosion_manager.draw(camera)
        img = sorcerer_img[self.animidx % len(sorcerer_img)]
        if self.facing == "right":
            img = pygame.transform.flip(img, True, False)
        camera.blit(img, self.rect * PIXEL_SIZE)

    def attack(self, possition: Vec2) -> bool:
        bullets = self.bullet_manager.get_bullets()
        for bullet in bullets:
            tmp_vec = Vec2(
                bullet.position.x - possition.x, bullet.position.y - possition.y
            )
            if tmp_vec.length() < 0.2:
                self.bullet_manager.remove_bullet(bullet)
                return True
        return False


boss_img = None


class Boss:
    def __init__(self, pos: Vec2, collision_map: Map):
        global boss_img
        if boss_img is None:
            boss_img = [
                pygame.transform.scale(
                    pygame.image.load("res/jola_na_sterydach.png").convert_alpha(),
                    (PIXEL_SIZE * 4, PIXEL_SIZE * 4),
                ),
            ]

        self.position = pos
        self.facing = "left"
        self.vel = Vec2(0.0, 0.0)
        self.dist = 10
        self.collision_map = collision_map
        self.health = 20
        self.ticks = 2
        self.max_distance = 2
        self.explosion_manager = ExplosionManager()
        self.bullet_manager = BulletManager(collision_map, self.explosion_manager)
        self.animidx = 0
        self.shoot_ticks = 0
        self.movement_ticks = 0

    def is_dead(self):  # True if enemy is dead
        if self.health <= 0:
            return True
        return False

    def get_class(self):
        return "boss"

    def distance(self, pos):
        return Vec2(pos.x - self.position.x, pos.y - self.position.y).length()

    def combat(
        self, bullet_meneger: BulletManager
    ) -> bool:  # przyjmowanie damage na twarz
        bullets = bullet_meneger.get_bullets()
        for bullet in bullets:
            bullet_box = bullet.getRect()

            tmp_rect = pygame.Rect(
                bullet_box.x * PIXEL_SIZE,
                bullet_box.y * PIXEL_SIZE,
                bullet_box.w * PIXEL_SIZE,
                bullet_box.h * PIXEL_SIZE,
            )

            if self.getRect().colliderect(tmp_rect):
                bullet_meneger.remove_bullet(bullet)
                self.health -= 1
                if self.is_dead():
                    return self
        return None

    def movement(self, player_pos, dt):
        # 1280 - rozmiar ekranu w pixelach / 4
        old_position = self.position.copy()
        vel = Vec2(2, 2)
        fx = 0.70

        if self.movement_ticks < 1:
            self.position.y = lerp(
                self.position.y, self.position.y + ((-vel.y) * dt), fx
            )
        elif self.movement_ticks < 2:
            self.position.y = lerp(self.position.y, self.position.y + (vel.y * dt), fx)
        else:
            self.movement_ticks = 0
        # def lerp(a, b, t):
        #   return a + t * (b - a)
        if self.distance(player_pos) > self.max_distance:
            if player_pos.x > self.position.x:
                self.position.x = lerp(
                    self.position.x, self.position.x + (vel.x * dt), fx
                )
            else:
                self.position.x = lerp(
                    self.position.x, self.position.x + (-vel.x * dt), fx
                )

        if self.collision_map.rect_collision(
            bbox=BBox(self.position.x, self.position.y, 4, 4)
        ):
            self.position.x = old_position.x

    def can_shoot(self, player_pos):
        if self.distance(player_pos) < self.dist - 1:
            return True
        return False

    def is_able_to_shoot(
        self, player_pos
    ) -> (
        bool
    ):  # można przyjąć jako wiąze światła - sprawdzanie czy dociera do celu jakim jest player_pos
        vect = Vec2(player_pos.x - self.position.x, player_pos.y - self.position.y)
        sample_vect = Vec2(vect.x / 50, vect.y / 50)
        samples = [self.position + sample_vect * i for i in range(50)]
        for sample in samples:
            if self.collision_map.rect_collision(
                bbox=BBox(sample.x, sample.y, 0.05, 0.05)
            ):
                return False
        return True

    def update(self, window: Window, player_pos):
        self.ticks += window.get_delta()
        self.shoot_ticks += window.get_delta()
        self.movement_ticks += window.get_delta()

        self.movement(player_pos, window.get_delta())

        if self.ticks > 0.1:
            self.animidx += 1
            self.ticks = 0

        if player_pos.x > self.position.x:
            self.facing = "right"
        else:
            self.facing = "left"

        if (
            self.can_shoot(player_pos)
            and self.is_able_to_shoot(player_pos)
            and self.shoot_ticks > 0.3
        ):
            self.shoot_ticks = 0
            direction = Vec2(player_pos - self.position).normalize()
            self.bullet_manager.add_bullet(self.position + Vec2(1, 1), direction)

        self.bullet_manager.update(window)
        self.explosion_manager.update(window)

    def draw(self, camera: Camera):
        self.bullet_manager.draw(camera)
        self.explosion_manager.draw(camera)
        img = boss_img[self.animidx % len(boss_img)]
        if self.facing == "right":
            img = pygame.transform.flip(img, True, False)
        camera.blit(img, self.position * PIXEL_SIZE)

    def getRect(self):
        return pygame.Rect(
            self.position.x * PIXEL_SIZE,
            self.position.y * PIXEL_SIZE,
            PIXEL_SIZE,
            PIXEL_SIZE,
        )

    def attack(self, possition: Vec2) -> bool:
        bullets = self.bullet_manager.get_bullets()
        for bullet in bullets:
            tmp_vec = Vec2(
                bullet.position.x - possition.x, bullet.position.y - possition.y
            )
            if tmp_vec.length() < 0.2:
                self.bullet_manager.remove_bullet(bullet)
                return True
        return False


# sorcer_anim = Animation(pygame.transform.scale(pygame.image.load("path..."), (64, 64))
#                           , cols=-1, frame_rate= 8)
class EnemyManager:
    def __init__(self, collision_map: Map):
        self._enemies = []
        self.collision_map = collision_map
        self._classes = {"warrior": Warrior, "sorcerer": Sorcerer, "boss": Boss}
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
        warrior_anim.update(window)
        for enemy in self._enemies:
            to_delete = enemy.combat(bullets_manager)
            # tmp = self._animations[enemy.get_class()]
            # enemy.update(window, self._animations[enemy.get_class()], player_pos)
            # enemy.update(window, tmp, player_pos)
            enemy.update(window, player_pos)

            if to_delete is not None:
                self.remove_enemy(to_delete)

    def draw(self, camera: Camera):
        for enemy in self._enemies:
            # enemy.draw(camera, self._animations[enemy.get_class()])
            enemy.draw(camera)


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
