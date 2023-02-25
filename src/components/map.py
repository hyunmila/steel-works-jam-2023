from typing import Tuple
import pygame
import math

from core.camera import Camera
from core.math import BBox


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


class Map:
    def __init__(self, tiles: dict, tile_size: int = 16) -> None:
        self._tiles = tiles
        self._tile_size = tile_size
        self._map_size = (0, 0)
        self._map: list(Tile) = []

        # Scale all tiles to desired resolution
        for tile in self._tiles.values():
            tile._resize(tile_size)

    def load_from_file(self, path: str) -> None:
        img = pygame.image.load(path)

        self._map_size = img.get_size()
        self._map = []

        for x in range(self._map_size[0]):
            for y in range(self._map_size[1]):
                color = img.get_at((x, y))
                color = (color.r, color.g, color.b)
                if color not in self._tiles:
                    raise ValueError(
                        f"Color {color} at pixel ({x}, {y}) is not a valid tile."
                    )

                tile = self._tiles[color]
                self._map.append(tile)

    def get_tile_size(self) -> int:
        return self._tile_size

    def get_map_size(self) -> int:
        return self._map_size

    def get_tile(self, x: int, y: int) -> Tile:
        return self._map[x * self._map_size[1] + y]

    def draw(self, camera: Camera) -> None:
        for x in range(self._map_size[0]):
            for y in range(self._map_size[1]):
                tile = self._map[x * self._map_size[1] + y]

                # Draw the tile onto the screen
                if tile.img is not None:
                    camera.blit(
                        tile.img,
                        (x * self._tile_size, y * self._tile_size),
                    )

    def rect_collision(self, bbox: BBox) -> bool:
        for x in range(math.floor(bbox.x), math.floor(bbox.x + bbox.w) + 1):
            for y in range(math.floor(bbox.y), math.floor(bbox.y + bbox.h) + 1):
                if x < 0 or y < 0 or x >= self._map_size[0] or y >= self._map_size[1]:
                    return True

                tile = self._map[x * self._map_size[1] + y]
                if tile.collision:
                    return True

        return False