import tkinter as tk

from .dimensions import Dimension, Dimension2d
from .interface import PyNamical

class ViewPort(PyNamical):

    def __init__(self, parent, position: Dimension = Dimension(0, 0)):
        self.position = position

    def offset(self, dimension: Dimension):
        return dimension.add(self.position)



class ProjectWindow(PyNamical):

    def __init__(self, parent, size: Dimension = Dimension(500, 500)):
        super().__init__(parent)
        self.parent.window = self

        self.size = size

        self._tk = tk.Tk()
        self._tk.geometry(f"{size.x}x{size.y}")
        self._tk.resizable(False, False)
        self.surface = tk.Canvas(self._tk, width=size.x, height=size.y, bg="white", highlightthickness=0)
        self.surface.pack()

    def _close_parent_close(self):
        self.parent.terminated = True
        self._tk.destroy()

    def start(self):
        self._tk.protocol("WM_DELETE_WINDOW", self._close_parent_close)
        self._tk.mainloop()

