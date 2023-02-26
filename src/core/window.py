from typing import Tuple
import pygame
import os

from core.color import Color
from core.input import Input


# Window handles pygame IO.
class Window:
    def __init__(self, title: str, size: Tuple[int, int], frame_rate: int = 60) -> None:
        os.environ[
            "SDL_VIDEO_CENTERED"
        ] = "1"  # centers the main window after the menu DO NOT DELETE PLS otherwise it won't work on Windows :(

        pygame.init()
        pygame.mixer.init()
        pygame.mixer.set_num_channels(100)

        pygame.display.set_caption(title)

        self._surface: pygame.Surface = pygame.display.set_mode(size, pygame.RESIZABLE)

        self._open: bool = True
        self._input = Input()
        self._clock = pygame.time.Clock()
        self.frame_rate = frame_rate
        self._delta: float = 0
        self.time_scale = 1
        self._just_resized = False

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
        return self._delta * self.time_scale

    def just_resized(self) -> bool:
        return self._just_resized

    def process_events(self) -> None:
        self._delta = self._clock.tick(self.frame_rate) / 1000
        self._just_resized = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._open = False
            elif event.type == pygame.KEYDOWN:
                self._input._update_key_state(event.key, True)
            elif event.type == pygame.KEYUP:
                self._input._update_key_state(event.key, False)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self._input._update_key_state(event.button, True)
            elif event.type == pygame.MOUSEBUTTONUP:
                self._input._update_key_state(event.button, False)
            elif event.type == pygame.WINDOWRESIZED:
                self._just_resized = True

        self._input._integrate_updates()

    def swap_buffers(self) -> None:
        pygame.display.flip()
        self._surface.fill(Color.BLACK)
