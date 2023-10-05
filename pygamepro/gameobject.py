from .interface import PygameProObject
from .dimensions import Dimension2d, Dimension
import pygame

class GameObject(PygameProObject):

    def __init__(self, *args, **kwargs):
        PygameProObject.__init__(self, *args, **kwargs)

class GameObjectCreator:

    children = []

    def render_all(self):
        for i in self.children:
            i.render()

    def create_rect(self, position, dimension: Dimension2d, *args, **kwargs):
        size_x = dimension.scale_x * self.size_x + dimension.offset_x
        size_y = dimension.scale_y * self.size_y + dimension.offset_y

        body = GameBody.from_fill((position.x, position.y), (size_x, size_y), self, *args, **kwargs)
        self.children.append(body)

        return body


class GameBody(GameObject, pygame.sprite.Sprite):

    def __init__(self, position, image, parent, *args, **kwargs):
        pygame.sprite.Sprite.__init__(self)
        GameObject.__init__(self, *args, **kwargs)
        self.parent = parent
        self.parent.sprites.add(self)
        self.image = image

        color = self.styles.get("background-color", None)
        c = (0, 0, 0)
        if isinstance(color, tuple):
            c = color
        elif isinstance(color, str):
            if color == "white":
                c = (255, 255, 255)
        self.image.fill(c)

        self.rect = self.image.get_rect()
        self.rect.x = position[0]
        self.rect.y = position[1]

        self.x = int(self.rect.x)
        self.y = int(self.rect.y)

        self.smoothblit = kwargs.get("smooth_blit", True)

        self._smoothframe_velocity = Dimension(0, 0)

        self.display_pos = Dimension(position[0], position[1])

    def update(self):
        self.rect.x = self.x
        self.rect.y = self.y
        self.display_pos.set(self.rect.x, self.rect.y)
        self.callEventListeners("update")

    def smooth_draw(self, context, surf):
        dx = self.x - self.rect.x
        dy = self.y - self.rect.y
        speed = max(context.fpt, 1)

        mx = dx / speed
        my = dy / speed
        #print(self.x, self.y, self.rect.x, self.rect.y, dx, dy, mx, my, speed)
        self.display_pos.add(mx, my)

        surf.blit(self.image, (int(round(self.display_pos.x, 0)), int(round(self.display_pos.y, 0))))

    def draw(self, context, surf):
        if self.smoothblit:
            self.smooth_draw(context, surf)
            return
        self.display_pos.set(self.x, self.y)
        surf.blit(self.image, (int(round(self.display_pos.x, 0)), int(round(self.display_pos.y, 0))))

    def set_position(self, dim: Dimension):
        self.x = dim.x
        self.y = dim.y

    def from_fill(pos, siz, parent, *args, **kwargs):

        # size = None
        # offset = offset

        # if isinstance(size, tuple):
        #     size = Dimension2d(0, size[0], 0, size[1])
        # elif isinstance(size, Dimension):
        #     size = Dimension2d(0, size.x, 0, size.y)
        # elif isinstance(size, Dimension2d):
        #     size = size

        return GameBody(pos, pygame.Surface(siz), parent, *args, **kwargs)
