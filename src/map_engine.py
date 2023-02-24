from typing import Tuple
import pygame
import math

import sys

if sys.version_info >= (3, 11):
    from typing import Self
else:
    from typing_extensions import Self


class BBox:
    def __init__(self, x: float, y: float, w: float, h: float) -> None:
        self.x = x
        self.y = y
        self.w = w
        self.h = h


class Tile:
    def __init__(self, img_path: str, collision: bool) -> None:
        try:
            self.img = pygame.image.load(img_path)
        except:
            self.img = None
        self.collision = collision

    def _resize(self, size: int) -> None:
        if self.img is not None:
            self.img = pygame.transform.scale(self.img, (size, size))


class MapEngine:
    def __init__(self, tiles: dict, tile_size: int = 16, tile_scale: int = 16) -> None:
        self.tiles = tiles
        self.tile_size = tile_size
        self.map_width = 0
        self.map_height = 0
        self.map: list(Tile) = []

        # Scale all tiles to desired resolution
        for tile in self.tiles.values():
            tile._resize(tile_size)

    def load_from_file(self, path: str) -> None:
        img = pygame.image.load(path)

        self.map_width = img.get_width()
        self.map_height = img.get_height()
        self.map = []

        for x in range(self.map_width):
            for y in range(self.map_height):
                color = img.get_at((x, y))
                color = (color.r, color.g, color.b)
                if color not in self.tiles:
                    raise ValueError(
                        f"Color {color} at pixel ({x}, {y}) is not a valid tile."
                    )

                tile = self.tiles[color]
                self.map.append(tile)

    def get_tile_size(self) -> int:
        return self.tile_size

    def get_tile_scale(self) -> int:
        return self.tile_scale

    def get_map_width(self) -> int:
        return self.map_width

    def get_map_height(self) -> int:
        return self.map_height

    def get_tile(self, x: int, y: int) -> Tile:
        return self.map[x * self.map_height + y]

    def draw(self, screen: pygame.Surface, offset: Tuple[int, int] = (0, 0)) -> None:
        for x in range(self.map_width):
            for y in range(self.map_height):
                tile = self.map[x * self.map_height + y]

                # Draw the tile onto the screen
                if tile.img is not None:
                    screen.blit(
                        tile.img,
                        (
                            x * self.tile_size + offset[0],
                            y * self.tile_size + offset[1],
                        ),
                    )

    # rect = (top-left XY, width and height)
    def rect_collision(self, bbox: BBox) -> bool:
        for x in range(math.floor(bbox.x), math.floor(bbox.x + bbox.w) + 1):
            for y in range(math.floor(bbox.y), math.floor(bbox.y + bbox.h) + 1):
                if x < 0 or y < 0 or x >= self.map_width or y >= self.map_height:
                    return True

                tile = self.map[x * self.map_height + y]
                if tile.collision:
                    return True

        return False
