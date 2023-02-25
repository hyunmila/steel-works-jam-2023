import pygame
from pygame.math import Vector2 as Vec2
from colors import Color
from map_engine import BBox, MapEngine, Tile
from player import Player

pygame.init()

WIDTH, HEIGHT = 1280, 720
CENTER = pygame.math.Vector2(300, 300)
__screen = pygame.display.set_mode([WIDTH, HEIGHT], pygame.RESIZABLE)
screen = __screen.copy()

pygame.display.set_caption("SteelWorksJam 2023")

running = True

screen.fill(Color.BLACK)
clock = pygame.time.Clock()
dt = clock.tick(60)
ticks = 0

map_engine = MapEngine(
    tiles={
        Color.WHITE: Tile("", False),
        Color.BLACK: Tile("res/metalowa-podłoga-2.png", True),
    },
    tile_size=64,
)

map_engine.load_from_file("res/test-map.png")

player_pos = Vec2(0, 0)
player_speed = Vec2(0, 0)

player = Player()

# text display
text = "Jak to jest byc skryba, dobrze?\nTo nie ma tak, ze dobrze czy niedobrze\nGdybym mial powiedziec"
fontcolor = COLOR.BLUE
textdisplay = TextDisplay(text, fontcolor, fontsize=16)
textposition = (100, 100)
# print(textdisplay.img.get_width()/2, textdisplay.img.get_height()/2) # fontsize 16x16 idealne kwadraty uwu

while running:
    screen.fill(Color.BLACK)
    dt = clock.tick(60)
    ticks += dt

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                player_speed.y = -5

    pressed_keys = pygame.key.get_pressed()

    pygame.draw.circle(screen, Color.WHITE, Vec2(200, 200), 50)

    if pressed_keys[pygame.K_w]:
        print(f"dt = {dt}")

    player_speed.x = int(pressed_keys[pygame.K_d]) - int(pressed_keys[pygame.K_a])
    player_speed.x *= 5

    player_pos[0] += player_speed.x * (dt / 1000)
    player_pos[1] += player_speed.y * (dt / 1000)
    if map_engine.rect_collision(bbox=BBox(player_pos.x, player_pos.y, 1, 1)):
        player_pos[0] -= player_speed.x * (dt / 1000)
        player_pos[1] -= player_speed.y * (dt / 1000)
        player_speed.x = 0
        player_speed.y = 0

    player_speed.y += 9.81 * (dt / 1000)

    # epicki gracz Mili
    player.update(pressed_keys, dt)
    pygame.draw.circle(screen, COLOR.WHITE, player.position, 50)

    # Rendering
    screen.blit(textdisplay.img, textposition)  # text display
    map_engine.draw(screen=screen, offset=(0, 0))
    pygame.draw.polygon(
        screen,
        (255, 0, 0),
        (
            (64 * player_pos[0], 64 * player_pos[1]),
            (64 * (player_pos[0] + 1), 64 * player_pos[1]),
            (64 * (player_pos[0] + 1), 64 * (player_pos[1] + 1)),
            (64 * player_pos[0], 64 * (player_pos[1] + 1)),
        ),
    )

    __scaled = pygame.transform.scale(
        screen, (__screen.get_width(), __screen.get_height())
    )
    __screen.blit(__scaled, (0, 0))
    pygame.display.flip()
