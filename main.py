import pygame
from pygame.math import Vector2 as Vec2
from colors import COLOR

from src.weapon import Weapon
from src.item import Item, ItemType

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

weapon = Weapon()

item = Item(
    name='dupa',
    item_type=ItemType.GUN,
    weight=69.0,
    shape=(2,3),
    ammo_type="dupa2",
    img=pygame.image.load("res/test.png")
)

weapon.add_item(item)

while running:
    screen.fill(COLOR.BLACK)
    dt = clock.tick(60)
    ticks += dt
    scale_width = __screen.get_width()/screen.get_width()
    scale_height = __screen.get_height()/screen.get_height()
    relative_mouse = Vec2(pygame.mouse.get_pos())
    relative_mouse.x /= scale_width
    relative_mouse.y /= scale_height

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pressed_keys = pygame.key.get_pressed()

    pygame.draw.circle(screen, COLOR.WHITE, Vec2(200, 200), 50)

    if pressed_keys[pygame.K_w]:
        print(f"dt = {dt}")

    screen.blit(weapon.process(relative_mouse), (0, 0))

    __scaled = pygame.transform.scale(screen, (__screen.get_width(), __screen.get_height()))
    __screen.blit(__scaled, (0, 0))
    pygame.display.flip()
