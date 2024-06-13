import os
import threading
import time

import numpy as np
import copy
from pynamics_legacy.events import EventPriority, EventType, KeyEvaulator
from pynamics_legacy.interface import PyNamical, network_transferrable
from pynamics_legacy.dimensions import Dimension, Vector2d, Color
from pynamics_legacy.styling import color_alias
from pynamics_legacy.metadata import PyNamicsTexture
from pynamics_legacy.logger import Logger
import math
import cmath
import tkinter as tk
import ctypes

from PIL import Image as ImageUtils
import numpy as np


import random

class LimitedArray():
    def __init__(self, size: int, initialArray=[]):
        self.size = size
        if len(initialArray) > self.size:
            raise IndexError("The initial array exceeds the alloted size.")
        else:
            self.arr = initialArray
    def push_add(self,element):
        self.arr.append(element)
        if len(self.arr) > self.size:
            self.arr.pop(0)
    def push_extend(self,extendings:list):
        for i in extendings:
            self.push_add(i)


class Point(Dimension):
    pass

    # Given three collinear points p, q, r, the function checks if


def socket_whitelisted_attributes(*args, **kwargs):
    def add_fields(obj):
        obj.P_whitelisted = args
        return obj

    return add_fields

# point q lies on line segment 'pr'
def onSegment(p, q, r):
    if ((q.x <= max(p.x, r.x)) and (q.x >= min(p.x, r.x)) and
            (q.y <= max(p.y, r.y)) and (q.y >= min(p.y, r.y))):
        return True
    return False


def orientation(p, q, r):
    # to find the orientation of an ordered triplet (p,q,r)
    # function returns the following values:
    # 0 : Collinear points
    # 1 : Clockwise points
    # 2 : Counterclockwise

    # See https://www.geeksforgeeks.org/orientation-3-ordered-points/amp/
    # for details of below formula.

    val = (float(q.y - p.y) * (r.x - q.x)) - (float(q.x - p.x) * (r.y - q.y))
    if (val > 0):

        # Clockwise orientation
        return 1
    elif (val < 0):

        # Counterclockwise orientation
        return 2
    else:

        # Collinear orientation
        return 0


# The main function that returns true if
# the line segment 'p1q1' and 'p2q2' intersect.
def doIntersect(p1, q1, p2, q2):
    # Find the 4 orientations required for
    # the general and special cases
    o1 = orientation(p1, q1, p2)
    o2 = orientation(p1, q1, q2)
    o3 = orientation(p2, q2, p1)
    o4 = orientation(p2, q2, q1)

    # General case
    if ((o1 != o2) and (o3 != o4)):
        return True

    # Special Cases

    # p1 , q1 and p2 are collinear and p2 lies on segment p1q1
    if ((o1 == 0) and onSegment(p1, p2, q1)):
        return True

    # p1 , q1 and q2 are collinear and q2 lies on segment p1q1
    if ((o2 == 0) and onSegment(p1, q2, q1)):
        return True

    # p2 , q2 and p1 are collinear and p1 lies on segment p2q2
    if ((o3 == 0) and onSegment(p2, p1, q2)):
        return True

    # p2 , q2 and q1 are collinear and q1 lies on segment p2q2
    if ((o4 == 0) and onSegment(p2, q1, q2)):
        return True

    # If none of the cases
    return False

