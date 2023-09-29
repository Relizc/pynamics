import pygame

from .dimensions import Dimension, Dimension2d

class GameContext:

    def __init__(self, size_x: int, size_y: int):
        self.main = pygame.display.set_mode((size_x, size_y))

    def from_dim(scale: Dimension):
        return GameContext(scale.x, scale.y)

    def set_title(self, caption: str):
        pygame.display.set_caption(caption)