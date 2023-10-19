import pygame
from .interface import PygameProObject

class Text(PygameProObject):

    def __init__(self, parent, text, *args, **kwargs):
        PygameProObject.__init__(self, *args, **kwargs)
        self.parent = parent
        self.parent.text.append(self)
        self.text = text

        self.styles["font-family"] = kwargs.get("font", "freesansbold.ttf")
        self.styles["font-size"] = kwargs.get("size", 16)
        self.styles["color"] = kwargs.get("color", (0, 0, 0))
        self.styles["background-color"] = kwargs.get("background-color", None)

        self.font = pygame.font.Font(self.styles["font-family"], self.styles["font-size"])
        self.text = self.font.render(self.text, True, self.styles["color"], self.styles["background-color"])

    def update(self):
        self.parent.main.blit(self.text, self.text.get_rect())