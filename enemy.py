import pygame
import random 
from math import sqrt
from pygame.math import Vector2 as Vec2
from colors import COLOR
import abc
import time


pygame.init()

WIDTH, HEIGHT = 1280, 720
CENTER = pygame.math.Vector2(300, 300)
__screen = pygame.display.set_mode([WIDTH, HEIGHT], pygame.RESIZABLE)
screen = __screen.copy()

pygame.display.set_caption("SteelWorksJam 2023")

running = True

screen.fill(COLOR.BLACK)
clock = pygame.time.Clock()
dt = clock.tick(60)
ticks = 0

VEL = 5 # global velocity
# path = 'graphics/Fly1.png'

class Box():
    def __init__(self, pos, size):
        self.pos = pos
        self.size = size
        self.velocity = Vec2(0., 0.)

    def get_points(self):
        l = Vec2(0, self.size.y/2)
        t = Vec2(self.size.x/2, 0)
        
        return (
            ((self.pos + l + t).x, (self.pos + l + t).y),
            ((self.pos + l - t).x, (self.pos + l - t).y),
            ((self.pos - l - t).x, (self.pos - l - t).y),
            ((self.pos - l + t).x, (self.pos - l + t).y)
        )

    def move(self, dt):
        self.pos += self.velocity*dt


class Enemy(metaclass = abc.ABCMeta):
    def __init__(self, path, pos, dist, vel):
        self.image = pygame.image.load(path)
        self.rect = self.image.get_rect(center = pos)
        self.gravity = 0
        self.vel = vel
        self.dist = dist
        self.self_space = self.rect.center
        self.health = 3
    
    # when player is too close to enemy, then enemy is starting chaise him
    def activate(self, pos):
        return Vec2(pos.x - self.rect.x, pos.y - self.rect.y).length()
    
    # to update all status about enemy
    def update(self, player_pos):
        self.draw()
        self.ability()
        if self.activate(player_pos) < self.dist:
            self.chase(player_pos)
    

    @abc.abstractmethod
    def chase(self, pos):
        pass
    
    @abc.abstractmethod
    def ability(self, cooldown):
        pass

    def draw(self):
        screen.blit(self.image, self.rect)
    
    def getRect(self) -> pygame.Rect:
        return self.rect
    
    def setPosX(self, pos):
        self.rect.x += pos
    
    def setPosY(self, pos):
        self.rect.y += pos
    

    

class Warrior(Enemy):
    def __init__(self, path, pos, dist, vel, cooldown = 5):
        super().__init__(path, pos, dist, vel)
        self.strong_attack = False
        self.cooldown = cooldown
        self.start = time.time()
    
    def chase(self, pos):
        vec = Vec2(pos.x - self.rect.x, pos.y - self.rect.y)
        if vec.length() != 0:
            vec.normalize_ip()
            new_vec = Vec2(vec.x * self.vel / sqrt(2), vec.y * self.vel / sqrt(2))

            self.rect.x = new_vec.x + self.rect.x
            self.rect.y = new_vec.y + self.rect.y
    
    def ability(self, cooldown): # super attack
        return cooldown - time.time()


    
        

class Sorcerer(Enemy):
    def __init__(self, path, pos, dist, vel):
        super().__init__(path, pos, dist, vel)

class Healer(Enemy):
    def __init__(self, path, pos, dist, vel):
        super().__init__(path, pos, dist, vel)

class Tank(Enemy):
    def __init__(self, path, pos, dist, vel):
        super().__init__(path, pos, dist, vel)
    
    def chase(self, pos):
        pass
        

class Archer(Enemy):
    def __init__(self, path, pos, dist, vel):
        super().__init__(path, pos, dist, vel)

def enemy_collision(enemies : list[Enemy]):
    n = len(enemies)
    dt = 10
    for _ in range(1000):
        random.shuffle(enemies)
        for i in range(n-1):
                for j in range(i+1, n):

                    box1 = Box(Vec2(enemies[i].getRect().topright), Vec2(enemies[i].getRect().width, enemies[i].getRect().height)) # Rect()
                    box2 = Box(Vec2(enemies[j].getRect().topright), Vec2(enemies[j].getRect().width, enemies[j].getRect().height)) # Rect()
                    
                    rect1 = enemies[i].getRect()
                    rect2 = enemies[j].getRect()


                    l1 = (box1.pos - box1.size/2)
                    r1 = (box1.pos + box1.size/2)
                    l2 = (box2.pos - box2.size/2)
                    r2 = (box2.pos + box2.size/2)

                    x = min(r1.x, r2.x) - max(l1.x, l2.x)
                    y = min(r1.y, r2.y) - max(l1.y, l2.y)   

                    if x <= 0 or y <= 0: continue

                    vec1 = Vec2((rect1.topleft[0] - rect1.center[0]) * 2,
                                (rect1.topleft[1] - rect1.center[1])*2 ).length() # ????
                    
                    vec = Vec2(rect1.center[0] - rect2.center[0], rect1.center[1] - rect2.center[1])
                    vec_len = vec.length()

                    if vec_len > 100: continue 

                    if x < y:
                        if box1.pos.x > box2.pos.x: x *= -1
                        # rect1.pos.x -= x
                        enemies[i].setPosX(-x)
                        # rect2.pos.x += x
                        enemies[j].setPosX(x)

                    else:
                        if box1.pos.y > box2.pos.y: y *= -1
                        # rect1.pos.y -= y
                        enemies[i].setPosY(-y)
                        # rect2.pos.y += y
                        enemies[j].setPosY(y)
                    
                    enemies[j].setPosX(random.random())
                    enemies[j].setPosY(random.random())

                    # enemies[i].setPosX(random.random())
                    # enemies[i].setPosY(random.random())

                    
                
player = pygame.image.load('graphics/snail1.png')
player_rec = player.get_rect(center = Vec2(100, 100))

enemy1 = Warrior('graphics/Fly1.png', CENTER, 200, 4)
warior1 = Warrior('graphics/Fly1.png', CENTER + Vec2(100, 100), 200, 4)

enemies = [enemy1, warior1, Warrior('graphics/Fly1.png', CENTER, 200, 4), Warrior('graphics/Fly1.png', CENTER, 200, 4)]

while running:
    screen.fill(COLOR.BLACK)
    dt = clock.tick(60)
    ticks += dt

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pressed_keys = pygame.key.get_pressed()

    # pygame.draw.circle(screen, COLOR.WHITE, CENTER, 20)
    screen.blit(player, player_rec)
    

    if pressed_keys[pygame.K_w]:
        player_rec.y -= VEL
    if pressed_keys[pygame.K_s]:
        player_rec.y += VEL
    if pressed_keys[pygame.K_d]:
        player_rec.x += VEL
    if pressed_keys[pygame.K_a]:
        player_rec.x -= VEL
    
    for enemy in enemies:
        enemy.update(player_rec)

    __scaled = pygame.transform.scale(screen, (__screen.get_width(), __screen.get_height()))
    __screen.blit(__scaled, (0, 0))

    enemy_collision(enemies)
    pygame.display.flip()
