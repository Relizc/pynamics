import pygame
from .interface import PygameProObject

class Line:

    def __init__(self, text, color):
        self.text = text
        self.color = color

class Text(PygameProObject):

    def __init__(self, parent, lines=[], *args, **kwargs):
        PygameProObject.__init__(self, *args, **kwargs)
        self.parent = parent
        self.parent.text.append(self)

        self.styles["font-family"] = kwargs.get("font", "freesansbold.ttf")
        self.styles["font-size"] = kwargs.get("size", 16)
        self.styles["color"] = kwargs.get("color", (0, 0, 0))
        self.styles["background-color"] = kwargs.get("background-color", None)

        self.font = pygame.font.Font(self.styles["font-family"], self.styles["font-size"])
        self.lines = lines
        self.texts = []

        self.x = kwargs.get("x", 0)
        self.y = kwargs.get("y", 0)

        for i in self.lines:
            self.texts.append(self.font.render(i[0], True, i[1], self.styles["background-color"]))

    def str(text):
        al = []
        for i in text.split("\n"):
            al.append((i, (0, 0, 0)))
        return al

    def create(parent, lines):
        l = []
        for i in lines:
            if isinstance(i, Line):
                l.append((i.text, i.color))
            else:
                l.append(tuple(i))

    def update(self):
        y = self.y
        if self.enabled:
            for i in self.texts:
                r = i.get_rect()
                r.x = self.x
                r.y = y
                self.parent.main.blit(i, r)
                y += self.styles["font-size"]