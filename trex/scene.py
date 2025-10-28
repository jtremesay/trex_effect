from pygame import Surface

from .thing import Thing


class Scene:
    def __init__(self):
        self.things: list[Thing] = []

    def update(self, delta_time: float):
        for thing in self.things:
            thing.update(delta_time)

    def draw(self, surface: Surface):
        for thing in self.things:
            thing.draw(surface)
