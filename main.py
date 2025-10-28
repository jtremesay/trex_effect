# ANTI-CAPITALIST SOFTWARE LICENSE (v 1.4)
#
# Copyright © 2025 Jonathan Tremesaygues
#
# This is anti-capitalist software, released for free use by individuals and
# organizations that do not operate by capitalist principles.
#
# Permission is hereby granted, free of charge, to any person or organization
# (the "User") obtaining a copy of this software and associated documentation
# files (the "Software"), to use, copy, modify, merge, distribute, and/or sell
# copies of the Software, subject to the following conditions:
#
# 1. The above copyright notice and this permission notice shall be included in
#    all copies or modified versions of the Software.
#
# 2. The User is one of the following:
#   a. An individual person, laboring for themselves
#   b. A non-profit organization
#   c. An educational institution
#   d. An organization that seeks shared profit for all of its members, and
#      allows non-members to set the cost of their labor
#
# 3. If the User is an organization with owners, then all owners are workers and
#    all workers are owners with equal equity and/or equal vote.
#
# 4. If the User is an organization, then the User is not law enforcement or
#     military, or working for or under either.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT EXPRESS OR IMPLIED WARRANTY OF ANY
# KIND, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
# FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF
# CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

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
