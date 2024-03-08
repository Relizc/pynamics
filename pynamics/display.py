import tkinter as tk
from .gamemanager import GameManager
from .dimensions import Dimension, Dimension2d, Color
from .interface import PyNamical
from .logger import Logger
from .gameobject import GameObject, Particle, Text, TopViewPhysicsBody
from PIL import ImageTk
from tkinter import NW
import time

import random


class ViewPort(PyNamical):

    def __init__(self, parent, position: Dimension = Dimension(0, 0)):
        super().__init__(parent)
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


def rgb_to_hex(i):
    return f"#%02x%02x%02x" % (i.r, i.g, i.b)


class ProjectWindow(PyNamical):

    def __init__(self, parent: GameManager, size: Dimension = Dimension(1000, 1000), title: str = "ViewPort Frame",
                 color: Color = Color(255, 255, 255)):
        super().__init__(parent)
        self.parent.window = self

        self.size = size
        self.title = title

        self.viewport = ViewPort(self, position=Dimension(0, 0))
        self.cropped_viewport = self.viewport.crop_add()
        self._tk = tk.Tk()
        self._tk.geometry(f"{size.x}x{size.y}")
        self._tk.resizable(False, False)
        self._tk.title(title)
        self.color = color
        self._curcolor = Color(color.r, color.g, color.b)
        self.surface = tk.Canvas(self._tk, width=size.x, height=size.y, bg=str(color), highlightthickness=0)
        self.surface.pack()
        self.ignore_render = []

        self._blits = 0
        self._checks = 0

        self.force_update = 0

    def blit(self):
        try:
            self.real_blit()
        except Exception as e:
            Logger.print(f"Error in printing object: {e}", channel=4)

    def real_blit(self):
        # self.surface.delete("all")

        s = time.time()

        if self._curcolor != self.color:
            self._curcolor = Color(self.color.r, self.color.g, self.color.b)
            #print(self.color)
            self.surface.config(bg=str(self.color))


        for i in self.parent.ghosts:
            self.surface.delete(f"ID{i.blit_id}")


        for i in self.parent.objects:

            self._checks += 1

            if (i.position.x + i.size.x < -10 or i.position.y + i.size.y < -10) or (i.position.x > self.parent.dimensions.x + 10 or i.position.y > self.parent.dimensions.y + 10):
                self.surface.delete(f"ID{i.blit_id}")
                if i.destroy_outside_boundary:
                    i.delete()
                continue

            f = False
            for n in self.ignore_render:
                if isinstance(i, n):
                    f = True
            if f:
                continue


            if isinstance(i, GameObject):

                # print("check")

                # if i.topleft < self.cropped_viewport.x

                # print()

                a = time.time()

                moved = i.position != i.last_display_position
                rotated = i.rotation != i.last_display_rotation

                if ((moved or rotated) and not i.hidden) or i.force_update:

                    self._blits += 1

                    # print(i, i.position, i.last_position)

                    if i.clear_blit:
                        self.surface.delete(f"ID{i.blit_id}")

                    if i.start_debug_highlight_tracking:
                        i._debug_blit_once()

                    g = random.randint(-2 ** 64, 2 ** 64)

                    cam = self.viewport.shift(i.position)

                    # If its a thing with ass image. why would u do it like this but not making another image class
                    if i.content is not None:
                        if rotated:
                            i.content = ImageTk.PhotoImage(i.image.rotate(i.rotation))
                        self.surface.create_image((cam.x, cam.y), image=i.content, anchor=i.anchor, tags=f"ID{g}")

                    # If its text
                    elif isinstance(i, Text):
                        self.surface.create_text(i.x, i.y, text=i.text, fill=i.font.color, font=str(i.font), tags=f"ID{g}")

                    # If its a Particle
                    elif isinstance(i, Particle):
                        self.surface.create_oval(i.x - i.r, i.y - i.r, i.x + i.r, i.y + i.r, tags=f"ID{g}")

                    # If its a TopLevelWhateverBody
                    elif isinstance(i, TopViewPhysicsBody):
                        self.surface.create_rectangle(i.x, i.y, i.x + i.size.x, i.y + i.size.y, fill="white", outline="white", tags=f"ID{g}")

                    # If its a regular gameobject
                    elif len(i.points) > 0:
                        for j in i.points:
                            pos1 = j[0]
                            pos2 = j[1]
                            self.surface.create_line(pos1[0] + i.x, pos1[1] + i.y, pos2[0] + i.x, pos2[1] + i.y,
                                                     tags=f"ID{g}", fill=i.color)

                    i.last_display_position = Dimension(i.position.x, i.position.y)
                    i.last_display_rotation = i.rotation
                    i.blit_id = g


            if i.force_update > 0:
                i.force_update -= 1

        # TODO: lag
        # for i in self.parent.displayorder:
        #     self.surface.tag_raise(f"ID{i.blit_id}")


    def update(self):
        pass

    def remove(self, obj):
        self.surface.delete(f"ID{obj.blit_id}")

    def _close_parent_close(self):
        self.parent.terminated = True
        if self.parent.debug != None:
            self.parent.debug.tk.destroy()
        self._tk.destroy()

    def start(self):
        self._tk.protocol("WM_DELETE_WINDOW", self._close_parent_close)
        self._tk.mainloop()
