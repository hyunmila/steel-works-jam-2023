import pygame
from typing import List, Tuple, Optional
from .item import Item, ItemType
from .inventory import Inventory
from pygame.math import Vector2 as Vec2

class Weapon:
    GRID_WIDTH = 16
    GRID_HEIGHT = 8
    GRID = [[None for _ in range(8)] for _ in range(16)]

    def __init__(self):
        self.items: List[Tuple[Item, Vec2]] = []
        self.inventory = Inventory()
        self.selected_item: Optional[Item] = None

    def is_valid(self, spot, item):
        rect = pygame.Rect(spot, item.shape)

        for item, spot in self.items:
            rect2 = pygame.Rect(spot, item.shape)
            if rect.colliderect(rect2):
                return False
        return True

    def add_item(self, item):
        self.inventory.add_item(item)

    def put_item(self, spot: Vec2, item: Item):
        if self.is_valid(spot, item) and self.inventory.get_count(item) > 0:
            self.items.append((item, spot))
            self.inventory.remove_item(item)


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
        return False
    
    def process(self, mouse_position):
        BORDER_COLOR = (0, 0, 0)
        GRID_COLOR = (200, 200, 230)
        SELECTED_GRID_COLOR = (180, 180, 210)
        INVENTORY_COLOR = (150, 150, 180)
        SELECTED_INVENTORY_COLOR = (120, 120, 150)
        BACKGROUND_COLOR = (100, 100, 130)

        width, height = 1280, 720
        grid_width, grid_height = 960, 480
        offset = Vec2((width-grid_width)//2, (height-grid_height)//2)
        step = grid_height//self.GRID_HEIGHT
        offset += Vec2(0, -step*1.25)

        surface = pygame.Surface((width, height))
        surface.fill(BACKGROUND_COLOR)

        grid_surface = pygame.Surface((grid_width, grid_height))
        grid_surface.fill((0, 255, 0))

        grid_relative_mouse_position = mouse_position - offset
        for i in range(len(self.GRID)):
            for j in range(len(self.GRID[i])):
                start_x = i*step
                start_y = j*step

                rect = pygame.Rect(start_x, start_y, step, step)
                
                color = GRID_COLOR
                if rect.collidepoint(grid_relative_mouse_position):
                    color = SELECTED_GRID_COLOR

                    if pygame.mouse.get_pressed()[0] and self.selected_item:
                        self.put_item(Vec2(i, j), self.selected_item)
                
                pygame.draw.rect(grid_surface, color, rect)
                

        for x in range(step, grid_width, step):
            for y in range(step, grid_height, step):
                pygame.draw.line(grid_surface, BORDER_COLOR, (x, 0), (x, grid_height), width=1)
                pygame.draw.line(grid_surface, BORDER_COLOR, (0, y), (grid_width, y), width=1)

        item_surface = pygame.Surface((grid_width, 2*step))
        item_surface.fill((0, 0, 0))

        item_offset = Vec2(0, grid_height) + offset + Vec2(0, step/2)

        item_relative_mouse_position = mouse_position - item_offset
        for i in range(16):
            start_x = i*step
            start_y = 0 #j*step

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

        for x in range(step, grid_width, step):
            for y in range(step, 2*step, step):
                pygame.draw.line(item_surface, BORDER_COLOR, (x, 0), (x, 2*step), width=1)
                pygame.draw.line(item_surface, BORDER_COLOR, (0, y), (grid_width, y), width=1)

        for item, spot in self.items:
            start = spot*step
            img = pygame.transform.scale(item.img, Vec2(item.shape)*step)
            grid_surface.blit(img, start)

        surface.blit(item_surface, item_offset)
        surface.blit(grid_surface, offset)

        if self.selected_item:
            shape = Vec2(self.selected_item.shape)*step
            s = pygame.Surface(shape)
            s.set_alpha(128)
            s.fill((0, 255, 0)) 
            surface.blit(s, mouse_position)

        return surface
