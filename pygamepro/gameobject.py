from .interface import PygameProObject
from .dimensions import Dimension2d, Dimension
import pygame

class GameObject(PygameProObject):

    def __init__(self):
        pass

class GameBody(GameObject, pygame.sprite.Sprite):

    def __init__(self, rect):
        pg.sprite.Sprite.__init__(self)
        self.rect = rect

    def from_fill(size, offset: Dimension):

        size = None
        offset = offset

        if isinstance(size, tuple):
            size = Dimension2d(0, size[0], 0, size[1])
        elif isinstance(size, Dimension):
            size = Dimension2d(0, size.x, 0, size.y)
        elif isinstance(size, Dimension2d):
            size = size

        return GameBody()
