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
