from enum import IntEnum
from dataclasses import dataclass
from typing import Tuple
import pygame

class ItemType(IntEnum):
    CONNECT = 1,
    AMMO = 2,
    GUN = 3

@dataclass
class Item:
    img: pygame.Surface
    name: str
    item_type: ItemType = ItemType.GUN
    weight: float = 1.0
    shape: Tuple[int, int] = (1, 1)
    ammo_type: str = ""
    color: Tuple[float, float, float] = (0, 0, 0)

