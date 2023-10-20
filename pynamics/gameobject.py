from .interface import PyNamical
from .dimensions import Dimension
from PIL import ImageTk,Image

class GameObject(PyNamical):
    def __init__(self, parent: PyNamical, x: float, y: float, width: float, height: float, contents: str=None):
        """
        :param x: The position of the GameObject, on X-Axis
        :param y: The position of the GameObject, on Y-Axis
        :param width: The width of the GameObject
        :param height: The height of the GameObject
        """
        super().__init__(parent)
        self.position = Dimension(x, y)
        self.size = Dimension(width, height)
        self.content = contents
        self.absolute = Dimension(x, y)

        self.parent.add_object(self)

        if self.content is not None:
            self.content = ImageTk.PhotoImage(Image.open(contents))

    @property
    def topleft(self):
        return self.position

    @property
    def topright(self):
        return self.position.add(self.size.x, 0)

    @property
    def bottomleft(self):
        return self.position.add(0, self.size.y)

    @property
    def bottomright(self):
        return self.position.add_dim(self.size)

    @property
    def center(self):
        return self.position.add(self.size.x / 2, self.size.y / 2)

