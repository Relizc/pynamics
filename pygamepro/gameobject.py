from .interface import PygameProObject
from .dimensions import Dimension2d, Dimension
import pygame

class GameObject(PygameProObject):

    def __init__(self):
        PygameProObject.__init__(self)

class GameObjectCreator:

    children = []

    def render_all(self):
        for i in self.children:
            i.render()

    def create_rect(self, position, dimension: Dimension2d):
        size_x = dimension.scale_x * self.size_x + dimension.offset_x
        size_y = dimension.scale_y * self.size_y + dimension.offset_y

        body = GameBody.from_fill((position.x, position.y), (size_x, size_y), self)
        self.children.append(body)

        return body


class GameBody(GameObject, pygame.sprite.Sprite):

    def __init__(self, position, image, parent):
        pygame.sprite.Sprite.__init__(self)
        GameObject.__init__(self)
        self.parent = parent
        self.parent.sprites.add(self)
        self.image = image

        self.rect = self.image.get_rect()
        self.rect.x = position[0]
        self.rect.y = position[1]

        self.x = position[0]
        self.y = position[1]

    def update(self):
        self.callEventListeners("update")

    def from_fill(pos, siz, parent, *args, **kwargs):

        # size = None
        # offset = offset

        # if isinstance(size, tuple):
        #     size = Dimension2d(0, size[0], 0, size[1])
        # elif isinstance(size, Dimension):
        #     size = Dimension2d(0, size.x, 0, size.y)
        # elif isinstance(size, Dimension2d):
        #     size = size

        return GameBody(pos, pygame.Surface(siz), parent)
