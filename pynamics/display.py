import tkinter as tk
from .gamemanager import GameManager
from .dimensions import Dimension, Dimension2d
from .interface import PyNamical
from .gameobject import GameObject
from tkinter import NW


class ViewPort(PyNamical):

    def __init__(self, parent, position: Dimension = Dimension(0, 0)):
        self.position = position

    def offset(self, dimension: Dimension):
        return dimension.add(self.position)


class ProjectWindow(PyNamical):

    def __init__(self, parent: GameManager, size: Dimension = Dimension(500, 500)):
        super().__init__(parent)
        self.parent.window = self

        self.size = size

        self._tk = tk.Tk()
        self._tk.geometry(f"{size.x}x{size.y}")
        self._tk.resizable(False, False)
        self.surface = tk.Canvas(self._tk, width=size.x, height=size.y, bg="white", highlightthickness=0)
        self.surface.pack()

    def blit(self):
        self.surface.delete("all")
        for i in self.parent.objects:
            if isinstance(i,GameObject):
                #print(i.position.x,i.position.y)
                if i.content is not None:
                    self.surface.create_image(i.position.x, i.position.y, anchor=NW, image=i.content)
                elif i.content is None:
                    self.surface.create_line(i.topleft.x, i.topleft.y, i.topright.x, i.topright.y)
                    self.surface.create_line(i.topleft.x, i.topleft.y, i.bottomleft.x, i.bottomleft.y)
                    self.surface.create_line(i.topright.x, i.topright.y, i.bottomright.x, i.bottomright.y)
                    self.surface.create_line(i.bottomleft.x, i.bottomleft.y, i.bottomright.x + 1, i.bottomright.y)

    def _close_parent_close(self):
        self.parent.terminated = True
        self._tk.destroy()

    def start(self):
        self._tk.protocol("WM_DELETE_WINDOW", self._close_parent_close)
        self._tk.mainloop()
