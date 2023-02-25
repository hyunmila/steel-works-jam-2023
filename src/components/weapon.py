import pygame
from typing import List, Tuple, Optional
from item import Item, ItemType
from inventory import Inventory
from pygame.math import Vector2 as Vec2

# from core.camera import Camera
from components.text_box import TextBox
from core.camera import Camera
from core.window import Window


class WeaponManager:
    GRID_WIDTH = 16
    GRID_HEIGHT = 8
    GRID = [[None for _ in range(8)] for _ in range(16)]

    def __init__(self):
        self.items: List[Tuple[Item, Vec2]] = []
        self.inventory = Inventory()
        self.selected_item: Optional[Item] = None
        self.visible = False
        self.surface = None

    def is_valid(self, spot, item):
        rect = pygame.Rect(spot, item.shape)

        if (spot[0] + item.shape[0] > self.GRID_WIDTH) or (
            spot[1] + item.shape[1] > self.GRID_HEIGHT
        ):
            return False

        for item, spot in self.items:
            rect2 = pygame.Rect(spot, item.shape)
            if rect.colliderect(rect2):
                return False
        return True

    def get_item_index_at_spot(self, spot) -> Optional[int]:
        spot = Vec2(spot)
        for i, (item, pos) in enumerate(self.items):
            tl = Vec2(pos)
            br = tl + Vec2(item.shape)

            if (tl.x <= spot.x < br.x) and (tl.y <= spot.y < br.y):
                return i
        return None

    def add_item(self, item):
        self.inventory.add_item(item)

    def put_item(self, spot: Vec2, item: Item):
        if self.is_valid(spot, item) and self.inventory.get_count(item) > 0:
            self.items.append((item, spot))
            self.inventory.remove_item(item)

    def load_grid(self):
        self.GRID = [
            [None for _ in range(self.GRID_HEIGHT)] for _ in range(self.GRID_WIDTH)
        ]

        for item, spot in self.items:
            start = Vec2(spot)
            end = start + Vec2(item.shape)

            for i in range(int(start.x), int(end.x)):
                for j in range(int(start.y), int(end.y)):
                    self.GRID[i][j] = item

    def is_connected(self):
        self.load_grid()
        if len(self.items) < 1:
            return True

        tile_count = sum(
            sum(1 if x is not None else 0 for x in row) for row in self.GRID
        )
        vis = [[False for _ in range(len(row))] for row in self.GRID]

        i, j = map(int, self.items[0][1])

        count = 0
        stack = [(i, j)]

        while len(stack) > 0:
            i, j = stack.pop()

            if not (0 <= i < len(self.GRID)):
                continue
            if not (0 <= j < len(self.GRID[0])):
                continue
            if vis[i][j] or self.GRID[i][j] is None:
                continue

            vis[i][j] = True
            count += 1

            stack.append((i + 1, j))
            stack.append((i - 1, j))
            stack.append((i, j + 1))
            stack.append((i, j - 1))

        return count == tile_count

    def will_blow_up(self):
        ammos = [x for x, _ in self.items if x.item_type == ItemType.AMMO]
        weapons = [x for x, _ in self.items if x.item_type == ItemType.GUN]

        for weapon in weapons:
            to_pop = None
            for i, ammo in enumerate(ammos):
                if weapon.ammo_type == ammo.name:
                    to_pop = i
                    break
            else:
                return True
            ammos.pop(to_pop)
        return False or not self.is_connected()

    def get_weapon_as_surface(self):
        weapon_surface = pygame.Surface(
            (self.GRID_WIDTH, self.GRID_HEIGHT), pygame.SRCALPHA, 32
        )
        weapon_surface = weapon_surface.convert_alpha()
        self.load_grid()

        for i in range(len(self.GRID)):
            for j in range(len(self.GRID[i])):
                if self.GRID[i][j] is not None:
                    weapon_surface.set_at((i, j), self.GRID[i][j].color)

        return weapon_surface

    def update(self, window: Window):
        if window.get_input().is_action_just_pressed(action="inventory"):
            self.visible = not self.visible
            if self.visible:
                window.time_scale = 0
            else:
                window.time_scale = 1

        if not self.visible:
            return

        BORDER_COLOR = (0, 0, 0)
        GRID_COLOR = (200, 200, 230)
        SELECTED_GRID_COLOR = (180, 180, 210)
        INVENTORY_COLOR = (150, 150, 180)
        SELECTED_INVENTORY_COLOR = (120, 120, 150)
        BACKGROUND_COLOR = (100, 100, 130)

        width = window.get_ratio() * 720
        height = 720
        grid_width, grid_height = 960, 480
        offset = Vec2((width - grid_width) // 2, (height - grid_height) // 2)
        step = grid_height // self.GRID_HEIGHT
        offset += Vec2(0, -step * 1.25)

        surface = pygame.Surface((width, height), pygame.SRCALPHA, 32)
        surface.fill((0, 0, 0, 150))  # translucent black

        grid_surface = pygame.Surface((grid_width, grid_height))
        grid_surface.fill((0, 255, 0))

        mouse_position = Vec2(window.get_input().get_mouse_pos()) * (
            height / window.get_size()[1]
        )
        grid_relative_mouse_position = mouse_position - offset
        for i in range(len(self.GRID)):
            for j in range(len(self.GRID[i])):
                start_x = i * step
                start_y = j * step

                rect = pygame.Rect(start_x, start_y, step, step)

                color = GRID_COLOR
                if rect.collidepoint(grid_relative_mouse_position):
                    color = SELECTED_GRID_COLOR

                    pressed = pygame.mouse.get_pressed()

                    if pressed[0] and self.selected_item:
                        self.put_item(Vec2(i, j), self.selected_item)

                    k = self.get_item_index_at_spot(Vec2(i, j))
                    if k is not None and pressed[2]:
                        item, _ = self.items.pop(k)
                        self.inventory.add_item(item)

                pygame.draw.rect(grid_surface, color, rect)

        for x in range(step, grid_width, step):
            for y in range(step, grid_height, step):
                pygame.draw.line(
                    grid_surface, BORDER_COLOR, (x, 0), (x, grid_height), width=3
                )
                pygame.draw.line(
                    grid_surface, BORDER_COLOR, (0, y), (grid_width, y), width=3
                )

        item_surface = pygame.Surface((grid_width, 2 * step), pygame.SRCALPHA, 32)

        item_offset = Vec2(0, grid_height) + offset + Vec2(0, step / 2)

        item_relative_mouse_position = mouse_position - item_offset
        for i in range(16):
            start_x = i * step
            start_y = 0  # j*step

            rect = pygame.Rect(start_x, start_y, step, step)

            color = INVENTORY_COLOR
            if rect.collidepoint(item_relative_mouse_position):
                color = SELECTED_INVENTORY_COLOR

                if pygame.mouse.get_pressed()[0]:
                    self.selected_item = self.inventory[i]

            if self.selected_item is not None and self.inventory[i] is not None:
                if self.inventory[i].name == self.selected_item.name:
                    color = (color[0], 255, color[2])

            pygame.draw.rect(item_surface, color, rect)

            if self.inventory[i] is not None:
                img = pygame.transform.scale(self.inventory[i].img, (step, step))
                item_surface.blit(img, (start_x, start_y))

            start_y = step

            if self.inventory[i] is not None:
                text_box = TextBox(
                    "res/uwu-font.ttf", font_size=step - 4, font_color=INVENTORY_COLOR
                )
                text_box.set_text(str(self.inventory.get_count(self.inventory[i])))
                # img = pygame.transform.scale(self.inventory[i].img, (step, step))
                item_surface.blit(text_box._rendered_text, (start_x + 2, start_y + 2))

        for x in range(step, grid_width, step):
            for y in range(step, 2 * step, step):
                pygame.draw.line(item_surface, BORDER_COLOR, (x, 0), (x, step), width=3)
                pygame.draw.line(
                    item_surface, BORDER_COLOR, (0, y), (grid_width, y), width=3
                )

        weapon_surface = self.get_weapon_as_surface()
        weapon_surface = pygame.transform.scale(
            weapon_surface, (grid_surface.get_width(), grid_surface.get_height())
        )
        weapon_surface.set_alpha(64)
        grid_surface.blit(weapon_surface, (0, 0))

        for item, spot in self.items:
            start = spot * step
            img = pygame.transform.scale(item.img, Vec2(item.shape) * step)
            grid_surface.blit(img, start)

        surface.blit(item_surface, item_offset)
        surface.blit(grid_surface, offset)

        if self.selected_item:
            shape = Vec2(self.selected_item.shape) * step
            s = pygame.Surface(shape)
            s.set_alpha(128)
            s.fill((0, 255, 0))
            surface.blit(s, mouse_position)

        # surface.blit(pygame.transform.scale_by(self.get_weapon_as_surface(), 10), (0, 0))
        self.surface = surface

    def draw(self, camera: Camera) -> None:
        if not self.visible:
            return

        if self.surface is None:
            return

        camera.blit(
            surface=self.surface,
            offset=(-camera.viewport.get_width() / 2, -camera.viewport.height / 2),
        )
