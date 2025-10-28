import pygame
from pygame import Color

from trex.colors import WHITE
from trex.engine import Engine
from trex.scene import Scene
from trex.thing import Thing

WIDTH = 1024
HEIGHT = WIDTH


class Rect(Thing):
    def __init__(
        self,
        x: float,
        y: float,
        width: float,
        height: float,
        color: Color,
    ):
        super().__init__(x, y)
        self.width = width
        self.height = height
        self.color = color

    def draw(self, surface: pygame.Surface):
        pygame.draw.rect(
            surface, self.color, pygame.Rect(self.x, self.y, self.width, self.height)
        )


class Scene1(Scene):
    def __init__(self):
        super().__init__()
        red_rect = Rect(100, 100, 200, 150, WHITE)
        blue_rect = Rect(400, 300, 250, 100, WHITE)
        self.things.append(red_rect)
        self.things.append(blue_rect)


def main():
    pygame.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    engine = Engine()
    engine.scene_manager.push_scene(Scene1())
    engine.run(screen)

    pygame.quit()


if __name__ == "__main__":
    main()
