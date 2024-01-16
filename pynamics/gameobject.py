import threading
import time

import numpy as np

from .events import EventPriority, EventType, KeyEvaulator
from .interface import PyNamical
from .dimensions import Dimension, Vector2d
import math
import cmath
import tkinter as tk
import ctypes
from PIL import Image as ImageUtils
from PIL import ImageTk


class Point(Dimension):
    pass

    # Given three collinear points p, q, r, the function checks if


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


class GameObject(PyNamical):
    def __init__(self, parent: PyNamical, x: float, y: float, width: float, height: float, contents: str = None,
                 from_points: tuple = None):
        """
        :param x: The position of the GameObject, on X-Axis
        :param y: The position of the GameObject, on Y-Axis
        :param width: The width of the GameObject
        :param height: The height of the GameObject
        """
        super().__init__(parent)

        self.position = Dimension(x, y)
        self.this_position = Dimension(x, y)
        self.last_position = None
        self.size = Dimension(width, height)
        self.content = contents
        self.hidden = False
        self.absolute = Dimension(x, y)
        self.blit_id = None
        self.force_update = 0
        self.points = [
            ((self.position.x, self.position.y), (self.position.x - self.size.x, self.position.y)),
            ((self.position.x - self.size.x, self.position.y),
             (self.position.x - self.size.x, self.position.y - self.size.y)),
            ((self.position.x - self.size.x, self.position.y - self.size.y),
             (self.position.x, self.position.y - self.size.y)),
            ((self.position.x, self.position.y - self.size.y), (self.position.x, self.position.y)),

        ]
        self.clear_blit = True
        if from_points is not None:
            self.points = []
            for i in from_points:
                self.points.append(i)
        self.id = id(self)

        self.parent.add_object(self)

    def delete(self):
        if isinstance(self.parent.objects, list):
            aid = self.parent.objectpointers[self.id]
            val = ctypes.cast(aid, ctypes.py_object).value
            self.parent.objects.remove(val)
            self.parent.ghosts.append(self)
            self.parent.frame()
            self.parent.ghosts.remove(self)
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

    def hide(self):
        self.hidden = True
        self.parent.frame()

    def unhide(self):
        self.hidden = False
        self.forcedisplay = True
        self.parent.frame()
        self.forcedisplay = False

    def debug_highlight(self):
        pass

    def debug_unhighlight(self):
        pass


class Image(GameObject):

    def __init__(self, parent: GameObject, x: float, y: float, width: float = -1, height: float = -1,
                 image_path: str = None,
                 resize_keep_ratio: bool = False):
        super().__init__(parent, x, y, width, height)
        self.image_path = image_path
        self.image = ImageUtils.open(image_path)
        if width != -1 or height != -1:
            if resize_keep_ratio:
                self.image.thumbnail((width, height), ImageUtils.ANTIALIAS)
            else:
                self.image = self.image.resize((width, height))

        self.content = ImageTk.PhotoImage(self.image)

    def __repr__(self):
        return f"Image(file={self.image_path})"


class TopViewPhysicsBody(GameObject):

    def __init__(self, parent: GameObject, x: float, y: float, width: float, height: float, mass: int,
                 contents: str = None, from_points: tuple = None,
                 floor_friction: float = 0.1):
        super().__init__(parent, x, y, width, height, contents, from_points)

        self.mass = mass
        self.force = Vector2d(0, 0)
        self.velocity = Vector2d(0, 0)
        self.acceleration = Vector2d(0, 0)
        self.coefficient = floor_friction

    def init_movement(self, force: int = 1):
        @self.parent.add_event_listener(event=EventType.KEYHOLD, condition=KeyEvaulator("Up"))
        def m(ctx):
            self.force.add_self(Vector2d(90, force))

        @self.parent.add_event_listener(event=EventType.KEYHOLD, condition=KeyEvaulator("Down"))
        def m(ctx):
            self.force.add_self(Vector2d(270, force))

        @self.parent.add_event_listener(event=EventType.KEYHOLD, condition=KeyEvaulator("Left"))
        def m(ctx):
            self.force.add_self(Vector2d(180, force))

        @self.parent.add_event_listener(event=EventType.KEYHOLD, condition=KeyEvaulator("Right"))
        def m(ctx):
            self.force.add_self(Vector2d(0, force))

    def update(self):
        self.acceleration = Vector2d(self.force.r, self.force.f / self.mass)
        self.force.clear()
        self.velocity.add_self(self.acceleration)
        self.acceleration.clear()
        self.position.add_vector(self.velocity)

        v = Vector2d(self.velocity.r + 180, self.velocity.f * self.coefficient)

        self.velocity.add_self(v)


