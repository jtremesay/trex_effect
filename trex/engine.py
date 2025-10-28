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
from pygame import Surface

from .colors import BLACK
from .scene_manager import SceneManager


class Engine:
    def __init__(self):
        self.scene_manager = SceneManager()

    def update(self, delta_time: float):
        self.scene_manager.update(delta_time)

    def draw(self, surface: Surface):
        surface.fill(BLACK)  # Clear screen with black
        self.scene_manager.draw(surface)

    def run(self, surface: Surface):
        clock = pygame.time.Clock()
        running = True
        while running:
            # poll for events
            # pygame.QUIT event means the user clicked X to close your window
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (
                    event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
                ):
                    running = False

            self.update(1 / 60)
            self.draw(surface)

            pygame.display.flip()
            clock.tick(60)  # limits FPS to 60
