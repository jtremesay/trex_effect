from pygame import Surface

from .scene import Scene


class SceneManager:
    def __init__(self):
        self.scenes: list[
            Scene
        ] = []  # Stack of scene. The last one is the current scene.

    def push_scene(self, scene: Scene):
        self.scenes.append(scene)

    def pop_scene(self):
        if self.scenes:
            self.scenes.pop()

    def replace_scene(self, scene: Scene):
        if self.scenes:
            self.scenes.pop()
        self.scenes.append(scene)

    def update(self, delta_time: float):
        if self.scenes:
            self.scenes[-1].update(delta_time)

    def draw(self, surface: Surface):
        if self.scenes:
            self.scenes[-1].draw(surface)
