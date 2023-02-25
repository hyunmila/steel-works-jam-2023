from typing import Tuple
import pygame

from core.color import Color
from core.input import Input


# Window handles pygame IO.
class Window:
    def __init__(self, title: str, size: Tuple[int, int], frame_rate: int = 60) -> None:
        pygame.init()
        pygame.display.set_caption(title)

        self._surface: pygame.Surface = pygame.display.set_mode(size, pygame.RESIZABLE)

        self._open: bool = True
        self._input = Input()
        self._clock = pygame.time.Clock()
        self.frame_rate = frame_rate
        self._delta: float = 0

    # Offset is in pixels.
    def blit(self, surface: pygame.Surface, offset: Tuple[int, int] = (0, 0)) -> None:
        self._surface.blit(surface, offset)

    def is_open(self) -> bool:
        return self._open

    def get_size(self) -> Tuple[int, int]:
        return self._surface.get_size()

    def get_ratio(self) -> float:
        size = self.get_size()
        return size[0] / size[1]

    def get_input(self) -> Input:
        return self._input

    def get_delta(self) -> float:
        return self._delta

    def process_events(self) -> None:
        self._delta = self._clock.tick(self.frame_rate) / 1000

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._open = False
            elif event.type == pygame.KEYDOWN:
                self._input._update_key_state(event.key, True)
            elif event.type == pygame.KEYUP:
                self._input._update_key_state(event.key, False)

        self._input._integrate_updates()

    def swap_buffers(self) -> None:
        pygame.display.flip()
        self._surface.fill(Color.BLACK)