@socket_whitelisted_attributes("position", "velocity", "hidden")
@network_transferrable
class GameObject(PyNamical):

    def __init__(self, parent: PyNamical, x: float = 0, y: float = 0, width: float = 10, height: float = 10, contents: str = None,
                 rotation = 0,
                 from_points: tuple = None,
                 clear_blit: bool = True,
                 anchor: str = "nw",
                 no_display=False,
                 zindex=1,
                 color: str = "white",
                 destroy_outside_boundary: bool = False):
        """
        :param x: The position of the GameObject, on X-Axis
        :param y: The position of the GameObject, on Y-Axis
        :param width: The width of the GameObject
        :param height: The height of the GameObject
        """
        super().__init__(parent)

        self.position = Dimension(x, y)
        self.this_position = Dimension(x, y)

        self.events[EventType.ONCLICK] = []

        self.this_display_position = Dimension(self.this_position.x, self.position.y)
        self.last_display_position = None
        self.size = Dimension(width, height)
        self.destroy_outside_boundary = destroy_outside_boundary
        self.bugid = 0
        self.content = None
        self.hidden = no_display
        self.absolute = Dimension(x, y)
        self.blit_id = None
        self.force_update = 0
        self.start_debug_highlight_tracking = False
        self.rotation = rotation
        self.last_display_rotation = None
        self.this_display_position = rotation
        self.color = color_alias(color)
        self.points = [
            ((0, 0), (0, self.size.y)),
            ((0, self.size.y), (self.size.x, self.size.y)),
            ((self.size.x, self.size.y), (self.size.x, 0)),
            ((self.size.x, 0), (0, 0))
        ]
        self.clear_blit = clear_blit
        self.zindex = zindex
        if from_points is not None:
            self.points = []
            for i in from_points:
                self.points.append(i)
        self.id = id(self)

        self.parent.add_object(self)

        self.anchor = anchor

        self._debughighlight = None # TKCanvas Support
        

    def delete(self):
        if isinstance(self.parent.objects, set):
            try:
                self.parent.remove_object(self)
                self.parent.displayorder.remove(self)
                #self.parent.window.remove(self)
                self.unbind()
            except KeyError as e:
                #Logger.warn(f"Attempting to remove {self} which does not have any active parents or hooked GameManager. Delete operation ignored")
                pass
            
            del self
    

    def __repr__(self):
        return f"GameObject()"

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

    @property
    def x(self):
        return self.position.x

    @property
    def y(self):
        return self.position.y

    @x.setter
    def x(self, new_x):
        self.position.x = new_x

    @y.setter
    def y(self, new_x):
        self.position.y = new_x

    def hide(self):
        self.hidden = True
        self.parent.frame()

    def unhide(self):
        self.hidden = False
        self.forcedisplay = True
        self.parent.frame()
        self.forcedisplay = False

    def _debug_blit_once(self):
        self.parent.delete_draws(f"DEBUG@{self._debughighlight}")
        self._debughighlight = random.randint(-2**64, 2**64)
        self.parent.create_rectangle(self.position.x, self.position.y, self.position.x + self.size.x, self.position.y + self.size.y,
                                     outline="green",
                                     width=2,
                                     tags=f"DEBUG@{self._debughighlight}")

    def debug_highlight(self):
        self.start_debug_highlight_tracking = True

    def debug_unhighlight(self):
        self.start_debug_highlight_tracking = False

    def update(self):
        pass

    def attach_update_thread(self):
        PyNamical.MAIN_GAMEMANAGER.attach_update_thread(self)


IMAGETEXTURE_TEXTURE_CACHE = {}
IMAGETEXTURE_PIL_CACHE = {}

class FrameArray:

    def __init__(self, frames=[]):
        self.frames = frames

    def __getitem__(self, item):
        return self.frames[item]

    def add(self, points):
        self.frames.append(points)

def STR_HASH_UINT32(inp: str):
    hash = 0
    for ch in inp:
        hash = (hash * 0xf5fcaad4 ^ ord(ch) * 0x663e3d4e) & 0xFFFFFFFF
    return hash

class FramedTexture:

    def __init__(self, metadata=None, frame: str = None, path: str=None, crop_resize=False):

        self.framedata = {}
        self.crop_resize = crop_resize


        self.frame_array_index = 0

        if path is None:
            path = os.path.splitext(os.path.basename(metadata))[0]

        self.path = path

        if not metadata is None:
            self.load_meta(metadata)

        self.current = STR_HASH_UINT32(frame)


        self.image = ImageTexture(path, crop=self.get_active_texture()[self.frame_array_index], crop_resize=crop_resize)

        self.width = self.image.size[0]
        self.height = self.image.size[1]
        self.size = Dimension(self.width, self.height)





    @property
    def data(self):
        return self.image.data

    @property
    def effective(self):
        return self.get_active_texture()


    def __getitem__(self, item):
        if isinstance(item, str):
            item = STR_HASH_UINT32(item)
        return self.framedata[item]

    def get_texture(self, hash):
        return self.__getitem__(hash)

    def crop(self, texture_name_or_hash):
        if isinstance(texture_name_or_hash, str):
            texture_name_or_hash = STR_HASH_UINT32(texture_name_or_hash)
        self.current = texture_name_or_hash

    def get_active_texture(self) -> FrameArray:
        return self.framedata[self.current][self.frame_array_index]

    def load_meta(self, path):
        loader = PyNamicsTexture(open(path, "rb"))

        while loader.hasnext():
            fingerprint, coords = loader.frame()
            if not fingerprint in self.framedata:
                self.framedata[fingerprint] = FrameArray()
            self.framedata[fingerprint].add(coords)



