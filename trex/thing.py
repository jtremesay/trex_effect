from pygame import Surface


class Thing:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def update(self, delta_time: float):
        pass

    def draw(self, surface: Surface):
        pass
