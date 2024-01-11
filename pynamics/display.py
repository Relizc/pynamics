import tkinter as tk
from .gamemanager import GameManager
from .dimensions import Dimension, Dimension2d
from .interface import PyNamical
from .gameobject import GameObject, Text
from tkinter import NW
import time

import random


class ViewPort(PyNamical):

    def __init__(self, parent, position: Dimension = Dimension(0, 0)):
        parent.viewport = self
        self.position = position
        self.size = parent.size

    def offset(self, dimension: Dimension):
        return dimension.add(self.position)
    
    def crop_add(self):
        return self.size.add_dim(self.position)
    
    def crop_sub(self):
        return self.size.sub
    
    def shift(self, other: Dimension):
        return other.add_dim(self.position)


class ProjectWindow(PyNamical):

    def __init__(self, parent: GameManager, size: Dimension = Dimension(1000, 1000), title: str = "ViewPort Frame"):
        super().__init__(parent)
        self.parent.window = self

        self.size = size

        self.viewport = ViewPort(self, position = Dimension(0, 0))
        self.cropped_viewport = self.viewport.crop_add()
        self._tk = tk.Tk()
        self._tk.geometry(f"{size.x}x{size.y}")
        self._tk.resizable(False, False)
        self._tk.title(title)
        self.surface = tk.Canvas(self._tk, width=size.x, height=size.y, bg="white", highlightthickness=0)
        self.surface.pack()

        self.force_update = 0

    def blit(self):
        #self.surface.delete("all")
        
        for i in self.parent.ghosts:
            self.surface.delete(f"ID{i.blit_id}")
        for i in self.parent.objects:
            if isinstance(i, GameObject):

                #print("check")

                #if i.topleft < self.cropped_viewport.x

                #print()

                a = time.time()

                moved = i.position != i.last_position

                if (moved and not i.hidden) or i.force_update:
                    
                    #print(i, i.position, i.last_position)

                    if i.clear_blit:
                        self.surface.delete(f"ID{i.blit_id}")
                    #print(f"delete: {(time.time() - a) * 1000}")
                    a = time.time()

                    g = random.randint(-2**64, 2**64)

                    cam = self.viewport.shift(i.position)
                    
                    # If its a thing with ass image. why would u do it like this but not making another image class
                    if i.content is not None:
                        self.surface.create_image(cam.x, cam.y, anchor=NW, image=i.content, tags=f"ID{g}")
                        #print(f"point creation: {(time.time() - a) * 1000}")
                        a = time.time()

                    # If its text
                    elif isinstance(i, Text):
                        self.surface.create_text(cam.x, cam.y, text=i.text, fill=i.font.color, font=str(i.font), anchor=NW, tags=f"ID{g}")

                    # If its a regular gameobject
                    elif len(i.points) > 0:
                        for j in i.points:
                            pos1 = j[0]
                            pos2 = j[1]
                            self.surface.create_line(pos1[0] + cam.x,pos1[1] + cam.y,pos2[0] + cam.x,pos2[1]+ cam.y, tags=f"ID{g}")

                        #print(f"multipoint creation: {(time.time() - a) * 1000}")
                        a = time.time()
                    
                    i.last_position = Dimension(i.position.x, i.position.y)
                    i.blit_id = g

                    #print(f"update: {(time.time() - a) * 1000}")
                    a = time.time()

        if self.force_update > 0:
            self.force_update -= 1


    def _close_parent_close(self):
        self.parent.terminated = True
        if self.parent.debug != None:
            self.parent.debug.tk.destroy()
        self._tk.destroy()

    def start(self):
        self._tk.protocol("WM_DELETE_WINDOW", self._close_parent_close)
        self._tk.mainloop()
