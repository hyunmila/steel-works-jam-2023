def lerp(a, b, t):
    # return (t - 1) * a + (t) * b
    return a + t * (b - a)


class BBox:
    def __init__(self, x: float, y: float, w: float, h: float) -> None:
        self.x = x
        self.y = y
        self.w = w
        self.h = h
