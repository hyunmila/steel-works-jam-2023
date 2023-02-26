import pygame

from core.window import Window


class Animation:
    def __init__(
        self,
        sheet: pygame.Surface,
        cols: int,
        rows: int = 1,
        frame_count: int = -1,
        frame_rate: float = 1,
    ) -> None:
        self.sheet = sheet
        self.cols = cols
        self.rows = rows
        if frame_count > 0:
            self.set_frame_count(frame_count)
        else:
            self._frame_count = self.cols * self.rows
        self._frame = 0
        self.frame_rate = frame_rate
        self._timer = 0

    def set_frame_count(self, frame_count: int) -> None:
        self._frame_count = min(frame_count, self.cols * self.rows)

    def get_frame_count(self) -> int:
        return self._frame_count

    def set_frame(self, frame: int) -> None:
        self._frame = frame % self._frame_count

    def get_frame(self) -> int:
        return self._frame

    def rasterize(self) -> pygame.Surface:
        frame_width = self.sheet.get_width() // self.cols
        frame_height = self.sheet.get_height() // self.rows

        row = self._frame // self.cols
        col = self._frame % self.cols

        return self.sheet.subsurface(
            (col * frame_width, row * frame_height, frame_width, frame_height)
        )

    def update(self, window: Window) -> None:
        self._timer += window.get_delta()
        if self._timer < 1 / self.frame_rate:
            return

        self._timer = 0

        self._frame += 1
        if self._frame >= self._frame_count:
            self._frame = 0

    def __hash__(self) -> int:
        return hash(id(self))
