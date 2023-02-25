from typing import Tuple
import pygame
from core.camera import Camera


# Enables rendering of multiline text.
class TextBox:
    def __init__(
        self,
        font_path: str,
        font_size: int,
        font_color: Tuple[int, int, int],
        line_height_factor: float = 1.5,
    ) -> None:
        self._font = pygame.font.Font(font_path, font_size)
        self._font_color: Tuple[int, int, int] = font_color
        self._line_height: int = int(font_size * line_height_factor)
        self._rendered_text: pygame.Surface = None
        self.offset: Tuple[int, int] = (0, 0)

    def set_text(self, text: str):
        # Split the text block by newlines.
        lines = text.split("\n")
        if lines[-1] == "":
            lines.pop()

        # Render each line.
        rendered_lines = []
        max_width = 0
        for line in lines:
            rendered_lines.append(self._font.render(line, True, self._font_color))
            # Remember width of the longest line.
            max_width = max(max_width, rendered_lines[-1].get_width())

        # Create a surface to hold all the lines.
        self._rendered_text = pygame.Surface(
            (max_width, self._line_height * len(rendered_lines)), pygame.SRCALPHA, 32
        )

        # Blit each rendered line onto the surface.
        for i, rendered_line in enumerate(rendered_lines):
            self._rendered_text.blit(rendered_line, (0, i * self._line_height))

    def get_size(self) -> Tuple[int, int]:
        if self._rendered_text is None:
            return (0, 0)
        else:
            return self._rendered_text.get_size()

    def draw(self, camera: Camera):
        # Abort if there's noting to draw.
        if self._rendered_text is None:
            return

        camera.blit(self._rendered_text, self.offset)
