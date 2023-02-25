import pygame
from pygame.math import Vector2 as Vec2
from colors import COLOR
from player import Player
from text_display import TextDisplay

pygame.transform

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
player = Player()
# text display
text = 'Jak to jest byc skryba, dobrze?\nTo nie ma tak, ze dobrze czy niedobrze\nGdybym mial powiedziec'
fontcolor = COLOR.BLUE
textdisplay = TextDisplay(text, fontcolor, fontsize = 16)
textposition = (100,100)
# print(textdisplay.img.get_width()/2, textdisplay.img.get_height()/2) # fontsize 16x16 idealne kwadraty uwu

while running:
    screen.fill(COLOR.BLACK)
    dt = clock.tick(60)
    ticks += dt

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pressed_keys = pygame.key.get_pressed()
    player.update(pressed_keys, dt)
    pygame.draw.circle(screen, COLOR.WHITE, player.position, 50)

    if pressed_keys[pygame.K_w]:
        print(f"dt = {dt}")
    screen.blit(textdisplay.img, textposition) # text display
    __scaled = pygame.transform.scale(screen, (__screen.get_width(), __screen.get_height()))
    __screen.blit(__scaled, (0, 0))
    pygame.display.flip()
