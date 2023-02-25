from typing import Tuple
import pygame
from core.window import Window


# Viewport is responsible for scaling the game world to fit the window.
class Viewport:
    def __init__(self, window: Window, height: float):
        self.window = window
        self.height = height

    def get_width(self) -> float:
        return self.window.get_ratio() * self.height

    def get_size(self) -> Tuple[float, float]:
        return (self.get_width(), self.height)

    # Offset is in pixels.
    def blit(
        self, surface: pygame.Surface, offset: Tuple[float, float] = (0, 0)
    ) -> None:
        window_height: int = self.window.get_size()[1]
        window_scale: float = window_height / self.height

        scaled_surface = pygame.transform.scale(
            surface,
            (
                surface.get_width() * window_scale,
                surface.get_height() * window_scale,
            ),
        )

        self.window.blit(
            scaled_surface,
            (offset[0] * window_scale, offset[1] * window_scale),
        )
