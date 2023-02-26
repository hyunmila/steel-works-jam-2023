from typing import Tuple
import pygame
from core.window import Window


# Viewport is responsible for scaling the game world to fit the window.
class Viewport:
    def __init__(self, window: Window, width: float, height: float):
        self.window = window
        self.width = width
        self.height = height

    def get_width(self) -> float:
        width = self.height * self.window.get_ratio()
        return min(width, self.width)

    def get_height(self) -> float:
        height = self.width / self.window.get_ratio()
        return min(height, self.height)

    def get_size(self) -> Tuple[float, float]:
        return (self.get_width(), self.get_height())

    # Offset is in pixels.
    def blit(
        self, surface: pygame.Surface, offset: Tuple[float, float] = (0, 0)
    ) -> None:
        window_size: int = self.window.get_size()

        w_scale: float = window_size[0] / self.width
        h_scale: float = window_size[1] / self.height

        scale = max(w_scale, h_scale)

        scaled_surface = pygame.transform.scale(
            surface,
            (
                surface.get_width() * scale,
                surface.get_height() * scale,
            ),
        )

        self.window.blit(
            scaled_surface,
            (offset[0] * scale, offset[1] * scale),
        )
