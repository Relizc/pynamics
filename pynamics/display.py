import tkinter as tk
from .gamemanager import GameManager
from .dimensions import Dimension, Dimension2d
from .interface import PyNamical
from .gameobject import GameObject
from tkinter import NW

import random


class ViewPort(PyNamical):

    def __init__(self, parent, position: Dimension = Dimension(0, 0)):
        self.position = position

    def offset(self, dimension: Dimension):
        return dimension.add(self.position)


class ProjectWindow(PyNamical):

    def __init__(self, parent: GameManager, size: Dimension = Dimension(500, 500), title: str = "ViewPort Frame"):
        super().__init__(parent)
        self.parent.window = self

        self.size = size

        self._tk = tk.Tk()
        self._tk.geometry(f"{size.x}x{size.y}")
        self._tk.resizable(False, False)
        self._tk.title(title)
        self.surface = tk.Canvas(self._tk, width=size.x, height=size.y, bg="white", highlightthickness=0)
        self.surface.pack()

    def blit(self):
        #self.surface.delete("all")
        for i in self.parent.objects:
            if isinstance(i, GameObject):

                #print("check")

                moved = i.position != i.last_position
                if moved:
                    
                    #print(i, i.position, i.last_position)
                    
                    self.surface.delete(f"ID{i.blit_id}")
                    

                    g = random.randint(-2**64, 2**64)

                    if i.content is not None:
                        self.surface.create_image(i.position.x, i.position.y, anchor=NW, image=i.content, tags=f"ID{g}")

                    elif len(i.points) > 0:
                        for j in i.points:
                            pos1 = j[0]
                            pos2 = j[1]
                            self.surface.create_line(pos1[0] + i.position.x,pos1[1] + i.position.y,pos2[0] + i.position.x,pos2[1]+ i.position.y, tags=f"ID{g}")
                    
                    i.last_position = Dimension(i.position.x, i.position.y)
                    i.blit_id = g
                    print(i.blit_id)

    def _close_parent_close(self):
        self.parent.terminated = True
        if self.parent.debug != None:
            self.parent.debug.tk.destroy()
        self._tk.destroy()

    def start(self):
        self._tk.protocol("WM_DELETE_WINDOW", self._close_parent_close)
        self._tk.mainloop()