class PhysicsBody(GameObject):
    def __init__(self, parent: PyNamical, x: float, y: float, width: float, height: float, mass: int = 1,
                 contents: str = None, from_points: tuple = None, row=1.225, use_mass=True, use_collide=True,
                 collision_type=1, use_gravity=True):
        super().__init__(parent, x, y, width, height, contents, from_points)

        # @self.parent.add_tick_update
        # def applyAirResistance():
        #     airResistance = (1 / 2) * self.row * (self.v_inst.f**2) * self.coeff
        #     print("AIRO",airResistance)
        #     r = (self.fnet.r + 180) % 360
        #
        #
        #     airVector = Vector2d(r,airResistance)
        #
        #     self.fnet = self.fnet.add(airVector)
        if use_mass == False:
            self.mass = 10e18
        else:
            self.mass = mass
        self.velocity = Vector2d(0, 0)
        self.use_gravity = use_gravity
        self.acceleration = Vector2d(0, 0)
        self.coeff = 0.5
        self.rectitude = 1
        self.row = row
        self.use_mass = use_mass
        self.collision_type = int(collision_type)
        self.use_collide = use_collide
        self.fnet = Vector2d(0, 0)
        self.gravity = -0.1
        

        # self.timeB = time.time()
        # self.timeA = time.time()

        if self.use_gravity: self.fnet = Vector2d(90, self.gravity * self.mass)
        if self.use_mass:
            self.attach_movement_thread()

            def update_self():
                while not self.parent.terminated:
                    self.acceleration.r = self.fnet.r
                    self.acceleration.f = self.fnet.f / self.mass
        # if self.use_collide and self.use_mass:
        #     # threading.Thread(target=self.handle_collisions).start()
        #     @self.parent.add_event_listener(event=EventType.TICK , priority = EventPriority.HIGHEST)
        #     def apply_collisions(e):
        #         self.handle_collisions()

    def attach_movement_thread(self):
        self.parent.ticksteplisteners+= 1

        def update_self():
            while self.parent.terminated == False:

                while self.parent.debug != None and self.parent.debug.tickchanger_paused:
                    time.sleep(0.01)
                    if self.parent.debug.tickchanger_stepping:
                        self.parent.debug.tickchanger_stepping = 0
                        break
                    continue

                self.update()
                time.sleep(self.parent._epoch_tps)

        threading.Thread(target=update_self).start()
                    
    def collide(self, other):
        collision = False
        if isinstance(other, GameObject):
            for j in other.points:
                for k in self.points:
                    p1 = (j[0][0] + other.position.x, (j[0][1] + other.position.y) * -1)
                    p2 = (j[1][0] + other.position.x, (j[1][1] + other.position.y) * -1)
                    q1 = (k[0][0] + self.position.x, (k[0][1] + self.position.y) * -1)
                    q2 = (k[1][0] + self.position.x, (k[1][1] + self.position.y) * -1)
                    p1 = Point(p1[0], p1[1])
                    p2 = Point(p2[0], p2[1])
                    q1 = Point(q1[0], q1[1])
                    q2 = Point(q2[0], q2[1])
                    if doIntersect(p1, p2, q1, q2):
                        collision = True
                        break
                if collision:
                    break
        return collision

    def collide_side(self, other):
        collision = False
        if isinstance(other, GameObject):
            for j in other.points:
                for k in self.points:
                    p1 = (j[0][0] + other.position.x, (j[0][1] + other.position.y) * -1)
                    p2 = (j[1][0] + other.position.x, (j[1][1] + other.position.y) * -1)
                    q1 = (k[0][0] + self.position.x, (k[0][1] + self.position.y) * -1)
                    q2 = (k[1][0] + self.position.x, (k[1][1] + self.position.y) * -1)
                    p1 = Point(p1[0], p1[1])
                    p2 = Point(p2[0], p2[1])
                    q1 = Point(q1[0], q1[1])
                    q2 = Point(q2[0], q2[1])
                    if doIntersect(p1, p2, q1, q2):
                        collision = True
                        break
                if collision:
                    break
        return collision

    def update(self):
        self.acceleration.r = self.fnet.r
        self.acceleration.f = self.fnet.f / self.mass

        self.velocity = self.velocity.add(
            Vector2d(self.acceleration.r, self.acceleration.f))

        v = Vector2d(self.velocity.r, self.velocity.f)
        v.f *= self.parent._epoch_tps
        if self.use_collide and self.use_mass and self.collision_type == 1:

            self.handle_collisions()
        elif self.use_collide and self.use_mass and self.collision_type == 2:
            pass
        x3, y3 = self.velocity.cart()

        self.position.x += x3
        self.position.y -= y3

        if self.use_gravity: self.fnet = Vector2d(90, self.gravity * self.mass)

        # if self.use_collide and self.use_mass:
        #     # threading.Thread(target=self.handle_collisions).start()
        #     @self.parent.add_event_listener(event=EventType.TICK , priority = EventPriority.HIGHEST)
        #     def apply_collisions(e):
        #         self.handle_collisions()

    def add_force(self, force):
        self.fnet = self.fnet.add(force)

    def apply_force(self, force, duration):
        def add_force():
            self.fnet = self.fnet.add(force)
            start_time = time.time()
            while True:
                if time.time() - start_time >= duration:
                    break
                time.sleep(self.parent._epoch_tps)
            self.fnet = self.fnet.subtract(force)

        thread_add_force = threading.Thread(target=add_force)
        thread_add_force.start()

    def clear(self):
        self.fnet.clear()
        self.velocity.clear()
        self.acceleration.clear()

    def handle_collisions(self):
        objects = self.parent.objects
        # while True:
        collision = False
        # if self.parent.terminated: break
        coeff = 0
        for i in objects:
            if isinstance(i, PhysicsBody) and i != self:
                for j in i.points:
                    for k in self.points:
                        p1 = (j[0][0] + i.position.x, (j[0][1] + i.position.y) * -1)
                        p2 = (j[1][0] + i.position.x, (j[1][1] + i.position.y) * -1)
                        q1 = (k[0][0] + self.position.x, (k[0][1] + self.position.y) * -1)
                        q2 = (k[1][0] + self.position.x, (k[1][1] + self.position.y) * -1)
                        p1 = Point(p1[0], p1[1])
                        p2 = Point(p2[0], p2[1])
                        q1 = Point(q1[0], q1[1])
                        q2 = Point(q2[0], q2[1])
                        if doIntersect(p1, p2, q1, q2):
                            collision = True
                            coeff = i.rectitude
                            break
                    if collision:
                        break
            if collision:
                x, y = self.velocity.cart()
                x += self.position.x
                y -= self.position.y
                pointx, pointy = self.position.x, self.position.y
                if pointx - x == 0:
                    num = pointx
                    collisions = []
                    collDist = 0

                    for k in self.points:
                        q11 = (k[0][0] + self.position.x, (k[0][1] + self.position.y) * -1)
                        q22 = (k[1][0] + self.position.x, (k[1][1] + self.position.y) * -1)
                        if min(q11[0], q22[0]) <= num <= max(q11[0], q22[0]):
                            if q11[0] == q22[0]:

                                collDist = max(abs(-self.position.y - min(q11[1], q22[1])), collDist)


                            else:
                                q1x, q1y = (q11[0], q11[1])
                                q2x, q2y = (q22[0], q22[1])
                                m = (q1y - q2y) / (q1x - q2x)
                                b = q2y - m * q2x

                                # intersection
                                yd = m * num + b
                                intersection = (num, yd)
                                if min(q11[0], q22[0]) <= intersection[0] <= max(q11[0], q22[0]) and min(q11[1],
                                                                                                         q22[1]) <= \
                                        intersection[1] <= max(q11[1], q22[1]):
                                    collDist = max(collDist, abs(-self.position.y - intersection[1]))

                vixself = self.velocity.cart()[0]
                viyself = self.velocity.cart()[1]

                vixi = i.velocity.cart()[0]
                viyi = i.velocity.cart()[1]
                # print(vixself, viyself, vixi, viyi, i.mass, self.mass)

                vfxself = (((self.mass - i.mass) / (self.mass + i.mass)) * vixself + (
                        (2 * i.mass) / (self.mass + i.mass)) * vixi) * min(self.rectitude, i.rectitude)
                vfyself = (((self.mass - i.mass) / (self.mass + i.mass)) * viyself + (
                        (2 * i.mass) / (self.mass + i.mass)) * viyi) * min(self.rectitude, i.rectitude)

                rho = np.sqrt(vfxself ** 2 + vfyself ** 2)
                phi = np.arctan2(vfyself, vfxself) * 180 / np.pi

                self.velocity = Vector2d(phi, rho)

                # time.sleep(self.parent._epoch_tps)

class Particle(PhysicsBody):

    def __init__(self, parent, x, y, r):
        super().__init__(parent, x, y, r*2, r*2)

class TextFont:

    def __init__(self, name: str = "Helvetica", size: int = 15, type: str = "", color: str = "black"):
        self.name = name
        self.size = size
        self.type = type
        self.color = color
    
    def __str__(self):
        return f"{self.name} {self.size} {self.type}"

class Text(GameObject):

    def __init__(self, parent, x, y, text, font=TextFont("Helvetica", 15), **kwargs):

        w, h = 10, 10
        super().__init__(parent, x, y, w, h)
        self.collision = False
        self.style.load_styles(kwargs.get("styles"))
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

    def update(self):
        print(self.i)
        self.i+=1