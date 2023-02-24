import pygame
from pygame.math import Vector2 as Vec2
from colors import COLOR

pygame.transform

pygame.init()

WIDTH, HEIGHT = 600, 600
CENTER = pygame.math.Vector2(300, 300)
__screen = pygame.display.set_mode([WIDTH, HEIGHT], pygame.RESIZABLE)
screen = __screen.copy()

pygame.display.set_caption("SteelWorksJam 2023")

running = True

screen.fill(COLOR.BLACK)
clock = pygame.time.Clock()
dt = clock.tick(60)
ticks = 0

while running:
    screen.fill(COLOR.BLACK)
    dt = clock.tick(60)
    ticks += dt

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pressed_keys = pygame.key.get_pressed()

    pygame.draw.circle(screen, COLOR.WHITE, Vec2(200, 200), 50)

    if pressed_keys[pygame.K_w]:
        print(f"dt = {dt}")

    __scaled = pygame.transform.scale(screen, (__screen.get_width(), __screen.get_height()))
    __screen.blit(__scaled, (0, 0))
    pygame.display.flip()
