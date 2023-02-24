import pygame
from colors import COLOR

pygame.init()

WIDTH, HEIGHT = 800, 800
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption("SteelWorksJam 2023")

running = True

screen.fill(COLOR.BLACK)
clock = pygame.time.Clock()
dt = clock.tick(60)
ticks = 0

while running:
    dt = clock.tick(60)
    ticks += dt

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pressed_keys = pygame.key.get_pressed()

    if pressed_keys[pygame.K_w]:
        print(f"dt = {dt}")

    screen.fill(COLOR.BLACK)
    pygame.display.flip()