class ImageTexture:

    def __init__(self, path, crop_resize=True, crop=None):
        self.path = path

        self.crop_resize = crop_resize



        if not self.path in IMAGETEXTURE_TEXTURE_CACHE:

            self.texture = ImageUtils.open(path)

            self.texture = self.texture.convert("RGBA")
            self.data = np.array(list(self.texture.getdata()), np.uint8)

            IMAGETEXTURE_TEXTURE_CACHE[self.path] = self.data
            IMAGETEXTURE_PIL_CACHE[self.path] = self.texture
        else:
            self.texture = IMAGETEXTURE_PIL_CACHE[self.path]
            self.data = IMAGETEXTURE_TEXTURE_CACHE[self.path]

        self.size = self.texture.size
        self.width = self.texture.width
        self.height = self.texture.height
        if crop is None:
            self.effective = (0, 0, self.width, self.height)
        else:
            self.effective = crop

    def resize(self, size, resample=None):
        pass

    def crop(self, a, b, x, y, crop_resize=None):
        if crop_resize is None:
            crop_resize = self.crop_resize
        self.effective = (a, b, x, y)
        self.crop_resize = crop_resize

    def color_content(self, x, y):
        x = min(x, self.texture.width - 1)
        y = min(y, self.texture.height - 1)
        return self.texture.getpixel((x, y))

class Image(GameObject):

    def __init__(self, parent: GameObject, x: float = 0, y: float = 0, width: float = -1, height: float = -1,
                 path: str = None,
                 ratio: int = 1,
                 texture: ImageTexture = None,
                 crop_resize: bool = False,
                 **kwargs):

        if texture is None:
            self.image = ImageTexture(path, crop_resize=crop_resize)
        else:
            self.image = texture



        super().__init__(parent, x, y, self.image.size[0], self.image.size[1], contents=None, **kwargs)

        w = self.image.width
        h = self.image.height

        if width != -1:
            w = width
        if height != -1:
            h = height

        self.image.resize((int(w * ratio), int(h * ratio)), resample=ImageUtils.BOX)

        self.size.x = int(w * ratio)
        self.size.y = int(h * ratio)

    @property
    def photosize(self):
        return self.size



    def __repr__(self):
        return f"Image(file={self.image.path})"

class StaticSprite(Image):

    def __repr__(self):
        return f"StaticSprite({self.position}, {self.size})"

class AnimatedSprite(GameObject):

    def __init__(self, parent: GameObject, x: float = 0, y: float = 0, width: float = -1, height: float = -1,
                 texture: FramedTexture=None,
                 path: str=None,
                 crop_resize: bool = False,
                 interval: float = -1,
                 **kwargs):

        self.interval = interval
        self.runtime = 0

        if texture is None:
            self.image = FramedTexture(path, crop_resize=crop_resize)
        else:
            self.image = texture

        self.photosize = Dimension(self.image.image.size[0], self.image.image.size[1])
        print(self.photosize)

        super().__init__(parent, x, y, width, height, contents=None, **kwargs)

        @PyNamical.MAIN_GAMEMANAGER.add_event_listener(event=EventType.TICK, name="ThreadedAnimateSpriteEvent")
        def do_later(e):

            self.runtime += 1

            if self.runtime == self.interval:

                if self.image.frame_array_index == len(self.image.framedata):
                    self.image.frame_array_index = 0
                else:
                    self.image.frame_array_index += 1
                self.runtime = 0

    @property
    def frame(self):
        return self.image.frame_array_index

    @frame.setter
    def frame(self, new):
        self.image.frame_array_index = new

    def set_frame(self, frame):
        self.image.frame_array_index = frame






    

class TextFont:

    def __init__(self, name: str = "Helvetica", size: int = 15, type: str = "", color: str = "black"):
        self.name = name
        self.size = size
        self.type = type
        self.color = color
    
    def __str__(self):
        return f"{self.name} {self.size} {self.type}"

class Text(GameObject):

    def __init__(self, parent, x = 0, y = 0, text = "Hello PyNamics World!", font=TextFont("Helvetica", 15), **kwargs):


        w, h = 10, 10
        super().__init__(parent, x, y, w, h)
        self.collision = False
        self.text = text
        self.font = font
        self.i=0

        #self.__setattr__ = self._silent__setattr__

    # This overrides the set attribute function when user does sometext.text = "anotherstring"
    # Therefore no need to do self.old == self.new
    def __setattr__(self, key, value):
        if key == "text":
            self.force_update += 1
        super(Text, self).__setattr__(key, value)

    def __repr__(self):
        return f"Text(\"{self.text}\")"

    def update(self):
        print(self.i)
        self.i+=1