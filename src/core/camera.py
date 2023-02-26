from typing import Tuple
import pygame
from core.viewport import Viewport


# Camera is responsible for offsetting the world appropriately
# so the chosen point is in the center of the screen.
class Camera:
    # Height is in units.
    def __init__(self, viewport: Viewport):
        self.viewport = viewport
        self.position: Tuple[float, float] = (0, 0)

    def blit(self, surface: pygame.Surface, offset: Tuple[float, float] = (0, 0)):
        viewport_size = (self.viewport.get_width(), self.viewport.get_height())

        ox = self.position[0] - viewport_size[0] / 2
        oy = self.position[1] - viewport_size[1] / 2

        self.viewport.blit(surface, (offset[0] - ox, offset[1] - oy))
